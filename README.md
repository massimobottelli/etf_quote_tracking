# ETF Quote Tracking

This script retrieves real-time quotes for ETFs based on their ISIN codes from the Borsa Italiana website.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/etf-quote-tracking.git
   ```
2. Navigate to the project directory:
   ```bash
   cd etf-quote-tracking
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Record your purchase date, type, ISIN codes and quantity in a CSV file named `portfolio.csv` in the project directory.

   ```csv
   purchase-date,type,ISIN,quantity
   2024-06-10 12:00:00,etf,IE00B5BMR087,45
   2024-06-10 12:00:00,etf,IE00B4K48X80,225
   2024-06-10 12:00:00,etf,IE00B4L5YX21,180
   2024-06-10 12:00:00,etc-etn,IE00B579F325,38
   ```
2. Run the script:
   ```bash
   python etf_quote_tracking.py
   ```
3. The script will retrieve real-time quotes for the provided ISIN codes and save them to a CSV file named `etf_quote_tracking.csv`.

## Output

The quote of the ETFs will be saved in a CSV file named `etf_quote_tracking.csv` with the following format:

```csv
Timestamp,ISIN,Value
2024-06-12 18:20:08,IE00B5BMR087,528.35
2024-06-12 18:20:09,IE00B4K48X80,80.37
2024-06-12 18:20:09,IE00B4L5YX21,50.22
2024-06-12 18:20:11,IE00B579F325,207.49
```
