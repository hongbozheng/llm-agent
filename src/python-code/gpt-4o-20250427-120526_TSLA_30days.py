import yfinance as yf
import datetime
import talib
import numpy as np
import backtrader as bt
import pandas as pd

# Define the asset and timeframe
asset = 'TSLA'
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=30)

# Download data for the specified asset and timeframe
data = yf.download(asset, start=start_date, end=end_date, auto_adjust=False)

# Ensure the data has an 'Adj Close' column for further analysis
if 'Adj Close' not in data.columns:
    data['Adj Close'] = data['Close']  # Use 'Close' if 'Adj Close' is not available

# Display the data to confirm it has been loaded correctly
print(data.head())

# Check if there are enough data points
if len(data) < 20:
    raise ValueError("Not enough data to calculate the moving averages and RSI. Please adjust the date range.")

# Calculate simple moving averages for momentum strategy evaluation
data['SMA_10'] = talib.SMA(data['Adj Close'].values.flatten(), timeperiod=10)
data['SMA_20'] = talib.SMA(data['Adj Close'].values.flatten(), timeperiod=20)

# Calculate RSI for mean-reversion strategy evaluation
data['RSI'] = talib.RSI(data['Adj Close'].values.flatten(), timeperiod=14)

# Drop rows with NaN values after calculations
data.dropna(inplace=True)

# Determine the strategy type
if len(data) == 0:
    raise ValueError("No data left after dropping NaN values. Please check the data range and calculations.")

# Momentum Strategy: If the 10-day SMA is above the 20-day SMA, it indicates an uptrend
momentum_condition = data['SMA_10'].iloc[-1] > data['SMA_20'].iloc[-1]

# Mean-Reversion Strategy: If the RSI is below 30 or above 70, it indicates potential reversal
mean_reversion_condition = (data['RSI'].iloc[-1] < 30) or (data['RSI'].iloc[-1] > 70)

# Decide the strategy type based on conditions
if momentum_condition:
    strategy_type = 'momentum'
elif mean_reversion_condition:
    strategy_type = 'mean-reversion'
else:
    strategy_type = 'hold'

# Store the strategy type in a dictionary
strategy_info = {'strategy_type': strategy_type}

# Display the selected strategy type
print(strategy_info)

# Extend the lookback period for historical analysis
lookback_days = 90

# Update the start date to include the lookback period
start_date_lookback = end_date - datetime.timedelta(days=lookback_days)

# Download data for the extended lookback period
data_lookback = yf.download(asset, start=start_date_lookback, end=end_date, auto_adjust=False)

# Ensure the data has an 'Adj Close' column for further analysis
if 'Adj Close' not in data_lookback.columns:
    data_lookback['Adj Close'] = data_lookback['Close']  # Use 'Close' if 'Adj Close' is not available

# Display the data to confirm it has been loaded correctly
print(data_lookback.head())

# Calculate simple moving averages for momentum strategy evaluation
data_lookback['SMA_10'] = talib.SMA(data_lookback['Adj Close'].values.flatten(), timeperiod=10)
data_lookback['SMA_20'] = talib.SMA(data_lookback['Adj Close'].values.flatten(), timeperiod=20)

# Calculate RSI for mean-reversion strategy evaluation
data_lookback['RSI'] = talib.RSI(data_lookback['Adj Close'].values.flatten(), timeperiod=14)

# Drop rows with NaN values after calculations
data_lookback.dropna(inplace=True)

# Determine the strategy type using the lookback data
if len(data_lookback) == 0:
    raise ValueError("No data left after dropping NaN values. Please check the data range and calculations.")

# Momentum Strategy: If the 10-day SMA is above the 20-day SMA, it indicates an uptrend
momentum_condition_lookback = data_lookback['SMA_10'].iloc[-1] > data_lookback['SMA_20'].iloc[-1]

# Mean-Reversion Strategy: If the RSI is below 30 or above 70, it indicates potential reversal
mean_reversion_condition_lookback = (data_lookback['RSI'].iloc[-1] < 30) or (data_lookback['RSI'].iloc[-1] > 70)

# Decide the strategy type based on conditions
if momentum_condition_lookback:
    strategy_type_lookback = 'momentum'
elif mean_reversion_condition_lookback:
    strategy_type_lookback = 'mean-reversion'
else:
    strategy_type_lookback = 'hold'

