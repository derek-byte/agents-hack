from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from exa_py import Exa
import os
import json

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    problem: str = Field(..., description="Problem that needs solving")
    solution: str = Field(..., description="Solution to the problem")

class ExaTool(BaseTool):
    name: str = "ExaTool"
    description: str = (
        "Uses Exa to research about the topic given to it"
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, problem: str, solution: str) -> str:
        exa = Exa(api_key=os.getenv("EXA_API_KEY"))
        
        output = exa.search(
            f"Give me more information about problem: {problem} and solution: {solution}",
            num_results=5,
            use_autoprompt=True
        )
        
        return_str = ""
        
        for obj in output.results:
            return_str += json.dumps(obj) + "\n"
        
        return return_str