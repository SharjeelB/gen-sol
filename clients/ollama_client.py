from ollama import Client

client = Client(host="http://localhost:11434")

MODEL = "llama3.2"


def ask_llm(prompt: str):

    response = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]

