import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


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
    args = parser.parse_args()  # read user input string from CLI

    # Creating list/ conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Main AI access code block
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=messages
    )

    if response.usage_metadata is None:
        raise RuntimeError("Gemini Api response metadata missing or malformed")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(f"{response.text}")


if __name__ == "__main__":
    main()
