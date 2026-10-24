import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: Unable to create absolute path from "{working_directory}" - {e}'

    try:
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
    except Exception as e:
        return f'Error: Unable to create absolute path for "{directory}" - {e}'

    try:
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
    except Exception as e:
        return f'Error: Unable to validate common path - {e}'

    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    is_directory = os.path.isdir(target_dir)

    if is_directory == False:
        return f'Error: "{directory}" is not a directory'

    dir_items = os.listdir(target_dir)
    response = []
    for item in dir_items:
        try:
            response.append(f'- {item}: file_size={os.path.getsize(os.path.normpath(os.path.join(target_dir, item)))}, is_dir={os.path.isdir(os.path.normpath(os.path.join(target_dir, item)))}')
        except Exception as e:
            return f'Error: "{item}" caused - {e}'

    response = "\n".join(response)

    # return f'Success: "{directory}" is within the working directory'
    return response
