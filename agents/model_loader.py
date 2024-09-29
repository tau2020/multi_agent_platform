# agents/model_loader.py

import os
from dotenv import load_dotenv
from agents.llm_interface import LLMInterface
from agents.llm_openai import OpenAILLM
from agents.llm_anthropic import AnthropicLLM
from agents.llm_huggingface import HuggingFaceLLM

load_dotenv()

_model_cache = {}

def get_llm(model_type, config):
    global _model_cache
    if model_type in _model_cache:
        return _model_cache[model_type]
    else:
        if model_type == 'openai':
            api_key = config.get('OPENAI_API_KEY')
            llm = OpenAILLM(api_key)
        elif model_type == 'anthropic':
            api_key = config.get('ANTHROPIC_API_KEY')
            llm = AnthropicLLM(api_key)
        elif model_type == 'huggingface':
            model_name = config.get('HUGGINGFACE_MODEL_NAME')
            llm = HuggingFaceLLM(model_name)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        _model_cache[model_type] = llm
        return llm
