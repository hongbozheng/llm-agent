from datetime import datetime


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
