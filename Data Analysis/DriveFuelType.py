import pandas as pd

# Script to standardise vehicle types for Drive.com listings

# Load your CSV data
data = pd.read_excel('FilteredData.xlsx')

VEHICLES_TYPES = ["suv","ute","hatch","sedan","station-wagon","coupe", "convertible", "van", "commercial-vehicle"]

# Function to categorize car type
def categorize_car_type(car_type):
    """
    Categorizes a car type based on a predefined list of vehicle types.
    
    Parameters:
    input_car_type (str): The type of car to categorize.
    
    Returns:
    str: The categorized vehicle type if found, otherwise 'NA'.
    """
    car_type = car_type.lower()
    
    for vehicle_type in VEHICLES_TYPES:
        if vehicle_type in car_type:
            return vehicle_type
    return 'NA'  # Default category

# Apply the categorization function to the 'Car Type' column
data['Car Type'] = data['Car Type'].apply(categorize_car_type)


# Save the modified data back to CSV
data.to_csv('UpdatedFilteredData.csv', index=False)