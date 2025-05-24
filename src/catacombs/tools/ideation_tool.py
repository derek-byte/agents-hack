import os
import json
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import anthropic

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    problem: str = Field(..., description="Problem being thought about")
    solution: str = Field(..., description="Solution for the problem given")
    reward: int = Field(..., description="Reward/rating for the current solution to the problem given")

class IdeationTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Given the problem, solution, and reward it modifies the solution to get the highest reward with the approach given"
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, problem: str, solution: str, reward: int) -> str:
        client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )

        message = client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=3000,
            system="You'll be given a problem, solution, and the reward (scale of 1 - 10) telling you how good the current solution is. Be objective and based on the current approach tweak the approach to maximize reward, your goal is to make sure the solution is feasible, and a new approach on how to solve it",
            messages=[
                {
                    "role": "user",
                    "content": "Think of a better solution that'd hypothetically maximize reward (max is 10) and return only the new solution"
                },
                {
                    "role": "user",
                    "content": f"Problem: {problem}\nSolution: {solution}\nReward: {solution}"
                } 
            ]   
        )

        return json.dumps(message.content)
