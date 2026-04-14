import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("api key was not found, please check your configuration")

client= genai.Client(api_key=api_key)


model_ai = "gemini-2.5-flash"


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    
    for _ in range(20):

        generate_content_response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0,
                    tools=[available_functions]
                    ),
                )
        
        for candidate in generate_content_response.candidates:
            messages.append(candidate.content)
    

        if generate_content_response.usage_metadata is None:
            raise RuntimeError("API request failed, usage_metadata is None")
        

        # Almacenar en variables la subclase que recibe los tokens usados en el prompt y en la respuesta.
        tokens_prompt = generate_content_response.usage_metadata.prompt_token_count
        tokens_response = generate_content_response.usage_metadata.candidates_token_count


        if args.verbose:
            print(f"User prompt: {args.user_prompt}\n")
            print(f"Prompt tokens: {tokens_prompt}")
            print(f"Response tokens: {tokens_response}")

        if generate_content_response.function_calls:
            function_results = []
            for function_call in generate_content_response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception("No parts in function call result")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("No function response")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("No response in function call")
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_results.append(function_call_result.parts[0])
            
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(generate_content_response.text)
            break
    else:
        print("Maximum iterations reached without a final response")
if __name__ == "__main__":
    main()
