from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import anthropic
import os
import json


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    problem: str = Field(..., description="Problem that needs solving")
    solution: str = Field(..., description="Solution to said problem")
    reward: int = Field(..., description="Reward rating how good that solution is to solve that problem")

class BestApproachTool(BaseTool):
    name: str = "Best Approach Tool"
    description: str = (
        "After all of the ideas have been evaluated to maximize reward, pick the tool with the highest reward"
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, problem: str, solution: str, reward: int) -> str:
        client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        
        message = client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=1000,
            system="Your job is to take the 5 different approaches given to you and pick the most optimal one, usually indicated by the highest reward",
            messages=[
                {
                    "role": "user",
                    # "content": "Pick the best solution with the highest reward\nEnsure your output is only 1 solution, the idea, and all of the details relating to the solution"
                    "content": "Make sure to return only the optimal solution"
                },
                {
                    "role": "user",
                    "content": f"Problem: {problem}\nSolution: {solution}\nReward: {reward}"
                }
            ]
        )
         
        return json.dumps(message.content)