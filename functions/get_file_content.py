import os

from google.genai import types

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_directory_abs, target_file])
            == working_directory_abs
        )
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            overflow = f.read(1)
            if overflow:
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return file_content_string
    except Exception as e:
        return f"Error reading file: {e}"


# AI input description for get_files_info function. AI CAN READ THIS. THIS IS STATIC.
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in a specified directory relative to the working directory, providing file contents with a maxiumum character count of 10000",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)
