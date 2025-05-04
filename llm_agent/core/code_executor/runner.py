import subprocess


def exec_code(file_path: str, timeout: int) -> bool:
    """Runs Python code in isolated subprocess and returns execution result."""

    try:
        result = subprocess.run(
            args=["python3", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        success = result.returncode == 0
        output = result.stdout + "\n" + result.stderr
        return success, output.strip()

    except subprocess.TimeoutExpired:
        return False, f"Execution timed out after {timeout}s"
    except Exception as e:
        return False, f"Unexpected execution error: {type(e).__name__} {str(e)}"
