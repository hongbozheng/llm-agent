import argparse
from llm_agent.core.prompt import PromptRouter
from llm_agent.core.logger import log


def main():
    parser = argparse.ArgumentParser(
        description="Run the LLM money strategy agent")
    parser.add_argument("--prompt", type=str,
                        help="User prompt for strategy generation")

    args = parser.parse_args()
    prompt = args.prompt or input(">>> ")

    print("🧠 Welcome to Money-Maker LLM Agent!")
    print("💬 Type your question about making money (e.g., crypto, real estate, stocks):")

    try:
        user_prompt = input(">>> ").strip()
        if not user_prompt:
            print("⚠️ Empty prompt. Please enter a question.")
            return

        router = PromptRouter()
        result = router.route(user_prompt)

        print("\n✅ Strategy Recommendation:")
        print("-" * 60)
        for key, value in result.items():
            print(f"🔹 {key.capitalize()}:\n{value}\n")

    except Exception as e:
        log(f"❌ Failed to process prompt: {e}")
        print("Something went wrong. Please try again.")

if __name__ == "__main__":
    main()
