from google.genai import types

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

# function declaration imported from the function tool file, in this case: import get_files_info.py's
# static AI function declartion (at the bottom of each function.py file:
# ie. get_files_info.py, write_file.py etc..)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ],
)
