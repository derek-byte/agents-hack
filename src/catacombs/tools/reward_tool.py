from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import anthropic
import os
import json

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    problem: str = Field(..., description="The problem which the solution is trying to solve")
    solution: str = Field(..., description="The solution to the problem; the thing that's being evaluated")


class RewardTool(BaseTool):
    name: str = "RewardTool"
    description: str = (
        "Given a thought/idea + approach on how to solve it the tool will rate/reward how good the idea is on a scale of 1 - 10; 1 being not good and 10 being the optimal solution"
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, problem: str, solution: str) -> str:
        client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )

        message = client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=1024,
            system="Your job is to take the approach given to you and reason about how good it is to solve the problem provided. Take as much time as you need and refer to as many external resources as needed. Your job is to be objective",
            messages=[
                {
                    "role": "user",
                    "content": "Ensure your output is a singular number from 1 to 10, 1 being the worst idea ever and 10 being phenomenal. Return only the rating/reward nothing else"
                },
                {
                    "role": "user",
                    "content": f"The problem is: {problem}\nThe solution is: {solution}'"
                }
            ]
        )

        return json.dumps(message.content)