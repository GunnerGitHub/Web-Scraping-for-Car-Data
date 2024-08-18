import pandas as pd
from DriveShowroomScraper import scrape_car_details

# This is a webscraper developed to scrape Car information from Drive.com Showroomm links

df1 = pd.read_excel('All_Electric_Vehicles_Listed.xlsx')
#df3=  pd.read_excel('car_details.xlsx')

links = []

links_done = []
# Corrected loop for df2
# for index, row in df3.iterrows():
#     if not pd.isna(row['Link']):
#         links_done.append(row['Link'])

# Loop for df1
for index, row in df1.iterrows():
    if not pd.isna(row['Website']) and "drive.com.au/showrooms/" in row['Website']:
        if row['Website'] not in links_done:
            links.append(row['Website'])

# Links should only hold links needing to be scraped not already done
print(links)

# List to hold all car details
all_car_details = []

i = 0
# Iterate over links and scrape details
for link in links:
    print(i)
    i+=1
    details = scrape_car_details(link)
    # Add the 'Link' key to the dictionary at the front
    details_with_link = {'Link': link}
    details_with_link.update(details)
    all_car_details.append(details_with_link)

# # Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_car_details)

# # Export the DataFrame to an Excel file
df.to_csv('car_details.csv', index=False, header=True)
print("Data exported to Excel successfully.")