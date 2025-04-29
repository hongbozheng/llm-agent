from typing import Dict


def backtest_strategy(strategy: Dict) -> Dict:
    """Simulate this strategy on dummy historical data."""
    # Placeholder: replace with real OHLCV crypto data engine
    return {
        "trades": 12,
        "win_rate": 0.67,
        "profit": 1234.56,
        "max_drawdown": -8.2,
        "sharpe_ratio": 1.25,
    }
