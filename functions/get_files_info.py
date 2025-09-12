import os


def get_files_info(working_directory, directory="."):

    abs_working_dir = os.path.abspath(working_directory)

    abs_dir = os.path.join(working_directory, directory)
    abs_dir_path = os.path.abspath(abs_dir)

    if not abs_dir_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    final_response = ""

    for file in os.listdir(abs_dir_path):
        file_path = os.path.join(abs_dir_path, file)
        file_size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        response = f"- {file}: file_size={file_size} bytes, is_dir={is_dir}"
        final_response += response + "\n"

    return final_response
