import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


# Fetch the eBay search results page
def fetch_ebay_search_results(search_term="laptop"):
    base_url = f"https://www.ebay.com/sch/i.html?_nkw={search_term.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(base_url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    return soup

