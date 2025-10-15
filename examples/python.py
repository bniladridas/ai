from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def main():
    # Retrieve API key and configuration from environment variables
    api_key = os.getenv('NVIDIA_API_KEY', '$API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC')
    model_name = os.getenv('DEEPSEEK_MODEL_NAME', 'deepseek-ai/deepseek-r1')
    temperature = float(os.getenv('DEEPSEEK_DEFAULT_TEMPERATURE', 0.6))
    top_p = float(os.getenv('DEEPSEEK_DEFAULT_TOP_P', 0.7))
    max_tokens = int(os.getenv('DEEPSEEK_MAX_TOKENS', 4096))

    # Initialize OpenAI client with NVIDIA's base URL
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )

    # Create a chat completion request
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": "Which number is larger, 9.11 or 9.8?"}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        stream=True
    )

    # Stream and print the response
    print("DeepSeek AI Response:")
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

if __name__ == "__main__":
    main()
