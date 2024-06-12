import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tabulate import tabulate
from tqdm import tqdm
import os  # Import the os module for file operations

def get_realtime_quotes_content(isin, type):
    url = f"https://www.borsaitaliana.it/borsa/{type}/scheda/{isin}.html"
    response = requests.get(url)

    if response.status_code == 200:
        content = '\n'.join(response.text.splitlines()[:500])

        soup = BeautifulSoup(content, 'html.parser')
        price_div = soup.find('div', class_='summary-value')
        if price_div:
            price_span = price_div.find('strong')
            if price_span:
                raw_text = price_span.get_text(strip=True)
                # Check if content is a number in international format (comma for decimal)
                try:
                    float_content = float(raw_text.replace(',', '.'))
                    return float_content
                except ValueError:
                    return raw_text
            else:
                return f"Error: {response.status_code}"

# Read the CSV file with ISINs
csv_file = 'portfolio.csv'
isin_df = pd.read_csv(csv_file) if os.path.isfile(csv_file) else pd.DataFrame(columns=["timestamp", "ISIN", "quote", "quantity"])

# List for data to save
data_to_save = []

# Create a list of headers for the table
table_headers = ["Timestamp", "ISIN", "Quantity", "Quote", "Market Value"]

# Create a list for the table data
table_data = []

# Iterate over each row of the DataFrame with tqdm to display the progress bar
print("\nRetrieving quotes for the listed ETFs...")
total_market_value = 0
for index, row in tqdm(isin_df.iterrows(), desc="Progress", total=len(isin_df),
                       bar_format="{desc}: {percentage:3.0f}%|{bar}|"):
    type = row['type']
    isin = row['ISIN']
    content = get_realtime_quotes_content(isin, type)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Calculate market value
    market_value = content * row['quantity']
    total_market_value += market_value  # Add market value to total

    # Sanitize market value (trim to 2 decimals)
    market_value = round(market_value, 2)

    # Add the data to the list for the table
    table_data.append([timestamp, isin, row['quantity'], content, market_value])

    # Add the data to the list for saving
    data_to_save.append([timestamp, isin, row['quantity'], content, market_value])

# Add a new row for total market value to the table data
table_data.append(['', '', '', 'Total Market Value:', round(total_market_value, 2)])

# Create a DataFrame with the data
df_to_save = pd.DataFrame(data_to_save, columns=['timestamp', 'ISIN', 'quantity', 'quote', 'market_value'])

# Check if the output file already exists
output_file_exists = os.path.isfile('tracking.csv')

# Save the DataFrame to a CSV file in append mode, with headers if the file doesn't exist
with open('tracking.csv', 'a') as f:
    df_to_save.to_csv(f, mode='a', index=False, header=not output_file_exists)

# Display the table at the end of processing
print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
