import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
import re

# response = requests.get("https://songsfortheday.wordpress.com/")
# print(response)
# bs = BeautifulSoup(response.text, "lxml")
# print(bs.find("body").text)

# Function to save site URL and its corresponding data to the output CSV
def save_to_csv(csv_file_name, url, data):
    if data:  # Only save if there's valid data
        with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([url, data])  # Append URL and data to CSV

def iteration_urls(csv_file_path,output_csv_path):
    # with open(csv_file_path,mode='r') as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         url = row[0]
    #         if validating_url(url):
    #             data = fetch_data(url)
    #             save_to_csv(output_csv_file, url, data)
    #         else:
    #             print(f"Invalid URL :{url}")

    df_input = pd.read_csv(csv_file_path)
    output_data = []
    
    for index, row in df_input.iterrows():
        url = row['urls']  # Assuming 'url' column exists in the input CSV
        print("Inside the urls :",url)
        if validating_url(url):
            data = fetch_data(url)  # Fetch data for the valid URL
            print('Inside Data : ',data)
            if data:  # Only add if data was successfully fetched
                print(f"URL: {url}")
                # print(f"Fetched Data Before Creating DataFrame: {data[:100]}...")  # Print first 100 characters
                # df_output = pd.DataFrame({'urls': [url], 'data': [data]})
                # print(f"Appending to CSV: {df_output}")  # Debugging the DataFrame content
                # df_output.to_csv(output_csv_path, mode='a', header=False, index=False)
                save_to_csv(output_csv_path, url, data)
                print(f"Data successfully written to {output_csv_path}")
            else:
                print(f"No data fetched for {url}. Skipping.")
        else:
            print(f"Invalid URL: {url}")


    # df_output = pd.DataFrame(output_data)

    # # Save the result DataFrame to the output CSV
    # df_output.to_csv(output_csv_file, index=False)  # Do not write row numbers

def validating_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)

def cleaned_data(data):
    if data:
        data.strip()
         # Replace multiple newlines with a single space
        data = re.sub(r'\s+', ' ', data)  # Replace any space, tab, or newline sequence with a single space
        data = re.sub(r'[^\w\s]', '', data)  

        print('Cleaned Data :',data) 

        return data      


def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses (e.g., 404)
        bs = BeautifulSoup(response.text, "lxml")
        body_text =  bs.find("body").text.strip()
        if not body_text:
            print(f"No data found for {url}")
            return None  # Return None if no data is found
        return cleaned_data(body_text)

    except requests.exceptions.RequestException as e:
        # Catch all types of exceptions from requests (e.g., 404, connection errors, etc.)
        print(f"Error fetching data from {url}: {e}")
    
csv_file = 'all_urls.csv'
output_csv_file = 'output_data.csv'
# Create the output CSV file with headers 'url' and 'data'
pd.DataFrame(columns=['url', 'data']).to_csv(output_csv_file, index=False)

iteration_urls(csv_file,output_csv_file)

def main():
    pass