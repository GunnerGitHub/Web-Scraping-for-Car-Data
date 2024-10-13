"""
Data Scraping Drive.com for car sales.

Author: Gunit Singh
Email: gunit.singh@uq.net.au

Note: Website has approx 20,000-25,000 Vehicles
"""

from bs4 import BeautifulSoup as soup
import pandas as pd
import os
import time
import requests
import csv
from datetime import datetime

# Extract day and month
today = datetime.today()
day = today.day
month = today.strftime("%m")  # Zero-padded month

# Configuration for the base URL of the website to scrape and the path for the output CSV file.
CSV_FILE_PATH = f"Drive_MarketPlace_Data_{day}.{month}.csv"
PAGES = 760

def extract_data(market_soup):
    """
    Parses the given BeautifulSoup object (market_soup) to extract car listings data.

    Args:
        market_soup (BeautifulSoup): The BeautifulSoup object representing the HTML content of the page.

    Returns:
        list: A list of dictionaries, where each dictionary represents one car listing with keys for 
              'Year', 'Make', 'Model', 'Price', 'Mileage', 'Location', 'Additional', 'Fuel Type', 
              'Car Type', and 'Scraping Time'.
    """
    # Update the class name to match the new structure
    car_listings = market_soup.find_all('div', class_='marketplace-listing-card_drive-model-card__content__dyji4')
    vehicles_list = []
    
    for listing in car_listings:
        
        # Extract Year, Make, Model from the listing title.
        car_title = listing.find('h3', class_='truncate-2').text.strip()
        
        year, make, model = car_title.split(maxsplit=2)  # Assuming format "Year Make Model"
        
        # Updated class names for the description and type
        car_type = listing.find('div', class_='title-short-description_d_container__shortDescription__pTuw5').text.strip()
        
        price_container = listing.find('div', class_='listing-card-price-info_drive-listing-card-price-info__tgUlF')
        # Updated class names for the price container
        if price_container.find('span', class_='amount') is None or price_container.find('span', class_='type') is None:
            continue
        else:        
            price = price_container.find('span', class_='amount').text.strip() if price_container else 'N/A'
            drive_away = price_container.find('span', class_='type').text.strip() if price_container else 'N/A'
    
        specs = listing.find('div', class_='listing-card-specs_d-listing-card-specs__specs__40ZSd')
        
        mileage = None
        fuel_type = None
        location = None
        transmission = None
        if specs:
            for spec in specs.find_all('span'):
                img_alt = spec.find('img')['alt']
                if 'KilometersIcon' in img_alt:
                    mileage = spec.text.strip()
                elif 'FuelType' in img_alt:
                    fuel_type = spec.text.strip()
                elif 'LocationSpecsIcon' in img_alt:
                    location = spec.text.strip()
                elif 'TransmissionSpecsIcon' in img_alt:
                    transmission = spec.text.strip()
        
        # Ensure all required details are present before adding to the list
        if None in (mileage, fuel_type, location, transmission):
            continue
                
        scraping_time = int(time.time())  # Get the current time in Unix timestamp format
        
        # Append the extracted details, including the URL, to the list
        vehicles_list.append({
            'Year': year,
            'Make': make,
            'Model': model,
            'Price': price,
            'Mileage': mileage,
            'Location': location,
            'Additional': drive_away,
            'Fuel Type': fuel_type,
            'Car Type': car_type,
            "Transmission" : transmission,
            'Scraping Time': scraping_time
        })
    
    return vehicles_list

def scrape_page(page_number):
    """
    Scrapes a single page of car listings from Drive.com.

    Args:
        page_number (int): The page number to scrape.

    Returns:
        None
    """
    url = f"https://www.drive.com.au/cars-for-sale/search/page/{page_number}/#sortBy=recommended"
    response = requests.get(url)
    market_soup = soup(response.content, 'html.parser')
    
    vehicles_list = extract_data(market_soup)
    vehicles_df = pd.DataFrame(vehicles_list)

    if os.path.exists(CSV_FILE_PATH):
        vehicles_df.to_csv(CSV_FILE_PATH, mode='a', index=False, header=False)
    else:
        vehicles_df.to_csv(CSV_FILE_PATH, index=False)
    
def main():
    """
    Main function to execute the web scraping process.
    Iterates through pages and scrapes data.

    Args:
        None

    Returns:
        None
    """
    print("Starting Scraping")
    
    for page_no in range(1, PAGES + 1):
        scrape_page(page_no)
        print(f"Scraped page: {page_no}")
    
    print("Scraping Completed and Data Exported")

if __name__ == "__main__":
    main()

def convert_to_int(value):
    """
    Converts a string value to an integer, removing common non-numeric characters.

    Args:
        value (str): The string value to convert.

    Returns:
        int or None: The converted integer value or None if the value cannot be converted.
    """
    try:
        return int(value.replace('$', '').replace(',', '').replace(' km', '').replace(' ', ''))
    except ValueError:
        return None

def filter_csv(input_file, output_file):
    """
    Processes the input CSV file to filter out rows with non-numeric prices or mileage.
    Converts price and mileage to integers and writes the cleaned data to the output file.

    Args:
        input_file (str): The path to the input CSV file.
        output_file (str): The path to the output CSV file.

    Returns:
        None
    """
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            price_int = convert_to_int(row['Price'])
            mileage_int = convert_to_int(row['Mileage'])
            
            if price_int is not None and mileage_int is not None:
                row['Price'] = price_int
                row['Mileage'] = mileage_int
                writer.writerow(row)

# Process the scraped data
filter_csv(CSV_FILE_PATH, f'CleanedDriveData_{day}.{month}.csv')
