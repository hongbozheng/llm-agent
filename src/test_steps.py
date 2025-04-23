import os
import traceback

def execute_step_folder(folder_path: str):
    """
    Execute all step_*.py files in the given folder sequentially.
    """
    exec_globals = {}
    results = []

    # Collect and sort step files
    step_files = sorted(
        [f for f in os.listdir(folder_path) if f.startswith("step_") and f.endswith(".py")]
    )

    for i, filename in enumerate(step_files):
        file_path = os.path.join(folder_path, filename)
        print(f"\n=== 🧪 Executing Step {i}: {filename} ===")

        try:
            with open(file_path, "r") as f:
                code = f.read()
            exec(code, exec_globals)
            print(f"[✅] Step {i} executed successfully.")
            results.append((filename, "success", None))
        except Exception as e:
            error_msg = traceback.format_exc()
            print(f"[❌] Step {i} execution failed.")
            print(error_msg)
            results.append((filename, "error", str(e)))

    return results


if __name__ == "__main__":
    folder = "step/gpt-4o"
    result = execute_step_folder(folder)
    for file, status, err in result:
        print(f"{file}: {status}")
