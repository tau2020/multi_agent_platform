# agents/model_loader.py

import os
from dotenv import load_dotenv
from agents.llm_interface import LLMInterface
from agents.llm_openai import OpenAILLM
from agents.llm_anthropic import AnthropicLLM
from agents.llm_huggingface import HuggingFaceLLM

load_dotenv()

def get_llm():
    model_type = os.getenv('MODEL_TYPE')
    if model_type == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
        return OpenAILLM(api_key)
    elif model_type == 'anthropic':
        api_key = os.getenv('ANTHROPIC_API_KEY')
        return AnthropicLLM(api_key)
    elif model_type == 'huggingface':
        model_name = os.getenv('HUGGINGFACE_MODEL_NAME')
        return HuggingFaceLLM(model_name)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

# Initialize the model once to reuse across agents
llm_model = get_llm()
