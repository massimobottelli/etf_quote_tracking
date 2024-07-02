import configparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tabulate import tabulate
from tqdm import tqdm
import os
import telegram
import asyncio

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
        df = pd.read_csv(file_path)
        df["purchase_value"] = df["quantity"] * df["purchase_price"]
        total_purchase_value = df["purchase_value"].sum()
        return df, total_purchase_value
    else:
        df = pd.DataFrame(columns=["timestamp", "type", "ISIN", "quantity", "accrual", "purchase_price", "purchase_value"])
        return df, 0


def save_tracking_data(file_path, data):
    if os.path.isfile(file_path):
        existing_data = pd.read_csv(file_path)
        existing_timestamps = existing_data['timestamp'].unique()
        new_timestamp = data['timestamp'].iloc[0]

        if new_timestamp in existing_timestamps:
            print("Tracking for today already exists. Skipping save.")
            return

    data.to_csv(file_path, mode='a', index=False, header=not os.path.isfile(file_path))


def save_market_value(file_path, date, value):
    if os.path.isfile(file_path):
        existing_data = pd.read_csv(file_path)
        if date in existing_data['date'].values:
            print(f"Market for today already exists. Skipping save.")
            return

    new_data = pd.DataFrame({'date': [date], 'market_value': [value]})
    new_data.to_csv(file_path, mode='a', index=False, header=not os.path.isfile(file_path))


def calculate_value(portfolio_df, purchase_value):
    table_headers = ["Timestamp", "ISIN", "Quantity", "Quote", "Market Value"]
    table_data = []
    total_market_value = 0

    for index, row in tqdm(portfolio_df.iterrows(), desc="Progress", total=len(portfolio_df),
                           bar_format="{desc}: {percentage:3.0f}%|{bar}|"):
        type = row['type']
        isin = row['ISIN']
        quantity = row['quantity']
        accrual = row['accrual']

        quote = fetch_realtime_quote(isin, type)
        if quote is None:
            continue

        market_value = round(quote * quantity + accrual, 2)
        total_market_value += market_value

        timestamp = datetime.now().strftime('%Y-%m-%d')
        table_data.append([timestamp, isin, quantity, quote, market_value])

    # Add a last row for total market value to the table data
    table_data.append(['', '', '', 'Total Market Value:', round(total_market_value, 2)])
    table_data.append(['', '', '', 'Purchase Value:', round(purchase_value, 2)])

    return table_headers, table_data, round(total_market_value, 2)


def display_table(headers, data):
    print(tabulate(data, headers=headers, tablefmt="grid"))


def read_telegram_config(file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    token = config['Telegram']['token']
    chat_id = config['Telegram']['chat_id']
    return token, chat_id


async def send_telegram_message(value):
    token, chat_id = read_telegram_config()
    timestamp = datetime.now().strftime('%d/%m/%Y')
    formatted_value = f"{value:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')
    message = f"{timestamp}: {formatted_value} €"

    bot = telegram.Bot(token)
    await bot.send_message(chat_id=chat_id, text=message)

async def main():
    print("\nETF Quote Tracking"
          "\n------------------")
    print("Retrieving quotes for the listed ETFs...")

    csv_file = 'portfolio.csv'
    portfolio_df, purchase_value = read_portfolio(csv_file)

    headers, data, total_market_value = calculate_value(portfolio_df, purchase_value)

    df_to_save = pd.DataFrame(data[:-2], columns=['timestamp', 'ISIN', 'quantity', 'quote',
                                                  'market_value'])  # Exclude the total row
    save_tracking_data('tracking.csv', df_to_save)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    save_market_value('market_value.csv', timestamp, total_market_value)

    display_table(headers, data)

    await send_telegram_message(total_market_value)


if __name__ == "__main__":
    asyncio.run(main())
