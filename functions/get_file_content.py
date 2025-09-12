import os

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):

    try:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_dir_path = os.path.abspath(working_directory)

        if not abs_file_path.startswith(abs_working_dir_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(abs_file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        with open(abs_file_path, "r") as f:
            file_content = f.read()

            if len(file_content) > MAX_CHARS:
                file_content = (
                    file_content[:MAX_CHARS]
                    + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return file_content

    except Exception as e:
        return f"Error: {e}"
