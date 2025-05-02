from typing import Dict

from ...core.schema import Prompt
from ..base import Domain
from .backtest import backtest_strategy
from .evaluator import evaluate_strategy
from .strategy import generate_strategy


class Stock(Domain):
    def handle_prompt(self, prompt: Prompt) -> Dict:
        strategy = generate_strategy(prompt)
        backtest_results = backtest_strategy(strategy)
        evaluation = evaluate_strategy(backtest_results)

        return {
            "domain": "crypto",
            "intent": prompt.intent,
            "strategy": strategy,
            "backtest": backtest_results,
            "evaluation": evaluation,
        }
