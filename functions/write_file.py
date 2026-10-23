import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
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
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    is_directory = os.path.isdir(target)

    if is_directory == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(os.path.dirname(target), exist_ok=True)
    except Exception as e:
        return f'Error: Unable to create all parent directories for "{file_path}"'

    try:
        with open(target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Failed to write to "{file_path}"'
