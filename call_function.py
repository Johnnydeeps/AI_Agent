from google.genai import types

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

# function declaration imported from the function tool file, in this case: import get_files_info.py's
# static AI function declartion (at the bottom of each function.py file:
# ie. get_files_info.py, write_file.py etc..)
# # Bundle all four function schemas into a single Tool object that we'll pass
# to the LLM, so it knows what functions are available to call.
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ],
)


def call_function(function_call, verbose=False):
    # check to handle --verbose inputs from CLI/user and return the correct name and arguments
    # from the above LLM prompts
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # hard coded dictionary of permissable functions incase LLM messes up and doesnt
    # grab the correct functions based on the above prompts.
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    # check to see if function_name is in the function map, if not returns the error
    # in the prescribed manner from google.genai to catch the error and not crash.
    function_name = function_call.name or ""
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    # # Make a shallow copy of the LLM-provided args dict so we can safely mutate it.
    # If the LLM didn't provide any args, default to an empty dict.
    #  dictionaries are require for the google.genai classes to function like the above.
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    # Look up the real function by name, then call it with **args to unpack the
    # dictionary into keyword arguments. Wrap the string result in a types.Content
    # so the LLM can later receive it as a structured tool response.
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
