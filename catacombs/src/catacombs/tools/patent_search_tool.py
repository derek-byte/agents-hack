from crewai.tools import BaseTool
from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
from exa_py import Exa
import os

class PatentSearchInput(BaseModel):
    """Input schema for PatentSearchTool."""
    category: str = Field(..., description="The category or field of patents to search for (e.g. 'artificial intelligence', 'biotechnology')")
    num_patents: int = Field(default=10, description="Number of patents to return")

class PatentSearchTool(BaseTool):
    name: str = "Patent Search Tool"
    description: str = (
        "A tool for searching historical patents in a specific category. "
        "This tool searches for expired patents from before the year 2000."
    )
    args_schema: Type[BaseModel] = PatentSearchInput

    def _run(self, category: str, num_patents: int = 10) -> List[Dict[str, Any]]:
        """
        Search for historical patents using Exa's search capabilities.
        
        Args:
            category: The category or field of patents to search for
            num_patents: Number of patents to return (default: 10)
        
        Returns:
            List of patent search results
        """
        try:
            # Initialize Exa client
            exa = Exa(api_key=os.getenv("EXA_API_KEY"))
            
            # Construct a query that specifically targets patents in the given category
            query = f"type:patent before:2000 status:patent expired historical {category}"
            
            # Use Exa's search with correct parameters
            response = exa.search(
                query,
                num_results=num_patents,
                use_autoprompt=True,
                include_domains=["https://patents.google.com/"]
                # https://freeip.mtu.edu/
            )
            
            # Extract just the essential information from the results
            simplified_results = []
            if hasattr(response, 'results'):
                for result in response.results:
                    simplified_result = {
                        'title': getattr(result, 'title', 'No title'),
                        'url': getattr(result, 'url', ''),
                        'score': getattr(result, 'score', 0.0),
                        'text': getattr(result, 'text', ''),
                        'metadata': getattr(result, 'metadata', {})
                    }
                    simplified_results.append(simplified_result)
            return simplified_results
        except Exception as e:
            return [{"error": f"Error searching patents: {str(e)}"}] 