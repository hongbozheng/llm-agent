from typing import Dict, List, Union

import os
from datetime import datetime

import config
import enum
from datetime import datetime


class LogLevel(enum.Enum):
    ALL = 6
    TRACE = 5
    DEBUG = 4
    INFO = 3
    WARN = 2
    ERROR = 1
    FATAL = 0
    OFF = -1

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def timestamp() -> str:
    time = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
    return time


def log_trace(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.TRACE:
        ts = timestamp()
        print(f"[{ts}] [TRACE] ", end="")
        print(*args, **kwargs)
    return


def log_debug(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.DEBUG:
        ts = timestamp()
        print(f"[{ts}] [DEBUG] ", end="")
        print(*args, **kwargs)
    return


def log_info(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.INFO:
        ts = timestamp()
        print(f"[{ts}] [INFO]  ", end="")
        print(*args, **kwargs)
    return


def log_warn(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.WARN:
        ts = timestamp()
        print(f"[{ts}] [WARN]  ", end="")
        print(*args, **kwargs)
    return


def log_error(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.ERROR:
        ts = timestamp()
        print(f"[{ts}] [ERROR] ", end="")
        print(*args, **kwargs)
    return


def log_fatal(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.FATAL:
        ts = timestamp()
        print(f"[{ts}] [FATAL] ", end="")
        print(*args, **kwargs)
    return


def log_trace_raw(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.TRACE:
        ts = timestamp()
        print(f"[{ts}] ", end="")
        print(*args, **kwargs)
    return


def log_debug_raw(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.DEBUG:
        ts = timestamp()
        print(f"[{ts}] ", end="")
        print(*args, **kwargs)
    return


def log_info_raw(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.INFO:
        ts = timestamp()
        print(f"[{ts}] ", end="")
        print(*args, **kwargs)
    return


def log_warn_raw(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.WARN:
        ts = timestamp()
        print(f"[{ts}] ", end="")
        print(*args, **kwargs)
    return


def log_error_raw(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.ERROR:
        ts = timestamp()
        print(f"[{ts}] ", end="")
        print(*args, **kwargs)
    return


def log_fatal_raw(*args, **kwargs) -> None:
    if config.LOG_LEVEL >= LogLevel.FATAL:
        ts = timestamp()
        print(f"[{ts}] ", end="")
        print(*args, **kwargs)
    return


def log(msg: str) -> None:
    """Prints a message with the current datetime prepended."""
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{curr_time}] {msg}")

    return


def log_usr_input(llm: str, prompt: str, file_path: str) -> None:
    log("=" * 75)
    log("📘 Input Arguments")
    log("-" * 75)
    log(f"🤖 LLM      {llm}")
    if prompt:
        log(f"💬 Prompt   {prompt}")
    else:
        log(f"📂️ Strategy {file_path}")
    log("=" * 75)

    return


def log_strategy(strategy: str) -> None:
    log("=" * 75)
    log("🧠 Strategy Plan")
    log("-" * 75)
    for line in strategy.splitlines():
        log(line)
    log("=" * 75)

    return


def log_prompt(sys_prompt: str, usr_prompt: str) -> None:
    log("=" * 75)
    log("🛠️ System Prompt")
    log("-" * 75)
    for line in sys_prompt.splitlines():
        log(line)
    log("~" * 75)
    log("💬 User Prompt")
    log("-" * 75)
    for line in usr_prompt.splitlines():
        log(line)
    log("=" * 75)

    return


def log_step(i: int, step: str) -> None:
    log("=" * 75)
    log(f"🛠️ Executing Step {i} {step}")
    log("-" * 75)

    return

def log_output(output: str) -> None:
    for line in output.splitlines():
        log(line)

def log_convo(
        convo: Dict[str, Union[str, Dict[str, str], List[Dict[str, Union[str, List[Dict[str, str]]]]]]],
        time: str
) -> None:
    c = f"""
# Conversation Between User and {convo['llm']}

---

## Configuration

- **LLM**: {convo['llm']}
- **Temperature**: {convo['temp']}
- **Timeout**: {convo['timeout']}
- **Max Attempts**: {convo['max_att']}

---

## Generate Strategy

#### System Prompt

```
{convo['generate-strategy']['sys-prompt']}
```

#### User Prompt

```
{convo['generate-strategy']['usr-prompt']}
```

#### LLM Response

```
{convo['generate-strategy']['llm-response']}
```

---

## Execute Strategy
"""

    for i in range(len(convo['exec-strategy'])):
        step = convo['exec-strategy'][i]
        c += f"""
\n### Step {i} {step['action']}

#### System Prompt

```
{step['sys-prompt']}
```

#### User Prompt

```
{step['usr-prompt']}
```

#### LLM Response

```
{step['llm-response']}
```
"""

        for k in range(len(step['code-convo'])):
            s = step['code-convo'][k]
            c += f"""
\n### Attempt to Fix Python Script

#### System Prompt
```
{s['sys-prompt']}
```

#### User Prompt
```
{s['usr-prompt']}
```

#### LLM Response
```
{s['llm-response']}
```
"""

    os.makedirs("conversation", exist_ok=True)
    file_path = os.path.join("conversation", f"{time}.md")
    f = open(file_path, 'w')
    f.write(c.strip())
    f.close()

    return
