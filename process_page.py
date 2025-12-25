import os
from dotenv import load_dotenv
import pyalex
from pyalex import Works
from playwright.sync_api import sync_playwright
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt = "You are an expert researcher. Extract ONLY the research paper titles from the provided text. Ignore years, authors, conferences, etc"

class TitlesRecipe(BaseModel):
    titles: list[str]

# Takes in url and outputs list of paper titles on that page
def process_page(url):
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

# Test: 
# rail_titles = process_page("https://rail.eecs.berkeley.edu/publications.html")
# print(rail_titles)

email = os.getenv("EMAIL")
pyalex.config.email = email

# Returns paper metadata by title, may fail if incomplete word in title
def search_paper_by_title(title):
    response = Works().search_filter(title=title).get()
    if response:
        print(len(response))
    else:
        print("No results found.")