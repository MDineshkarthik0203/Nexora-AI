import subprocess
import tempfile
import os


def execute_python_code(code: str):

    if not code:
        return {
            "success": False,
            "output": "",
            "error": "No Python code was provided."
        }

    temp_file = None

    try:

        # Create temporary Python file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as file:

            file.write(code)
            temp_file = file.name

        # Execute Python code
        result = subprocess.run(
            ["python", temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Successful execution
        if result.returncode == 0:

            return {
                "success": True,
                "output": result.stdout,
                "error": ""
            }

        # Failed execution
        return {
            "success": False,
            "output": result.stdout,
            "error": result.stderr
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "error": "Code execution timed out."
        }

    except Exception as e:

        return {
            "success": False,
            "output": "",
            "error": str(e)
        }

    finally:

        # Delete temporary file
        if temp_file and os.path.exists(temp_file):

            os.remove(temp_file)