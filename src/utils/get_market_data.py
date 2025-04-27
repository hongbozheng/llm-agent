import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def get_historical_data(
    ticker: str,
    period: str = "6mo",
    interval: str = "1d",
    auto_adjust: bool = True
) -> pd.DataFrame:
    """
    Get historical market data for a ticker
    
    Args:
        ticker: Stock symbol (e.g. "TSLA")
        period: Time period (valid options: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)
        interval: Data interval (1d, 1wk, 1mo, etc.)
        auto_adjust: Adjust for corporate actions (splits, dividends)
    
    Returns:
        Pandas DataFrame with historical data
    """
    try:
        data = yf.Ticker(ticker).history(
            period=period,
            interval=interval,
            auto_adjust=auto_adjust
        )
        
        # Clean up the data
        data = data[["Open", "High", "Low", "Close", "Volume"]]
        data.index.name = "Date"
        
        print(f"✅ Successfully downloaded {len(data)} records for {ticker}")
        return data
    
    except Exception as e:
        print(f"❌ Failed to download data for {ticker}: {str(e)}")
        return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    # Get 6 months of daily data
   
    tsla_data = get_historical_data("TSLA", period="2y") #options “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
    
    # Save to CSV if data was retrieved
    if not tsla_data.empty:
        # filename = f"TSLA_historical_{datetime.now().strftime('%Y%m%d')}.csv"
        filename = f"SPS_historical_{datetime.now().strftime('%Y%m%d')}.csv"
        tsla_data.to_csv(filename)
        print(f"📊 Data saved to {filename}")
        
        # Show sample
        print("\nSample data:")
        print(tsla_data.tail())
    else:
        print("nothing loaded")