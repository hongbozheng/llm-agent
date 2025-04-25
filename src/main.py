import argparse
import json
import openai
import os
import time

from dotenv import load_dotenv
from logger import log, log_usr_input, log_strategy
from step_generator import generate_strategy
# from step_executor import ask_gpt_to_execute_step_with_files
from step_executor import run_strategy_steps
from step_executor import compare_strategy_summaries
from datetime import datetime
from utils import check_api_keys, sanitize_for_filename


def main(args):
    llm = args.llm
    prompt = args.prompt
    file_path = args.file_path

    if (file_path is None and prompt is None) or (file_path and prompt):
        log(f"❌ [ERROR] Please specify exactly one of --file_path or --question")
        exit(1)

    log_usr_input(llm, prompt, file_path)
    check_api_keys(llm)

    os.makedirs("strategy", exist_ok=True)

    if prompt is not None:
        strategy = generate_strategy(llm, prompt)
        if strategy is None:
            exit(1)

        strategy = json.dumps(strategy, indent=2)

        p = sanitize_for_filename(prompt)
        filename = f"strategy_{llm}_{p}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path = os.path.join("strategy", filename)
        file = open(file_path, "w")
        file.write(strategy)
        file.close()

    file = open(file_path, 'r')
    strategy = json.load(file)
    file.close()
    log_strategy(json.dumps(strategy, indent=2))

    exit(0)
    run_strategy_steps(file_path, args.llm_model)

    # if step == "generate_step":
    #     result = ask_for_strategy(args.question)
    #     time.sleep(10)
    #     if result:
    #         print("[INFO] Strategy Plan:")
    #         pretty_json = json.dumps(result, indent=2)
    #         print(pretty_json)
    #
    #         safe_prompt = sanitize_prompt_for_filename(args.question)
    #         filename = f"strategy_plan_{safe_prompt}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    #         save_path = os.path.join("outputs", filename)
    #
    #         # Ensure the output folder exists
    #         os.makedirs("outputs", exist_ok=True)
    #
    #         with open(save_path, "w") as f:
    #             f.write(pretty_json)
    #
    #         print(f"[INFO] Saved strategy plan to: {save_path}")
    # elif step == "full_pipeline":
    #     # procedure 1 : generate step
    #     strategy = ask_for_strategy(question, llm)
    #
    #     prompt = sanitize_for_filename(question)
    #     filename = f"strategy_{llm}_{prompt}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    #     save_path = os.path.join("outputs", filename)
    #
    #     # Ensure the output folder exists
    #     os.makedirs("outputs", exist_ok=True)
    #
    #     with open(save_path, "w") as f:
    #         f.write(strategy)
    #
    #     print(f"[INFO] Saved strategy plan to: {save_path}")
    #     # procedure 2: generate step code and execute
    #     run_strategy_steps(save_path,args.llm_model)
    #
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

# python3 src/pipeline.py -s compare_agents -m gpt-4o -q "What's a good momentum strategy for TSLA over the past 3 months?"
# python3 src/pipeline.py -s full_pipeline -m gpt-4o -q "What's a good strategy for NVDA for the next 1 months?"
