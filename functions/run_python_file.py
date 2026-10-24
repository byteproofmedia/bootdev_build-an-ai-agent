import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run the specified python file, file path is relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "required": {
                    "file_path": {
                        "type": "string",
                        "description": "File path to load content from, relative to the working directory.",
                    },
                },
                "args": {
                    "type": "array",
                    "items": "string",
                    "description": "File path to load content from, relative to the working directory.",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: Unable to create absolute path from "{working_directory}" - {e}'

    try:
        target = os.path.normpath(os.path.join(abs_path, file_path))
    except Exception as e:
        return f'Error: Unable to create absolute path for "{file_path}" - {e}'

    try:
        valid_target = os.path.commonpath([abs_path, target]) == abs_path
    except Exception as e:
        return f'Error: Unable to validate common path - {e}'

    if valid_target == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    try:
        file_exists = os.path.isfile(target)
    except Exception:
        return f'Error: Unable to validate file exists - {e}'

    if file_exists == False:
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if file_path.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = ["python", target]
        if args != None:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=abs_path, capture_output=True, text=True, timeout=30)

        output_str = []
        if completed_process.returncode != 0:
            output_str.append(f"Process existed with code {completed_process.returncode}")
        if completed_process.stderr == "" and completed_process.stdout == "":
            output_str.append("No output produced")
        if completed_process.stdout != "":
            output_str.append(f"STDOUT: {completed_process.stdout}")
        if completed_process.stderr != "":
            output_str.append(f"STDERR: {completed_process.stderr}")
        return "\n".join(output_str)
    except Exception as e:
        return f"Error: executing Python file: {e}"
