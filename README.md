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

1. Place your ISIN codes in a CSV file named `isin_codes.csv` in the project directory.
2. Run the script:
   ```bash
   python etf_quote_tracking.py
   ```
3. The script will retrieve real-time quotes for the provided ISIN codes and save them to a CSV file named `etf_quote_tracking.csv`.

## CSV Format

The CSV file should have the following format:

```csv
Timestamp,ISIN,Value
2024-06-12 15:30:00,US1234567890,100.00
2024-06-12 15:31:00,US9876543210,200.00
```
