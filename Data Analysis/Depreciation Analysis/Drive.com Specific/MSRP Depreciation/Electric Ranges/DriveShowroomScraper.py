import requests
from bs4 import BeautifulSoup

# Script to scrape car details from a given Drive.com showroom link

def scrape_car_details(url):
    # Send a request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extracting car model and price with null checks
        title_element = soup.find('h1', class_='variant_drive-showrooms-variant__title__25Gis')
        price_element = soup.find('div', class_='variant_drive-showrooms-variant__price__value__qa_aW')
        
        title = title_element.text.strip() if title_element else "No title available"
        price = price_element.text.strip() if price_element else "No price available"
        
        result = {
            'Model': title,
            'Price': price
        }
        
        # Identifying all tables
        tables = soup.find_all('table', class_='specs-table_drive-specs-table__SkMny')
        temp = 0
        for table in tables:
            # Attempt to find a heading or identifier for the table
            heading = table.find_previous('h3')
            table_heading = heading.text.strip() if heading else "Unknown Table"
            
            if temp >= 1 and "Ownership & Safety" not in table_heading:
                continue  # Skip subsequent tables unless they are "Ownership & Safety"
            
            rows = table.find_all('tr')
            for row in rows:
                title_cell = row.find('div', class_='specs-table_drive-specs-table__cell__row-title__3qeeX')
                data_cell = row.find('div', class_='specs-table_drive-specs-table__cell__data__QStuY')
                if title_cell and data_cell:
                    key = title_cell.text.strip()
                    value = data_cell.text.strip()
                    # Adding each specification directly to the main dictionary
                    result[key] = value
            temp += 1
        
        return result

    else:
        return {"Error": f"Failed to retrieve the webpage. Status code: {response.status_code}"}
