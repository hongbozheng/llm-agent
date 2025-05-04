from llm_agent.config import AgentConfig
from llm_agent.core.prompt.schema import Prompt
from llm_agent.domains.base import Domain
from llm_agent.domains.stock.backtest import backtest_strategy
from llm_agent.domains.stock.evaluator import evaluate_strategy
from llm_agent.domains.stock.strategy import generate_strategy


class Stock(Domain):
    def __init__(self, cfg: AgentConfig):
        super().__init__(cfg=cfg)

    def handle_prompt(self, prompt: Prompt) -> dict:
        strategy = generate_strategy(cfg=self.cfg, prompt=prompt)
        backtest_results = backtest_strategy(cfg=self.cfg, strategy=strategy)
        evaluation = evaluate_strategy(backtest_results)

        return {
            "domain": "crypto",
            "intent": prompt.intent,
            "strategy": strategy,
            "backtest": backtest_results,
            "evaluation": evaluation,
        }
