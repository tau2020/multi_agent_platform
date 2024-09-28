# agents/llm_interface.py

class LLMInterface:
    def generate(self, prompt):
        raise NotImplementedError("Subclasses should implement this method.")
