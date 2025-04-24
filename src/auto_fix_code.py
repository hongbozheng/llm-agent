# autofix.py
import threading
import time
import traceback
from io import StringIO
import contextlib

# ✅ STEP 1: create a placeholder for auto_fix() to be filled in later
def auto_fix(code: str, error_msg: str, plan, step_index: int, llm_model: str) -> str:
    print("[🛠️ AUTO-FIX] Attempting to fix code via GPT...")
    # Simulate LLM call delay (placeholder)
    time.sleep(3)
    # Return original code for now
    return code

# ✅ STEP 2: auto-fix execution using a threaded correction process
def execute_with_auto_fix_threaded(code: str, plan, step_index: int, llm_model: str, exec_globals: dict):
    max_attempts = 3
    attempt = 0
    fix_success = threading.Event()
    fix_result = {'code': code, 'error': None}

    def fix_loop():
        nonlocal fix_result, attempt
        while attempt < max_attempts:
            try:
                with contextlib.redirect_stdout(StringIO()):
                    exec(fix_result['code'], exec_globals)
                fix_success.set()
                return
            except Exception as e:
                fix_result['error'] = traceback.format_exc()
                print(f"[❌] Step {step_index} failed on attempt {attempt + 1}.")
                print(fix_result['error'])
                fix_result['code'] = auto_fix(fix_result['code'], fix_result['error'], plan, step_index, llm_model)
                time.sleep(1)
                attempt += 1

    fix_thread = threading.Thread(target=fix_loop)
    fix_thread.start()
    fix_thread.join(timeout=60)  # wait up to 60 seconds

    if fix_success.is_set():
        print(f"[✅] Step {step_index} executed successfully with auto-fix.")
        return True, fix_result['code'], None
    else:
        print(f"[🚫] Final execution failed for step {step_index}. Timeout or max attempts reached.")
        return False, fix_result['code'], fix_result['error']