import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tabulate import tabulate
from tqdm import tqdm


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
csv_file = 'isin_codes.csv'
isin_df = pd.read_csv(csv_file) if csv_file else pd.DataFrame(columns=["Timestamp", "ISIN", "Value"])

# List for data to save
data_to_save = []

# Create a list of headers for the table
table_headers = ["Timestamp", "ISIN", "Value"]

# Create a list for the table data
table_data = []

# Iterate over each row of the DataFrame with tqdm to display the progress bar

print("\nRetrieving quotes for the listed ETFs...")
for index, row in tqdm(isin_df.iterrows(), desc="Progress", total=len(isin_df),
                       bar_format="{desc}: {percentage:3.0f}%|{bar}|"):
    type = row['type']
    isin = row['ISIN']
    content = get_realtime_quotes_content(isin, type)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Add the data to the list for the table
    table_data.append([timestamp, isin, content])

    # Add the data to the list for saving
    data_to_save.append([timestamp, isin, content])

# Create a DataFrame with the data
df_to_save = pd.DataFrame(data_to_save, columns=['Timestamp', 'ISIN', 'Value'])

# Save the DataFrame to a CSV file in append mode
csv_output_file = 'etf_quote_tracking.csv'
df_to_save.to_csv(csv_output_file, mode='a', index=False, header=not csv_file)

# Display the table at the end of processing
print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
