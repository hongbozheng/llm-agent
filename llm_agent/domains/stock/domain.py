from llm_agent.config import AgentConfig
from llm_agent.core.prompt.schema import Prompt
from typing import Optional

from llm_agent.core.code_executor.executor import CodeExecutor
from llm_agent.domains.base import Domain
from llm_agent.domains.stock.backtest import backtest_strategy
from llm_agent.domains.stock.evaluator import evaluate_strategy
from llm_agent.domains.stock.strategy import generate_strategy
from llm_agent.io.conversation_logger import ConversationLogger
from llm_agent.io.writer import Writer
from llm_agent.logger.logger import log_info


class Stock(Domain):
    def __init__(self, cfg: AgentConfig):
        super().__init__(cfg=cfg)

    def process_prompt(
            self,
            prompt: Prompt,
            logger: Optional[ConversationLogger] = None,
            writer: Optional[Writer] = None,
    ) -> dict:
        strategy = generate_strategy(
            cfg=self.cfg, prompt=prompt, logger=logger, writer=writer
        )

        code = backtest_strategy(
            cfg=self.cfg, strategy=strategy, logger=logger, writer=writer
        )

        executor = CodeExecutor(cfg=self.cfg)
        executor.execute(
            file_path=writer.get_path() / "backtest.py", logger=logger
        )

        # evaluation = evaluate_strategy(
        #     strategy=strategy,
        #     file_path=file_path,
        # )

        return {
            "domain": "crypto",
            "intent": prompt.intent,
            "strategy": strategy,
            "backtest": code,
            "evaluation": evaluation,
        }
