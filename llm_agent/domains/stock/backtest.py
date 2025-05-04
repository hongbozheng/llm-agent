import json
import os
from llm_agent.config import AgentConfig
from llm_agent.core.code_executor.executor import CodeExecutor
from llm_agent.core.llm_backends import LLMClient
from llm_agent.core.utils.parser import extract_block


def backtest_strategy(cfg: AgentConfig, strategy: dict) -> dict:
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
        "- Following best engineering practices with complete scripts"
    )

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

    code = extract_block(text=response, language="python")

    os.makedirs("output", exist_ok=True)
    file_path = "output/backtest.py"
    with open(file_path, mode='w') as f:
        f.write(code)

    executor = CodeExecutor(cfg=cfg)
    executor.execute(file_path=file_path)

    print(response)

    return response