# Store the strategy type in a dictionary
strategy_info_lookback = {'strategy_type': strategy_type_lookback}

# Display the selected strategy type based on the lookback period
print(strategy_info_lookback)

# Choose technical indicators based on strategy type
if strategy_type_lookback == 'momentum':
    # Use Moving Averages and MACD for momentum strategy
    data_lookback['MACD'], data_lookback['MACD_signal'], data_lookback['MACD_hist'] = talib.MACD(
        data_lookback['Adj Close'].values.flatten(), fastperiod=12, slowperiod=26, signalperiod=9)
elif strategy_type_lookback == 'mean-reversion':
    # Use RSI and Bollinger Bands for mean-reversion strategy
    data_lookback['upper_band'], data_lookback['middle_band'], data_lookback['lower_band'] = talib.BBANDS(
        data_lookback['Adj Close'].values.flatten(), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

# Display the data with chosen indicators
print(data_lookback.tail())

# Define a function to calculate Sharpe Ratio
def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    excess_returns = returns - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns)

# Define a function to calculate Max Drawdown
def calculate_max_drawdown(prices):
    cumulative_returns = (1 + prices.pct_change()).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()
    return max_drawdown

# Define a function to calculate Return on Investment (ROI)
def calculate_roi(start_price, end_price):
    return (end_price - start_price) / start_price

# Calculate daily returns
data_lookback['daily_returns'] = data_lookback['Adj Close'].pct_change()

# Calculate Sharpe Ratio for the lookback period
sharpe_ratio = calculate_sharpe_ratio(data_lookback['daily_returns'].dropna())

# Calculate Max Drawdown for the lookback period
max_drawdown = calculate_max_drawdown(data_lookback['Adj Close'])

# Calculate ROI for the lookback period
roi = calculate_roi(data_lookback['Adj Close'].iloc[0], data_lookback['Adj Close'].iloc[-1])

# Store evaluation metrics in a dictionary
evaluation_metrics = {
    'Sharpe Ratio': sharpe_ratio,
    'Max Drawdown': max_drawdown,
    'ROI': roi
}

# Display the evaluation metrics
print(evaluation_metrics)

# Create a custom strategy class
class TSLA_Strategy(bt.Strategy):
    params = (
        ('sma1', 10),
        ('sma2', 20),
        ('rsi_period', 14),
        ('rsi_upper', 70),
        ('rsi_lower', 30),
    )
    
    def __init__(self):
        # Define indicators
        self.sma1 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma1)
        self.sma2 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma2)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        
    def next(self):
        # Momentum strategy logic
        if self.sma1 > self.sma2:
            if not self.position:
                self.buy()
        elif self.rsi > self.params.rsi_upper:
            if self.position:
                self.sell()
        elif self.rsi < self.params.rsi_lower:
            if not self.position:
                self.buy()

# Set up the backtesting environment
cerebro = bt.Cerebro()
cerebro.addstrategy(TSLA_Strategy)

# Convert data to a format suitable for backtrader
# Flatten MultiIndex if present and convert to lowercase
data_lookback.columns = ['_'.join(col).lower() if isinstance(col, tuple) else col.lower() for col in data_lookback.columns]
data_bt = bt.feeds.PandasData(dataname=data_lookback)

# Add data to cerebro
cerebro.adddata(data_bt)

# Set initial cash
cerebro.broker.setcash(10000)

# Set commission
cerebro.broker.setcommission(commission=0.001)

# Run the backtest
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Paper trading setup (mock implementation, adjust according to actual paper trading platform)
def paper_trade(strategy_type):
    if strategy_type == 'momentum':
        print("Executing paper trades for momentum strategy...")
    elif strategy_type == 'mean-reversion':
        print("Executing paper trades for mean-reversion strategy...")
    else:
        print("Holding position as per strategy...")

# Execute paper trading
paper_trade(strategy_type_lookback)

# Store the strategy information in a dictionary
strategy_info = {
    'strategy_type': strategy_type_lookback,
    'assets': asset,
    'lookback_days': lookback_days,
    'indicators': ['SMA_10', 'SMA_20', 'RSI', 'MACD' if strategy_type_lookback == 'momentum' else 'Bollinger Bands'],
    'evaluation_metrics': evaluation_metrics
}

# Display the strategy information
print(strategy_info)