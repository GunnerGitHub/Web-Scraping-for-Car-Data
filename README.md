# Web-Scraping-for-Car-Data
   Repository to store code and research done for the Thesis: Data Scraping and Analysis of Used Car Sales Data for Battery Electric Vehicles in Australia.

# Repository Structure
## 1. Data Analysis
This folder contains Python scripts and Jupyter notebooks designed for data analysis, focusing on vehicle depreciation, mileage trends, and fuel types.

DriveFuelType.py: This Python script categorizes cars based on their fuel type using the data collected from various web sources.
Depreciation Analysis
Focuses on analyzing how different car models depreciate over time, with specific attention to MSRP (Manufacturer’s Suggested Retail Price) and data from Drive.com.

Drive.com Data.xlsx: Contains raw listing data from Drive.com, used as a basis for further depreciation analysis.

Listings.xlsx: Another dataset focused on car listings.

MSRP Depreciation:

DepreciationAnalysis.ipynb: Jupyter notebook analyzing how cars depreciate relative to their MSRP over time. It includes statistical analysis and visualizations to illustrate trends.
GetMergedData.ipynb: Merges various datasets for unified analysis, focusing on MSRP and listing prices.
RetentionRateAnalysis.ipynb: Explores retention rates across different car models, providing insights into how long cars hold their value.
StatisticsSummary.ipynb: Summarizes key statistics of the collected datasets, providing an overview of the major trends.
Electric Ranges:
CarDetailsFromShowroom.py: Scrapes car details from showroom links to gather electric vehicle (EV) range data.
DriveShowroomScraper.py: A web scraper to extract data from Drive.com's showroom pages specifically related to electric cars.
ElectricVehiclesInfoFromShowroomLinks.xlsx: Dataset containing details on EVs collected from the showroom.
RangeAnalysis.ipynb: Analyzes the ranges of electric vehicles, comparing the data gathered through scraping to real-world performance.
Top Listings:
CarsInListings.xlsx: Data about cars that frequently appear in top listings on Drive.com.
CodeForGettingTopListings, Courtesy of ChatGPT.txt: Code provided to extract top car listings.
Grouped_Cars_Data.csv: Grouped data for the top cars in the listings.
Top Cars in Listings.csv: CSV file containing details of the top cars by listing frequency.
General Statistics
StatisticsSummary.ipynb: Provides general statistical insights into the collected car data, including distribution and summary statistics for various variables.
Mileage Analysis
This section analyzes vehicle mileage accumulation, looking at how different factors such as fuel type and car model affect mileage.

MileageAnalysis.ipynb: Detailed notebook that analyzes mileage trends across different vehicle models and categories.
Old:
MileageAnalysis.ipynb: An older version of the mileage analysis, kept for reference.
## 2. Web Scraping
Contains Python scripts used for web scraping from car-related websites.

CarsGuideScraping.py: Scrapes car data from CarsGuide, focusing on vehicle specifications and listings.
DriveScraping.py: Scrapes car data from Drive.com, used for the depreciation and listing analysis.
