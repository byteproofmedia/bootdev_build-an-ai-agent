import os

from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Gets the contents of a file relative to the working directory, with a max response of {MAX_CHARS} characters.",
        "parameters": {
            "type": "object",
            "properties": {
                "required": {
                    "file_path": {
                        "type": "string",
                        "description": "File path to load content from, relative to the working directory.",
                    },
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
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
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        is_file = os.path.isfile(target)
    except Exception as e:
        return f'Error: Unable to check if {target} is a file - {e}'

    if is_file == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    if is_file == True:
        try:
            with open(target, "r") as f:
                contents = f.read(MAX_CHARS)
                if f.read(1):
                    contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        except Exception as e:
            return f'Error: Unable to read file "{target}'

        return contents
