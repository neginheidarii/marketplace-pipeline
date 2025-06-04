import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


# Fetch the search results page
def fetch_kijiji_search_results(search_term="laptop"):
    search_term_encoded = search_term.replace(" ", "-")
    url = f"https://www.kijiji.ca/b-buy-sell/gta-greater-toronto-area/{search_term_encoded}/k0c10l1700272"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')




# Extract product info
def extract_kijiji_listings(soup):
    listings = []


    for item in soup.select('[data-testid="listing-card"]'):
        title_elem = item.select_one('[data-testid="listing-title"] a')
        price_elem = item.select_one('[data-testid="listing-price"]')
        location_elem = item.select_one('[data-testid="listing-location"]')


        if title_elem:
            listings.append({
                "title": title_elem.get_text(strip=True),
                "price": price_elem.get_text(strip=True).replace("$", "").replace(",", "") if price_elem else "N/A",
                "location": location_elem.get_text(strip=True) if location_elem else "Unknown",
                "url": title_elem["href"],
                "post_time": datetime.now().isoformat()
            })

    return listings

 

# Save data to JSON file
if __name__ == "__main__":
    print("🔍 Fetching Kijiji search results...")
    soup = fetch_kijiji_search_results("laptop")

# Debugging: Save the raw HTML to a file
    # with open("kijiji_page.html", "w") as f:
    #     f.write(soup.prettify())


    print("🔍 Extracting listings...")
    listings = extract_kijiji_listings(soup)

    with open("../data/raw/listings.json", "w") as f:
        json.dump(listings, f, indent=2)

    print(f"✅ Saved {len(listings)} listings to data/raw/listings.json")
