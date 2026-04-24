import os

from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_directory_abs, target_file])
            == working_directory_abs
        )

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        directory_of_target_file = os.path.dirname(target_file)
        os.makedirs(directory_of_target_file, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing file: {e}"


# AI input description for get_files_info function. AI CAN READ THIS. THIS IS STATIC.
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided 'content' into a file in a specified directory relative to the working directory, this will create a file if it doesnt already exist, and overwrite the file if it does exist",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write the 'content' to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is being written to the specified file.",
            ),
        },
    ),
)
