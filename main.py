import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI


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
    args = parser.parse_args()
    # prompt: str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    messages: list[dict[str, str]] = [
        {"role": "user", "content": args.prompt},
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if response.usage == None:
        raise RuntimeError("Invalid response")

    print(f"User prompt: {args.prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print(f"Response:\n{response.choices[0].message.content}")


if __name__ == "__main__":
    main()
