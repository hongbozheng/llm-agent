from typing import Dict


def evaluate_strategy(backtest_results: Dict) -> Dict:
    sharpe = backtest_results.get("sharpe_ratio", 0)
    drawdown = backtest_results.get("max_drawdown", 0)

    if sharpe > 1.2 and drawdown > -10:
        grade = "A"
    elif sharpe > 0.8:
        grade = "B"
    else:
        grade = "C"

    return {
        "grade": grade,
        "recommendation": "Consider reducing position size during volatile periods."
    }
