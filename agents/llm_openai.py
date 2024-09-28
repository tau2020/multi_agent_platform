# agents/llm_openai.py

import os
from openai import OpenAI
from agents.llm_interface import LLMInterface
from openai import OpenAIError  # Correctly import the OpenAIError exception
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenAILLM(LLMInterface):
    def __init__(self, api_key=None):
        # Allow api_key to be passed directly or via environment variable
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided")
        
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use "gpt-4" if you have access
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes code."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ""