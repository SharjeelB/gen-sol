from fastapi import FastAPI
from pydantic import BaseModel

from agents.agent_ollam import JsonAgent

app = FastAPI()

agent = JsonAgent("data/employee.json")


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(question: Question):

    answer = agent.ask(question.question)

    return {
        "question": question.question,
        "answer": answer
    }