import os
import sys
from subprocess import call

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import (
    MODEL_NAME,
    SYSTEM_PROMPT,
    available_functions,
    call_function,
)

MAX_ITERATIONS = 20


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

    i = 0
    while True:
        if i > MAX_ITERATIONS:
            print(f"Miximum itertations {MAX_ITERATIONS} reached.")
            sys.exit(1)
        else:
            try:
                response = generate_content(client, messages, verbose_flag)
                if response:
                    print(f"Final response: {response}")
                    break
            except Exception as e:
                print(f"Error while generating respnse: {e}")
                break


def generate_content(client, messages, verbose_flag):

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=SYSTEM_PROMPT
    )

    response = client.models.generate_content(
        model=MODEL_NAME, contents=messages, config=config
    )

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            if function_call_content:
                messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []

    for function_call in response.function_calls:
        function_response = call_function(function_call, verbose_flag)
        if not function_response:
            raise Exception(
                f"No result after calling function {function_call.name} with args {function_call.args}"
            )

        if (
            not function_response.parts
            or not function_response.parts[0].function_response.response
        ):
            raise Exception("Empty function call result")

        if verbose_flag:
            print(f"-> {function_response.parts[0].function_response.response}")
        function_responses.append(function_response.parts[0])

    messages.append(types.Content(role="tool", parts=function_responses))


main()
