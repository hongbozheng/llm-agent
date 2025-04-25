# LLM-Powered Quant Developer Assistant

## 🧠 Project Overview

This project is a fully autonomous AI-powered Quant Developer Assistant. It enables users—such as retail investors, quant researchers, and finance students—to generate, execute, and evaluate algorithmic trading strategies by simply asking natural language questions.

> Example:
> **"What's a good momentum strategy for TSLA over the past 3 months?"**

The system returns a step-by-step strategy plan, generates code, executes it, performs backtests on historical data, and outputs a full evaluation summary.

---

## 🚀 Key Features

### ✅ GPT-Orchestrated Strategy Planning
- LLM generates a JSON plan detailing asset, indicators, timeframe, evaluation metrics, and task sequence

### ✅ Code Generation & Automated Execution
- Each step is translated into Python code and auto-executed
- Failures trigger a threaded auto-fix system with up to 3 retries

### ✅ Strategy Evaluation & Backtesting
- Historical stock data is used for realistic backtesting
- Calculates Sharpe Ratio, Max Drawdown, Annualized Return, Win Rate, and more

---

## 🧱 Technology Stack

- **LLMs**: OpenAI GPT-4o, DeepSeek-Chat, Gemini Pro
- **Backend**: Python, Pandas
- **Execution Engine**: `exec()` with error recovery + retry logic
- **Data**: Yahoo Finance API
- **Frontend (optional)**: Flask

---

## 📂 Project Structure
```
src/
├── pipeline.py            # CLI entrypoint: generate → execute → compare
├── step_generator.py      # Uses LLM to generate step plans
├── step_executor.py       # Executes and evaluates each step
├── autofix.py             # Threaded error handler + code fixer
├── config_data/
│   └── rule.py            # Contains common error rules for LLM prompting
summaries/                 # Final results for each strategy
outputs/                   # Raw step outputs

```              
## 🚀 How to Run

### Install dependencies

``` 
pip install -r requirements.txt 
```

### Generate + Execute Strategy Plan

``` python
python3 src/pipeline.py \
  --step full_pipeline \
  --llm_model gpt-4o \
  --question "What's a good strategy for MAXN in the next 30 days?" 
  ``` 
## 👥 Team Members

Hanqi Mao – hanqim2@illinois.edu

Hanxi Fang – hanxif2@illinois.edu

Hongbo Zheng – hongboz2@illinois.edu

Dadong Peng – dadongp2@illinois.edu