import yfinance as yf
import json

def get_ticker_data(ticker_symbol: str):
    """Fetch and return news data for the given ticker symbol."""
    dat = yf.Ticker(ticker_symbol)
    news = dat.get_sec_filings()
    return news



def main():
    ticker_symbol = "MSTR"
    refined_data = get_ticker_data(ticker_symbol)
    print(refined_data)

if __name__ == "__main__":
    main()