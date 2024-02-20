"""
Data Scraping Drive.com for car sales.

Author: Gunit Singh
Email: gunit.singh@uq.net.au

Note: Website has approx 760 pages to be scraped (27000 vehicles)

"""

from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import os
import time
import requests

# Configuration for the base URL of the website to scrape and the path for the output CSV file.
BASE_URL = "https://www.drive.com.au/cars-for-sale/search/page/{}/#sortBy=recommended"
CSV_FILE_PATH = "Drive_MarketPlace_Data.csv"
PAGES = 760
        
# Function to extract data from the webpage.
def extract_data(market_soup):
    """
    Parses the given BeautifulSoup object (market_soup) to extract car listings data.
    The data is extracted from specific HTML elements identified by their class names.
    Each car listing includes details such as Year, Make, Model, Price, Location, Mileage, and Fuel Type.
    Returns a list of dictionaries, where each dictionary represents one car listing.
    """
    # Find all div elements that contain car listing details.
    listings = market_soup.find_all('div', class_='marketplace-listing-card_drive-model-card__content__5gRhp')
    all_car_details = []
    
    for listing in listings:
        # Extract Year, Make, Model from the listing title.
        car_title = listing.find('h3', class_='truncate-2').text.strip()
        year, make, model = car_title.split(maxsplit=2)  # Assuming format "Year Make Model"
    
        # Extract Price from the listing.
        price = listing.find('div', class_='marketplace-listing-card_drive-model-card__price__aYQsj').text.strip()
    
        mileage = None
        fuel_type = None
        location = None
        # Extract additional specifications like Mileage, Fuel Type, and Location.
        specs = listing.find('div', class_='marketplace-listing-card_drive-model-card__specs__MmOgJ')
        if specs:
            for spec in specs.find_all('span'):
                img_alt = spec.find('img')['alt']
                if 'KilometersIcon' in img_alt:
                    mileage = spec.text.strip()
                elif 'FuelTypePetrolIcon' in img_alt:
                    fuel_type = spec.text.strip()
                elif 'LocationSpecsIcon' in img_alt:
                    location = spec.text.strip()
    
        if mileage == None or fuel_type == None or location == None:
            continue
        
        # Extract URL
        link_tag = listing.find('a', attrs={'data-cy': 'CarTitle-permalink'})
        url = "drive.com.au" + link_tag['href'] if link_tag else None
    
        # Append the extracted details, including the URL, to the list
        all_car_details.append({
            'Year': year,
            'Make': make,
            'Model': model,
            'Price': price,
            'Location': location,
            'Mileage': mileage,
            'Fuel Type': fuel_type,
            'URL': url
        })
    
    print(all_car_details)
    return all_car_details

def scrape_page(page_number):
    url = f"https://www.drive.com.au/cars-for-sale/search/page/{page_number}/#sortBy=recommended"
    response = requests.get(url)
    market_soup = soup(response.content, 'html.parser')
    
    # Extract vehicle data and save it to a DataFrame.
    vehicles_list = extract_data(market_soup)
    vehicles_df = pd.DataFrame(vehicles_list)

    # Check if the CSV file already exists.
    if os.path.exists(CSV_FILE_PATH):
        # Append without writing the header.
        vehicles_df.to_csv(CSV_FILE_PATH, mode='a', index=False, header=False)
    else:
        # Create a new file and write with the header.
        vehicles_df.to_csv(CSV_FILE_PATH, index=False)

# Main function to execute the scraper.
def main():
    print("Starting Scraping")
    
    # Initialise the browser instance using Splinter and navigate to the BASE_URL.
    browser = Browser('chrome')
    
    for page_no in range(1, PAGES+1):
        scrape_page(page_no)
        print(page_no)
    
    browser.quit()
    print("Scraping Completed and Data Exported")

if __name__ == "__main__":
    main()
