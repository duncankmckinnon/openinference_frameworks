from typing import Dict, List


class Prompts:
    base_prompt = """
            # Role
            You are a helpful assistant that can answer questions and help with tasks.
        """

    def format_prompt(self, request: str, context: str = None) -> List[Dict]:
        return f"""
        {self.base_prompt}
        Customer message: {request}
        Context: {context}
        """
