import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tabulate import tabulate
from tqdm import tqdm
import os


def fetch_realtime_quote(isin, type):
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
                try:
                    return float(raw_text.replace(',', '.'))
                except ValueError:
                    return raw_text
    return None


def read_portfolio(file_path):
    if os.path.isfile(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame(columns=["timestamp", "ISIN", "quote", "quantity"])


def save_tracking_data(file_path, data):
    output_file_exists = os.path.isfile(file_path)
    with open(file_path, 'a') as f:
        data.to_csv(f, mode='a', index=False, header=not output_file_exists)


def calculate_value(portfolio_df):
    table_headers = ["Timestamp", "ISIN", "Quantity", "Quote", "Market Value"]
    table_data = []
    total_market_value = 0

    for index, row in tqdm(portfolio_df.iterrows(), desc="Progress", total=len(portfolio_df),
                           bar_format="{desc}: {percentage:3.0f}%|{bar}|"):
        type = row['type']
        isin = row['ISIN']
        quantity = row['quantity']

        quote = fetch_realtime_quote(isin, type)
        if quote is None:
            continue

        market_value = round(quote * quantity, 2)
        total_market_value += market_value

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        table_data.append([timestamp, isin, quantity, quote, market_value])

    # Add a last row for total market value to the table data
    table_data.append(['', '', '', 'Total Market Value:', round(total_market_value, 2)])

    return table_headers, table_data, total_market_value


def display_table(headers, data):
    print(tabulate(data, headers=headers, tablefmt="grid"))


def main():
    print("\nETF Quote Tracking"
          "\n------------------")
    print("Retrieving quotes for the listed ETFs...")

    csv_file = 'portfolio.csv'
    portfolio_df = read_portfolio(csv_file)

    headers, data, total_market_value = calculate_value(portfolio_df)

    df_to_save = pd.DataFrame(data[:-1], columns=['timestamp', 'ISIN', 'quantity', 'quote',
                                                  'market_value'])  # Exclude the total row for saving
    save_tracking_data('tracking.csv', df_to_save)

    display_table(headers, data)


if __name__ == "__main__":
    main()
