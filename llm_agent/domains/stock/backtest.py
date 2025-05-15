from llm_agent.config import AgentConfig
from llm_agent.io.conversation_logger import ConversationLogger
from llm_agent.io.writer import Writer
from typing import Optional

from llm_agent.core.llm_backends import LLMClient
from llm_agent.core.utils.parser import extract_block
from llm_agent.domains.stock.knowledge.prompt_helpers import get_coding_advice
from llm_agent.logger.logger import log_error, log_info


def backtest_strategy(
        cfg: AgentConfig,
        strategy: dict,
        logger: Optional[ConversationLogger] = None,
        writer: Optional[Writer] = None,
) -> str:
    """Simulate this strategy on dummy historical data."""
    # Placeholder: replace with real OHLCV crypto data engine

    system_prompt = (
        "You are a professional quant developer at a financial technology company. "
        "You write backtest scripts in Python that simulate trading strategies using only open-source tools. "
        "You are very strict about:\n"
        "- Using only `pandas`, `numpy`, `yfinance`\n"
        "- Writing clean, minimal, executable code\n"
        "- Avoiding any external frameworks (like Backtrader or Zipline)\n"
        "- Printing backtest results in JSON format (using `json.dumps`)\n"
        "- Using clear variable names and simple performance metrics\n"
        "- Following best engineering practices with complete scripts\n\n"
    )

    system_prompt += get_coding_advice()

    user_prompt = f"""
Using the strategy details below, write a complete backtest script in Python:

Strategy:
- Asset: {strategy.get('asset')}
- Entry Logic: {strategy.get('entry-logic')}
- Exit Logic: {strategy.get('exit-logic')}
- Holding Period: {strategy.get('holding-period')}
- Risk Management Notes: {strategy.get('risk-management')}

Your script must:
1. Download 90 days of 1D OHLCV data using `yfinance`
2. Use pandas to implement the entry/exit logic (signal-based)
3. Assume $100,000 capital per trade
4. Calculate and print the following metrics:
   - Total trades
   - Win rate
   - Net profit percentage
   - Max drawdown percentage
   - Sharpe ratio (daily returns)
5. Print a JSON summary using `print(json.dumps(summary))`
6. Wrap the whole script in a single code block like:
```python
# complete script here
```
""".strip()

    response = LLMClient.call(
        llm=cfg.llm,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=cfg.max_tokens,
        temperature=cfg.temperature,
        top_p=cfg.top_p,
    )

    try:
        code = extract_block(text=response, language="python")
    except Exception as e:
        log_error(f"❌ Failed to parse LLM response into Python")
        log_error(f"❌ Exception `{e}`")
        raise

    if logger is not None:
        logger.log_system(prompt=system_prompt)
        logger.log_user(prompt=user_prompt)
        logger.log_llm(response=code)

    if writer is not None:
        writer.save_code(code=code, name="backtest")
        log_info(f" 💾 Save strategy to `{writer.get_path()}/backtest.py`")

    return code
