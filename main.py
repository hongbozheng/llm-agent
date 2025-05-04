import argparse
from llm_agent.config.config import AgentConfig
from llm_agent.config.env import load_api_keys
from llm_agent.core.prompt.prompt_router import PromptRouter
from llm_agent.core.logger import log


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="llm-agent", description="Financial Strategist Config",
    )
    parser.add_argument(
        "--llm",
        "-m",
        type=str,
        choices=["gpt-4o", "deepseek", "gemini"],
        default="gpt-4o",
        required=False,
        help="LLM backend (e.g., gpt-4o, gemini, deepseek)",
    )
    parser.add_argument(
        "--max_tokens",
        "-l",
        type=int,
        default=1024,
        required=False,
        help="Max tokens",
    )
    parser.add_argument(
        "--temperature",
        "-r",
        type=float,
        default=0.5,
        required=False,
        help="Temperature parameter (default: 0.5)",
    )
    parser.add_argument(
        "--top_p",
        "-p",
        type=float,
        default=0.8,
        required=False,
        help="Top-p nucleus sampling"
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=float,
        default=60,
        required=False,
        help="Timeout"
    )
    parser.add_argument(
        "--attempts",
        "-a",
        type=int,
        default=5,
        required=False,
        help="Max attempts"
    )
    parser.add_argument(
        "--prompt",
        "-q",
        type=str,
        default=None,
        required=False,
        help="Financial prompt"
    )

    return parser.parse_args()


def main():
    args = parse_cli()
    cfg = AgentConfig.load(cfg_path="llm_agent/config/cfg.yaml", args=args)
    load_api_keys(selected_llm=cfg.llm)
    cfg.print_summary()

    router = PromptRouter(cfg=cfg)

    log("[INFO] 🧠 Welcome to Financial Strategist!")
    user_prompt = args.prompt

    if not user_prompt:
        log("[INFO] 💬 Ask your financial question (e.g., crypto, real estate, stocks):")
        user_prompt = input("                      >>>>>> 👉 ").strip()

    if not user_prompt:
        log("[ERROR] ❌ Empty prompt. Please enter a question.")

        return

    try:
        result = router.route(user_prompt=user_prompt)

        print("[INFO] ✅ Strategy Recommendation:")
        print("-" * 60)
        for key, value in result.items():
            print(f"🔹 {key.capitalize()}:\n{value}\n")

    except Exception as e:
        log(f"[ERROR] ❌ Failed to process prompt: {e}")


if __name__ == "__main__":
    main()
