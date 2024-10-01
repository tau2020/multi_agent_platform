import json
from typing import Any, Dict, List, Union

class LLMResponseResolver:
    def __init__(self):
        self.supported_llms = ["openai", "anthropic", "huggingface"]

    def resolve(self, llm_type: str, raw_response: str) -> Dict[str, Any]:
        """
        Resolve the raw LLM response into a standardized format consumable by agents.
        
        :param llm_type: Type of LLM used (e.g., "openai", "anthropic", "huggingface")
        :param raw_response: Raw response from the LLM API
        :return: Standardized dictionary containing resolved response
        """
        if llm_type not in self.supported_llms:
            raise ValueError(f"Unsupported LLM type: {llm_type}")

        resolver_method = getattr(self, f"_resolve_{llm_type}")
        return resolver_method(raw_response)

    def _resolve_openai(self, raw_response: str) -> Dict[str, Any]:
        try:
            parsed_response = json.loads(raw_response)
            return {
                "content": parsed_response["choices"][0]["message"]["content"],
                "role": parsed_response["choices"][0]["message"]["role"],
                "model": parsed_response["model"],
                "usage": parsed_response["usage"]
            }
        except (json.JSONDecodeError, KeyError) as e:
            return self._handle_parsing_error(raw_response, str(e))

    def _resolve_anthropic(self, raw_response: str) -> Dict[str, Any]:
        try:
            parsed_response = json.loads(raw_response)
            return {
                "content": parsed_response["completion"],
                "model": parsed_response.get("model", "unknown"),
                "stop_reason": parsed_response.get("stop_reason", None)
            }
        except (json.JSONDecodeError, KeyError) as e:
            return self._handle_parsing_error(raw_response, str(e))

    def _resolve_huggingface(self, raw_response: str) -> Dict[str, Any]:
        try:
            parsed_response = json.loads(raw_response)
            return {
                "content": parsed_response[0]["generated_text"],
                "model": "huggingface_model"  # Huggingface doesn't typically return model info in the response
            }
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            return self._handle_parsing_error(raw_response, str(e))

    def _handle_parsing_error(self, raw_response: str, error_msg: str) -> Dict[str, Any]:
        return {
            "content": raw_response,
            "error": f"Failed to parse LLM response: {error_msg}",
            "raw_response": raw_response
        }

    def extract_actions(self, resolved_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract actionable items from the resolved response.
        This method can be expanded to handle more complex action extraction logic.
        
        :param resolved_response: The resolved response from an LLM
        :return: List of actionable items
        """
        content = resolved_response.get("content", "")
        # This is a simple example. In a real-world scenario, you might use
        # more sophisticated NLP techniques to extract actions.
        actions = []
        for line in content.split('\n'):
            if line.strip().lower().startswith("action:"):
                actions.append({"type": "action", "description": line.strip()[7:].strip()})
        return actions

    def get_response_metadata(self, resolved_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract metadata from the resolved response.
        
        :param resolved_response: The resolved response from an LLM
        :return: Dictionary containing metadata
        """
        metadata = {}
        for key in ["model", "usage", "stop_reason"]:
            if key in resolved_response:
                metadata[key] = resolved_response[key]
        return metadata

# Example usage:
# resolver = LLMResponseResolver()
# raw_response = '{"choices":[{"message":{"role":"assistant","content":"Hello, how can I help you today?"}}],"model":"gpt-3.5-turbo","usage":{"total_tokens":20}}'
# resolved = resolver.resolve("openai", raw_response)
# print(resolved)
# actions = resolver.extract_actions(resolved)
# print(actions)
# metadata = resolver.get_response_metadata(resolved)
# print(metadata)
