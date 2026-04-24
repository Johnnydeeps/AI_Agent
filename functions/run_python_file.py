import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_directory_abs, target_file])
            == working_directory_abs
        )

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_string = []
        if result.returncode != 0:
            output_string.append(f"Process exited with code {result.returncode}")
        if result.stdout:
            output_string.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output_string.append(f"STDERR: {result.stderr}")
        if not output_string:
            output_string.append("No output produced")
        return "\n".join(output_string)

    except Exception as e:
        return f"Error: executing Python file: {e}"
