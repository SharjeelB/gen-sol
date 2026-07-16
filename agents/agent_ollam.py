import json
from clients.ollama_client import ask_llm


class JsonAgent:

    def __init__(self, filename):

        with open(filename, "r") as f:
            self.data = json.load(f)

    def ask(self, question):

        prompt = f"""
You are an Employee Assistant.

Answer ONLY from the JSON.

If the answer is not present, say:

"I don't know based on the provided data."

JSON:

{json.dumps(self.data, indent=2)}

Question:

{question}

Answer:
"""

        return ask_llm(prompt)