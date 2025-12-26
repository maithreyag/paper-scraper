import os
from dotenv import load_dotenv
import pyalex
from pyalex import Works, autocomplete
from playwright.sync_api import sync_playwright
from google import genai
from google.genai import types
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
import psycopg2

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt = "You are an expert researcher. Extract ONLY the research paper titles from the provided text. Ignore years, authors, conferences, etc"

email = os.getenv("EMAIL")
pyalex.config.email = email

class TitlesRecipe(BaseModel):
    titles: list[str]

# Takes in url and outputs list of paper titles on that page
def get_titles_from_page(url):
    print(f"Scraping from {url}...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        scraped_text = page.inner_text("body")
        browser.close()

    print(f"Sending {len(scraped_text)} chars to Gemini...")
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[prompt, scraped_text],
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=TitlesRecipe,
        ),
    )

    parsed_response = response.parsed
    titles = parsed_response.titles
    titles = list(set(titles))
    print(f"Extracted {len(titles)} titles successfully.")

    return titles

def get_paper_by_title(title):
    response = Works().autocomplete(title)
    return response[0] if response else None

def process_page(url):
    titles = get_titles_from_page(url)

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = [res for res in executor.map(get_paper_by_title, titles) if res]

    works = []
    step = 50

    for i in range(0, len(results), step):
        ids = [res["id"] for res in results[i:i+50]]

        id_filter = "|".join(ids)
        
        works.extend(Works().filter(openalex=id_filter).get(per_page=50))
    
    print(f"Retrieved {len(works)} works from OpenAlex")

    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(database_url)
    try:
        print(f"Writing records to database...")
        for work in works:
            store_metadata(work, conn)
    finally:
        conn.close()

    print("Done!")
    
    return

def store_metadata(data, conn):
    # make a join table later for topics, authors

    oa_id = data.get("id", "")
    title = data.get("title", "")
    abstract = data["abstract"]
    date = data.get("publication_date", "")

    primary_location = data.get("primary_location", {})
    link = primary_location.get("landing_page_url", "")

    authorships = data.get("authorships", [])
    primary_author = ""
    if authorships:
        primary_author = authorships[0].get("author").get("display_name")

    to_write = (title, primary_author, abstract, oa_id, link, date)

    # send to postgres DB
    with conn:
        with conn.cursor() as cursor:
            write_sql = """
            INSERT INTO papers (oa_id, title, primary_author, abstract, link, date)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (oa_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                primary_author = EXCLUDED.primary_author,
                abstract = EXCLUDED.abstract,
                link = EXCLUDED.link,
                date = EXCLUDED.date;
            """
            cursor.execute(write_sql, to_write)
    
    return

# Test:
# process_page("https://rail.eecs.berkeley.edu/publications.html")