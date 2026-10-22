import os

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

    if valid_target_dir == True:
        return f'Success: "{directory}" is within the working directory'
