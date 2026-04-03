import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("api key was not found, please check your configuration")

client= genai.Client(api_key=api_key)

contents_ai = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
model_ai = "gemini-2.5-flash"


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    generate_content_response = client.models.generate_content(
            model="gemini-2.5-flash", contents=messages
            )

    if generate_content_response.usage_metadata is None:
        raise RuntimeError("API request failed, usage_metadata is None")
    

    # Almacenar en variables la subclase que recibe los tokens usados en el prompt y en la respuesta.
    tokens_prompt = generate_content_response.usage_metadata.prompt_token_count
    tokens_response = generate_content_response.usage_metadata.candidates_token_count


    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
        print(f"Prompt tokens: {tokens_prompt}")
        print(f"Response tokens: {tokens_response}")

    print("Hello from agent-ai!")
    print(generate_content_response.text)

if __name__ == "__main__":
    main()
