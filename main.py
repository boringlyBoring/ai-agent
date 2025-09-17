import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import MODEL_NAME, SYSTEM_PROMPT, available_functions


def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Please provide a prompt in arguments")
        sys.exit(1)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=SYSTEM_PROMPT
    )

    response = client.models.generate_content(
        model=MODEL_NAME, contents=messages, config=config
    )

    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")

    print(response.text)

    if verbose_flag:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
