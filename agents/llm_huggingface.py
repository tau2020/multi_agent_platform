# agents/llm_huggingface.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from agents.llm_interface import LLMInterface

class HuggingFaceLLM(LLMInterface):
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate(self, prompt):
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(inputs, max_length=inputs.shape[1]+500, temperature=0.7)
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return generated_text[len(prompt):].strip()
        except Exception as e:
            print(f"HuggingFace LLM error: {e}")
            return ""
