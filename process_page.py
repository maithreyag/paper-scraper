import os
from dotenv import load_dotenv
import pyalex
from pyalex import Works
from playwright.sync_api import sync_playwright
from google import genai
from google.genai import types
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt = "You are an expert researcher. Extract ONLY the research paper titles from the provided text. Ignore years, authors, conferences, etc"

class TitlesRecipe(BaseModel):
    titles: list[str]

# Takes in url and outputs list of paper titles on that page
def get_titles_from_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        scraped_text = page.inner_text("body")
        browser.close()

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

    return titles

email = os.getenv("EMAIL")
pyalex.config.email = email

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

    store_metadata(works)
    
    return len(works)

def store_metadata(data):
    pass