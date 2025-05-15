import argparse
from datetime import datetime
from llm_agent.config.config import AgentConfig
from llm_agent.config.env import load_api_keys
from llm_agent.core.prompt.prompt_router import PromptRouter
from llm_agent.io.conversation_logger import ConversationLogger
from llm_agent.io.writer import Writer
from llm_agent.logger.logger import log_error, log_info
from pathlib import Path


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="llm-agent", description="Financial Strategist Config",
    )
    parser.add_argument(
        "--llm",
        type=str,
        choices=["gpt-4o", "deepseek", "gemini"],
        default=None,  # "gpt-4o"
        required=False,
        help="LLM backend (e.g., gpt-4o, gemini, deepseek)",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=None,  # 1024
        required=False,
        help="Max tokens",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,  # 0.50
        required=False,
        help="Temperature parameter (default: 0.5)",
    )
    parser.add_argument(
        "--top_p",
        type=float,
        default=None,  # 0.80
        required=False,
        help="Top-p nucleus sampling",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,  # 60
        required=False,
        help="Timeout",
    )
    parser.add_argument(
        "--attempts",
        type=int,
        default=None,  # 5
        required=False,
        help="Max attempts",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        required=False,
        help="Financial prompt",
    )
    parser.add_argument(
        "--log_level",
        type=str,
        choices=["all", "trace", "debug", "info", "warn", "error", "fatal", "off"],
        default=None,  # "info"
        required=False,
        help="Log level",
    )
    parser.add_argument(
        "--log",
        type=bool,
        default=None,  # true
        required=False,
        help="Log flag",
    )
    parser.add_argument(
        "--save",
        type=bool,
        default=None,  # true
        required=False,
        help="Save output",
    )

    return parser.parse_args()


def main():
    args = parse_cli()
    cfg = AgentConfig.load(cfg_path="llm_agent/config/cfg.yaml", args=args)
    load_api_keys(selected_llm=cfg.llm)
    cfg.print_summary()

    router = PromptRouter(cfg=cfg)
    logger = None
    writer = None

    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    if cfg.log:
        logger = ConversationLogger(path=Path("output") / timestamp)
    if cfg.save:
        writer = Writer(path=Path("output") / timestamp)

    log_info(" 🧠 Welcome to Financial Strategist!")
    user_prompt = args.prompt

    if not user_prompt:
        log_info(" 💬 Ask your financial question (e.g., crypto, real estate, stocks):")
        user_prompt = input("                      >>>>>>  👉 ").strip()

    if not user_prompt:
        log_error("❌ Empty prompt. Please enter a question.")

        return

    try:
        result = router.route(
            user_prompt=user_prompt, logger=logger, writer=writer,
        )

        print("[INFO] ✅ Strategy Recommendation:")
        print("-" * 60)
        for key, value in result.items():
            print(f"🔹 {key.capitalize()}:\n{value}\n")

    except Exception as e:
        log_info(f" ❌ Failed to process prompt: {e}")


if __name__ == "__main__":
    main()
