import pandas as pd
import requests
import matplotlib.pyplot as plt

# Download data (using a secure method) 
url = 'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/daily_covid_confirmed_global.csv'  # Secure URL for data retrieval

def download_and_analyze(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            df = pd.read_csv(response.content, index_col="Province/State")  
            print("Data loaded successfully.")

            # Clean and analyze the data (optional) ... 
            country_data = df.groupby(["Country/Region"])["Confirmed"].sum().sort_values(ascending=False)

            plt.figure(figsize=(10, 6))  
            plt.bar(country_data.index, country_data.values)
            plt.xlabel("Country/Region")
            plt.ylabel("Total Cases")
            plt.title("COVID-19 Cases by Country")
            plt.xticks(rotation=45)
            plt.tight_layout() 
            plt.savefig('covid_cases.png')
            plt.show()
        except Exception as e:  
            print("An error occurred during data loading or analysis:", e)

    else: 
        print("Error: Failed to download data.")

# Download and analyze the COVID-19 data
download_and_analyze(url) 