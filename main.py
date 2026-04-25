import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    # load environment stored api_key from .env, with error if key stops working
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api_key missing. check .env in project root directory")

    # argparse added, creates the ability for a users input to be pass to "content=" inside
    # .generate_content to be passed into the api for the AI model.
    parser = argparse.ArgumentParser(
        description="Chatbot"
    )  # create parser object (imported from argparse)
    parser.add_argument(
        "user_prompt", type=str, help="User Prompt"
    )  # expect one argument called "user_prompt" which is a string

    # adding --verbose argument input
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()  # read user input string from CLI

    # Creating list/ conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Main AI access/config code block
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.usage_metadata is None:
        raise RuntimeError("Gemini Api response metadata missing or malformed")

    # changed print structure to reflect the addition of the --verbose flag in user_input
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # check to see if AI 'response' contains function calls.
    if response.function_calls:
        function_responses = []
        for response_returned_arg in response.function_calls:
            function_call_result = call_function(response_returned_arg, args.verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
                or not function_call_result.parts[0].function_response.response
            ):
                raise RuntimeError(
                    f"Empty function response for {response_returned_arg.name}"
                )
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            function_responses.append(function_call_result.parts[0])
    else:
        print("Response:")
        print(f"{response.text}")


if __name__ == "__main__":
    main()
