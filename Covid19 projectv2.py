import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Step 1: Define the URL for the latest COVID-19 confirmed cases data
# The data is hosted on GitHub in the CSSEGISandData/COVID-19 repository.
# We use the raw URL to download the CSV directly.
DATA_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

def download_data(url):
    """
    Download the CSV data from the provided URL.
    
    Parameters:
    url (str): The URL to the CSV file.
    
    Returns:
    str: The content of the CSV as a string, or None if download fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes (4xx/5xx)
        print("Data downloaded successfully.")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        return None

def clean_and_analyze_data(csv_content):
    """
    Clean and analyze the COVID-19 data using pandas.
    
    - Read the CSV content into a DataFrame.
    - Group by 'Country/Region' and sum the latest confirmed cases (last column).
    - Clean the data by handling missing values if any.
    
    Parameters:
    csv_content (str): The CSV data as a string.
    
    Returns:
    pd.Series: Sorted series of total cases by country.
    """
    try:
        # Read CSV from string content
        df = pd.read_csv(StringIO(csv_content))
        
        # Print initial shape for debugging
        print(f"DataFrame shape: {df.shape}")
        
        # The dataset has columns: Province/State, Country/Region, Lat, Long, and then date columns
        # The last column is the most recent date with cumulative confirmed cases
        latest_date = df.columns[-1]  # Last column is the latest date
        
        # Group by Country/Region and sum the latest cases (handles countries with multiple provinces)
        country_cases = df.groupby('Country/Region')[latest_date].sum().sort_values(ascending=False)
        
        # Handle any NaN values (though unlikely in this dataset)
        country_cases = country_cases.fillna(0)
        
        print("Data cleaned and analyzed.")
        return country_cases
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def create_bar_chart(country_cases, top_n=20):
    """
    Create a matplotlib bar chart of the top N countries by total cases.
    
    - Plot horizontal bar chart for better readability.
    - Save the plot as 'covid_cases.png'.
    
    Parameters:
    country_cases (pd.Series): Series with countries as index and cases as values.
    top_n (int): Number of top countries to display.
    """
    if country_cases is None or country_cases.empty:
        print("No data to plot.")
        return
    
    # Select top N countries
    top_countries = country_cases.head(top_n)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    top_countries.plot(kind='barh', color='skyblue')
    plt.title(f'Top {top_n} Countries by Total COVID-19 Confirmed Cases')
    plt.xlabel('Total Confirmed Cases')
    plt.ylabel('Country/Region')
    plt.gca().invert_yaxis()  # Invert y-axis to have highest at top
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('covid_cases.png')
    print("Plot saved as 'covid_cases.png'.")
    
    # Optionally show the plot (comment out if not needed)
    # plt.show()

# Main execution
if __name__ == "__main__":
    # Download the data
    csv_content = download_data(DATA_URL)
    
    if csv_content:
        # Clean and analyze
        country_cases = clean_and_analyze_data(csv_content)
        
        if country_cases is not None:
            # Create and save the chart
            create_bar_chart(country_cases)