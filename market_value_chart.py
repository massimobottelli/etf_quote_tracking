import pandas as pd
import matplotlib.pyplot as plt
import os


def read_report(file_path):
    if os.path.isfile(file_path):
        return pd.read_csv(file_path)
    else:
        print("File not found.")
        return pd.DataFrame()


def calculate_daily_totals(report_df):
    # Group by the 'timestamp' and sum the 'market_value'
    daily_totals = report_df.groupby('timestamp')['market_value'].sum().reset_index()
    return daily_totals


def on_key(event):
    if event.key == 'q':
        plt.close()


def plot_price_chart(daily_totals):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(daily_totals['timestamp'], daily_totals['market_value'], marker='o', linestyle='-', color='skyblue')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Market Value')
    ax.set_title('Daily Total Market Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()


def main():
    csv_file = 'tracking.csv'
    report_df = read_report(csv_file)

    if not report_df.empty:
        daily_totals = calculate_daily_totals(report_df)
        plot_price_chart(daily_totals)


if __name__ == "__main__":
    main()
