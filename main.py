import os
import argparse
import json

from tabnanny import verbose

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import available_functions


def main():
    # print("Hello from build-an-ai-agent!")
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError("No openrouter.ai api key found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("prompt", type=str, help="AI Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # prompt: str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    messages: list[dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.prompt},
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if response.usage == None:
        raise RuntimeError("Invalid response")

    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message

    if not message.tool_calls:
        print(f"Response:\n{message.content}")
        return

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
                    continue
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")


if __name__ == "__main__":
    main()
