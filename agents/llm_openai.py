import os
from openai import OpenAI
from agents.llm_interface import LLMInterface
from dotenv import load_dotenv

load_dotenv()

class OpenAILLM(LLMInterface):
    def __init__(self, api_key=None):
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key must be provided")
            self.client = OpenAI(api_key=api_key)

    def generate(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use "gpt-4" if you have access, or "gpt-3.5-turbo" for a smaller model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes code."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""