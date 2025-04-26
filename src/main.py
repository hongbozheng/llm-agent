import argparse
import json
import os
from datetime import datetime
from logger import log, log_strategy, log_usr_input
from step_executor import exec_strategy
from step_generator import generate_strategy
from utils import check_api_keys, sanitize_for_filename


def main(args):
    llm = args.llm
    temp = args.temperature
    timeout = args.timeout
    max_att = args.attempt
    prompt = args.prompt
    file_path = args.file_path

    if (file_path is None and prompt is None) or (file_path and prompt):
        log(f"❌ [ERROR] Please specify exactly one of --file_path or --question")
        exit(1)

    log_usr_input(llm, prompt, file_path)
    check_api_keys(llm)

    os.makedirs("strategy", exist_ok=True)

    if prompt is not None:
        strategy = generate_strategy(llm, prompt, temp)

        strategy = json.dumps(strategy, indent=2)

        p = sanitize_for_filename(prompt)
        filename = f"strategy-{llm}-{p}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        file_path = os.path.join("strategy", filename)
        f = open(file_path, 'w')
        f.write(strategy)
        f.close()

    f = open(file_path, 'r')
    strategy = json.load(f)
    f.close()
    log_strategy(json.dumps(strategy, indent=2))

    exec_strategy(llm, temp, timeout, max_att, file_path)

    # elif args.step == "compare_agents":
    #     summary_paths = []
    #     for agent_model in ["gpt-4o", "deepseek-chat"]:
    #         print(f"\n=== Running strategy for: {agent_model} ===")
    #         result = ask_for_strategy(args.question, llm=llm)
    #         time.sleep(10)
    #         if result:
    #             pretty_json = json.dumps(result, indent=2)
    #             safe_prompt = sanitize_prompt_for_filename(args.question)
    #             filename = f"strategy_plan_{agent_model}_{safe_prompt}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    #             plan_path = os.path.join("outputs", filename)
    #
    #             os.makedirs("outputs", exist_ok=True)
    #             with open(plan_path, "w") as f:
    #                 f.write(pretty_json)
    #             print(f"[INFO] Saved strategy plan to: {plan_path}")
    #
    #             # run_strategy_steps(plan_path, agent_model)
    #
    #             # # Assume summary saving will be added to run_strategy_steps()
    #             # summary_path = plan_path.replace("outputs", "summaries").replace("strategy_plan", "summary")
    #             # summary_paths.append(summary_path)
    #
    #             summary_path = run_strategy_steps(plan_path, agent_model)
    #             summary_paths.append(summary_path)
    #
    #     # Step 3: Use GPT-4o to compare
    #     if len(summary_paths) == 2:
    #
    #         compare_strategy_summaries(summary_paths[0], summary_paths[1], args.question)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LLM Agent for High-Frequency Trading (HFT) Strategies"
    )
    parser.add_argument(
        "--llm",
        "-m",
        type=str,
        choices=["gpt-4o", "deepseek", "gemini"],
        required=True,
        help="The LLM to use.",
    )
    parser.add_argument(
        "--temperature",
        "-r",
        type=float,
        default=0.5,
        required=False,
        help="LLM response randomness.",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=60,
        required=False,
        help="Timeout for code execution.",
    )
    parser.add_argument(
        "--attempt",
        "-a",
        type=int,
        default=5,
        required=False,
        help="Number of attempts to fix the code.",
    )
    parser.add_argument(
        "--prompt",
        "-p",
        type=str,
        default=None,
        required=False,
        help="The finance prompt to generate a strategy plan for."
    )
    parser.add_argument(
        "--file_path",
        "-f",
        type=str,
        default=None,
        required=False,
        help="Strategy filepath.",
    )
    args = parser.parse_args()
    main(args)
