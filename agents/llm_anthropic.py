# agents/llm_anthropic.py

import anthropic
from agents.llm_interface import LLMInterface

class AnthropicLLM(LLMInterface):
    def __init__(self, api_key):
        self.client = anthropic.Client(api_key)

    def generate(self, prompt):
        response = self.client.completion(
            prompt=anthropic.HUMAN_PROMPT + prompt + anthropic.AI_PROMPT,
            stop_sequences=[anthropic.HUMAN_PROMPT],
            max_tokens_to_sample=500,
            temperature=0.7,
        )
        return response['completion'].strip()
