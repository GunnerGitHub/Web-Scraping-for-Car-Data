"""
Data Scraping Facebook Market Place for used cars

Author: Gunit Singh
Email: gunit.singh@uq.net.au

TO DO: Figure out how to filter by fuel type? How to avoid filters but still maximise results.
https://www.facebook.com/marketplace/brisbane/search?daysSinceListed=30&minMileage=100&maxMileage=200000&minYear=2010&maxYear=2024&query=Cars&exact=false
"""

from splinter import Browser
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import time
import os

# Configuration
BASE_URL = "https://www.facebook.com/marketplace/{}/search?"
PARAMS = {
    'minPrice': 1000,
    'maxPrice': 250000,
    'minMileage': 100,
    'maxMileage': 200000,
    'minYear': 2010,
    'maxYear': 2023,
    'query': '{}',
    'exact': 'false'
}
CSV_FILE_PATH = "Facebook_MarketPlace_Data.csv"

electric_vehicles = {'Tesla Model Y': 5,
 'Tesla Model 3': 5,
 'BYD Atto 3': 5,
 'MG 4': 5,
 'Volvo XC40 Recharge': 4,
 'MG ZS EV': 4,
 'Polestar 2': 3,
 'Kia EV6': 3,
 'Mercedes-Benz EQA': 3,
 'Volvo C40 Recharge': 3,
 'Kia Niro EV': 2,
 'Hyundai Ioniq 5': 2,
 'BMW iX1': 2,
 'BYD Dolphin': 2,
 'Cupra Born': 2,
 'Hyundai Kona Electric': 2,
 'BMW iX': 2,
 'Mercedes-Benz EQB': 2,
 'BMW iX3': 2,
 'Hyundai Ioniq 6': 2,
 'Mini Cooper SE': 2,
 'Porsche Taycan': 2,
 'GWM Ora': 2,
 'Nissan Leaf': 2,
 'BYD Seal': 2,
 'Mercedes-Benz EQE': 2,
 'BMW i4': 2,
 'Audi E-Tron GT': 2,
 'Mercedes-Benz EQC': 2,
 'Lexus RZ450e': 2,
 'Mercedes-Benz EQE SUV': 1,
 'Kia EV9': 1,
 'Audi E-Tron': 1,
 'Genesis GV60': 1,
 'Fiat/Abarth 500e': 1,
 'Lexus UX300e': 1,
 'LDV eT60': 1,
 'Genesis Electrified GV70': 1,
 'Foton Mobility T5': 1,
 'Peugeot e-Partner': 1,
 'Mercedes-Benz EQS': 1,
 'BMW i7': 1,
 'Ford E-Transit': 1,
 'Mercedes-Benz EQS SUV': 1,
 'Peugeot e-2008': 1,
 'Ford Mustang Mach-E': 1,
 'LDV eDeliver 9': 1,
 'BMW i5': 1,
 'Mercedes-Benz eVito Van': 1,
 'Jaguar I-Pace': 1,
 'SEA Electric trucks': 1,
 'Mercedes-Benz eVito Tourer': 1,
 'Renault Kangoo EV': 1,
 'Mazda MX-30 Electric': 1,
 'LDV Mifa 9': 1,
 'Genesis Electrified G80': 1,
 'Mercedes-Benz EQV': 1,
 'Hyundai Mighty Electric': 1,
 'LDV eDeliver7': 1,
 'Renault Megane E-Tech': 1,
 'Rolls-Royce Spectre': 1}

cities = ['brisbane', 'sydney', 'melbourne', 'hobart', 
          'adelaide', 'perth', 'canberra', 'darwin']

# Function to construct the search URL
def construct_url(base_url, city, car_model, params):
    params['query'] = car_model
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{base_url.format(city)}{query}"

# Function to scroll and load page
def scroll_page(browser, scroll_count=4, scroll_delay=2):
    for _ in range(scroll_count):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_delay)
        
# Function to extract data
def extract_data(market_soup):
    # Extract all the necessary info and insert into lists by INSPECT ELEMENT
    titles_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
    titles_list = [title.text.strip() for title in titles_div]
    prices_div = market_soup.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
    prices_list = [price.text.strip() for price in prices_div]
    mileage_div = market_soup.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1nxh6w3 x1sibtaa xo1l8bm xi81zsa")
    mileage_list = [mileage.text.strip() for mileage in mileage_div]
    urls_div = market_soup.find_all('a', class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv")
    urls_list = [url.get('href') for url in urls_div]
    
    # Add all values to a list of dictionaries
    vehicles_list = []

    for i, item in enumerate(titles_list):
        cars_dict = {}
        
        title_split = titles_list[i].split()
        
        cars_dict["Year"] = int(title_split[0])
        cars_dict["Make"] = title_split[1]
        if len(title_split)>2:
            cars_dict["Model"] = title_split[2:]
        cars_dict["Location"] = mileage_list[2*i]
        cars_dict["Price"] = int(re.sub(r'[^\d.]', '', prices_list[i]))
        cars_dict["Mileage"] = mileage_list[2*i+1]
        cars_dict["URL"] = urls_list[i]
        vehicles_list.append(cars_dict)
        
    return vehicles_list


# Main function to run the scraper
def main():
    print("Starting Scraping")
    
    browser = Browser('chrome')

    for city in cities:
        for car_model, scroll_count in electric_vehicles.items():
            print(city,car_model)
            PARAMS = {
                'minPrice': 1000,
                'maxPrice': 250000,
                'minMileage': 100,
                'maxMileage': 200000,
                'minYear': 2010,
                'maxYear': 2023,
                'exact': 'false'
            }
            
            url = construct_url(BASE_URL, city, car_model, PARAMS)
            
            browser.visit(url)
            
            # Use the value from the dictionary as the scroll count
            scroll_page(browser, scroll_count)
            
            market_soup = soup(browser.html, 'html.parser')
            
            try:
                vehicles_list = extract_data(market_soup)
            except:
                continue
            
            # Filtering vehicles by make
            vehicles_list = [v for v in vehicles_list if car_model.split()[0].lower() in v['Make'].lower()]
            
            # Extract vehicle data and save it to a DataFrame.
            vehicles_df = pd.DataFrame(vehicles_list)

            # Check if the CSV file already exists.
            if os.path.exists(CSV_FILE_PATH):
                # Append without writing the header.
                vehicles_df.to_csv(CSV_FILE_PATH, mode='a', index=False, header=False)
            else:
                # Create a new file and write with the header.
                vehicles_df.to_csv(CSV_FILE_PATH, index=False)
    
    browser.quit()
    
    print("Scraping Completed and Data Exported")


if __name__ == "__main__":
    main()