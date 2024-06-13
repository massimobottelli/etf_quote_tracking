# ETF Quote Tracking

This script retrieves real-time quotes for ETFs based on their ISIN codes from the Borsa Italiana website.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/massimobottelli/etf-quote-tracking.git
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

1. Record your assets in a file named `portfolio.csv` in the project directory.

   ```csv
   purchase-date,type,ISIN,quantity
   2024-06-10,etf,IE00B5BMR087,45
   2024-06-10,etf,IE00B4K48X80,225
   2024-06-10,etf,IE00B4L5YX21,180
   2024-06-10,etc-etn,IE00B579F325,38
   ```
2. Run the script:
   ```bash
   python etf_quote_tracking.py
   ```
3. The script will retrieve real-time quotes for the provided ISIN codes, calculate the market value, display a table on screen and save it to a CSV file named `tracking.csv`.

## Output

The quote of the ETFs will be saved in a CSV file named `etf_quote_tracking.csv` with the following format:

```csv
timestamp,ISIN,quantity,quote,market_value
2024-06-12,IE00B5BMR087,45,528.35,23775.75
2024-06-12,IE00B4K48X80,225,80.37,18083.25
2024-06-12,IE00B4L5YX21,180,50.22,9039.6
2024-06-12,IE00B579F325,38,207.49,7884.62
```
