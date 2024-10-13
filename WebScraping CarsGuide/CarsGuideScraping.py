"""
Data Scraping CarsGuide.com for car sales.

Author: Gunit Singh
Email: gunit.singh@uq.net.au

Note: Website has approximately 50,000 listings
"""

from bs4 import BeautifulSoup as soup
import pandas as pd
import os
import time
import requests
import csv
import re
from datetime import datetime

# Extract day and month
today = datetime.today()
day = today.day
month = today.strftime("%m")  # Zero-padded month

# Constants for URLs and CSV file path
CSV_FILE_PATH = f"CarsGuide_{day}.{month}.csv"
LINKS = {
    "Electric": "https://www.carsguide.com.au/buy-a-car/used/electric-vehicle?page={}",
    "Hybrid": "https://www.carsguide.com.au/buy-a-car/used/hybrid?page={}",
    "Premium": "https://www.carsguide.com.au/buy-a-car/used/premium-fuel?page={}",
    "Diesel": "https://www.carsguide.com.au/buy-a-car/used/diesel?page={}",
    "Unleaded": "https://www.carsguide.com.au/buy-a-car/used/unleaded-fuel?page={}"
}

# List of fuel types and vehicle types as on the website
FUEL_TYPES = list(LINKS.keys())
VEHICLE_TYPES = ["suv", "ute", "hatch", "sedan", "station-wagon", "coupe", "convertible", "van", "commercial-vehicle"]

def extract_data(market_soup, fuel_type, car_type):
    """
    Extracts car listings data from CarsGuide webpage.

    Args:
    - market_soup (BeautifulSoup object): Parsed HTML content of the webpage.
    - fuel_type (str): Type of fuel (e.g., Electric, Hybrid).
    - car_type (str): Type of vehicle (e.g., suv, ute).

    Returns:
    - list: List of dictionaries representing car listings.
    - bool: True if more pages are available, False otherwise.
    """
    
    # Find all div elements that contain car listing details
    vehicles_list = []
    car_listings = market_soup.find_all('div', class_='carListing--content')
    
    for listing in car_listings:
        # Extracting advertised price
        price_tag = listing.find('span', class_='carListingPrice--advertisedPrice')
        price = price_tag.text.strip() if price_tag else 'N/A'
        
        # Extracting mileage
        mileage_tag = listing.find('span', class_='carListing--mileage')
        mileage = mileage_tag.text.strip() if mileage_tag else 'N/A'
        
        # Extracting title (including make, model, and variant)
        title_tag = listing.find('h3', class_='carListing--title')
        title = title_tag.text.strip() if title_tag else 'N/A'
        
        # Extracting dealer status
        dealer_status_tag = listing.find('div', class_='carListing--adType')
        dealer_status = dealer_status_tag.text.strip() if dealer_status_tag else 'N/A'
        
        # Extracting location
        location_tag = listing.find('div', class_='carListing--location')
        location = location_tag.text.strip() if location_tag else 'N/A'
        
        drive_away_tag = listing.find('div', class_='carListingPrice--clause')
        drive_away = drive_away_tag.text.strip() if drive_away_tag else 'N/A'
        
        if title != 'N/A':
            year, make, model = title.split(maxsplit=2)
        else:
            year = 'N/A'
            make = 'N/A'
            model = 'N/A'
            
        scraping_time = int(time.time())  # Get the current time in Unix timestamp format
        
        vehicles_list.append({
            'Year': year,
            'Make': make,
            'Model': model,
            'Price': price,
            'Mileage': mileage,
            'Location': location,
            'Dealer Status': dealer_status,
            'Additional' : drive_away,
            'Fuel Type': fuel_type,
            'Car Type': car_type,
            'Scraping Time': scraping_time
        })
    
    to_continue = len(car_listings) > 0
            
    return vehicles_list, to_continue

def scrape_page(page_number, url_template, fuel_type, car_type):
    """
    Scrapes a specific page of car listings from CarsGuide.

    Args:
    - page_number (int): Page number to scrape.
    - url_template (str): Template URL for the specific fuel and vehicle type.
    - fuel_type (str): Type of fuel (e.g., Electric, Hybrid).
    - car_type (str): Type of vehicle (e.g., suv, ute).

    Returns:
    - bool: True if more pages are available, False otherwise.
    """
    url = url_template.format(page_number)
    response = requests.get(url)
    market_soup = soup(response.content, 'html.parser')
    
    vehicles_list, to_continue = extract_data(market_soup, fuel_type, car_type)
    vehicles_df = pd.DataFrame(vehicles_list)

    if os.path.exists(CSV_FILE_PATH):
        vehicles_df.to_csv(CSV_FILE_PATH, mode='a', index=False, header=False)
    else:
        vehicles_df.to_csv(CSV_FILE_PATH, index=False)
    
    return to_continue

def main():
    """
    Main function to execute the scraping process for all fuel and vehicle types.
    """
    for fuel_type, url_template in LINKS.items():
        for car_type in VEHICLE_TYPES:
            page_number = 1
            to_continue = True
            
            while to_continue and page_number <= 500:  # Limiting to 500 pages for safety
                try:
                    to_continue = scrape_page(page_number, url_template, fuel_type, car_type)
                    print(f"Scraped Page {page_number} for Fuel Type {fuel_type} and Car Type {car_type}")
                except Exception as e:
                    print(f"Page {page_number} failed for Fuel Type {fuel_type} and Car Type {car_type}: {str(e)}")
                
                page_number += 1

if __name__ == "__main__":
    main()

# Additional function to clean the scraped CSV file
def clean_csv(input_filepath, output_filepath):
    """
    Cleans the scraped CSV file by converting price and mileage to integers and simplifying dealer status.

    Args:
    - input_filepath (str): Path to the input CSV file.
    - output_filepath (str): Path to the output cleaned CSV file.
    """
    def clean_price(price):
        return int(re.sub(r'[^\d]', '', price)) if price.isdigit() else None
    
    def clean_mileage(mileage):
        return int(re.sub(r'[^\d]', '', mileage)) if mileage.isdigit() else None
    
    def clean_dealer_status(dealer_status):
        return 'USED'  # Simplifying dealer status
    
    with open(input_filepath, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_filepath, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            row['Price'] = clean_price(row['Price'])
            row['Mileage'] = clean_mileage(row['Mileage'])
            row['Dealer Status'] = clean_dealer_status(row['Dealer Status'])
            writer.writerow(row)

# Clean the CSV file
input_filepath = "CarsGuide_{day}.{month}.csv"
output_filepath = "CleanedCarsGuide_{day}.{month}.csv"
clean_csv(input_filepath, output_filepath)
