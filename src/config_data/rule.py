def add_prompt():
    return "avoid no import error"


COMMON_CODE_ERRORS = [
    {
        "error": "'Adj Close'",
        "cause": "yfinance may return data without an 'Adj Close' column, or the column might be labeled 'Close'.",
        "fix": "After downloading data, check and rename columns: data.rename(columns={'Close': 'Adj Close'}, inplace=True)"
    },
    # {
    #     "error": "name 'data' is not defined",
    #     "cause": "Data was not loaded in previous steps or not shared across steps.",
    #     "fix": "Always start by loading data (e.g., using yfinance) and ensure it's assigned to a variable called 'data'."
    # },
    # {
    #     "error": "name 'strategy_type' is not defined",
    #     "cause": "strategy_type is computed in a previous step but not saved globally.",
    #     "fix": "Store it in a shared dictionary: strategy_info = {'strategy_type': strategy_type}."
    # },
    # {
    #     "error": "name 'np' is not defined",
    #     "cause": "You are using numpy without importing it.",
    #     "fix": "Include import numpy as np at the top of the code."
    # },
    # {
    #     "error": "name 'plt' is not defined",
    #     "cause": "You are plotting with matplotlib but didn't import it.",
    #     "fix": "Include import matplotlib.pyplot as plt before using it."
    # },
    # {
    #     "error": "ModuleNotFoundError: No module named 'talib'",
    #     "cause": "TA-Lib is not installed in your Python environment.",
    #     "fix": "Install with pip install TA-Lib, or switch to pandas-based indicator implementations."
    # }
    {
    "error": "TypeError: Argument 'real' has incorrect type (expected numpy.ndarray, got DataFrame)",
    "cause": "TA-Lib functions expect NumPy arrays, not pandas Series or DataFrames.",
    "fix": "Use .values to convert: talib.SMA(data['Adj Close'].values, ...). Optionally fill NaN with .fillna(method='ffill')."
    }

]

def get_rule_prompt_text():
    return "\n".join([
        f"- Error: {rule['error']}\n  Cause: {rule['cause']}\n  Fix: {rule['fix']}"
        for rule in COMMON_CODE_ERRORS
    ])
