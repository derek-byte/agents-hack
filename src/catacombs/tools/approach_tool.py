"""
A LLM who's purpose is to generate a reward function for a given thought
Claude Model: claude-3-5-haiku-latest
"""
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import json
import anthropic


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    title: str = Field(..., description="Title of the patent you want to analyze further")
    description: str = Field(..., description="Description of the patent you want to analyze further")

class ApproachTool(BaseTool):
    name: str = "Generate Approach"
    description: str = (
        "A tool that takes one idea and outputs 5 different approaches to solve it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, title: str, description: str) -> str:
        client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        
        message = client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=3000,
            system="Your job is to take the idea given to you and generate 5 different approaches to solve it. An idea and 1 non-optimal approach will be given to you. Your job is to analyze and think of why the approach given to you doesn't work and generate 5 approaches that would solve the idea in a feasible manner.",
            messages=[
                {
                    "role": "user",
                    "content": "Ensure your output is a JSON array of 5 objects, each with a 'title' and 'description' field. Do not include any other text in your response."
                },
                {
                    "role": "user",
                    "content": f"The title of the idea is: {title}\nThe description of the non-optimal approach is: {description}'"
                }
            ]
        )

        return json.dumps(message.content)
