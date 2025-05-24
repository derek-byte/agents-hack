from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from exa_py import Exa
import os
import requests
from bs4 import BeautifulSoup
import re

class PatentSearchParams(BaseModel):
    """Parameters for patent search functionality."""
    category: str = Field(..., description="The category or field of patents to search for (e.g. 'artificial intelligence', 'biotechnology')")
    num_patents: int = Field(default=10, description="Number of patents to return")

def scrape_google_patent_abstract(url: str) -> Optional[str]:
    """
    Scrapes the abstract from a Google Patents page.
    
    Args:
        url: The Google Patents URL to scrape
        
    Returns:
        The patent abstract if found, None otherwise
    """
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the English abstract section
        # First try to find the English translation section
        description = soup.find('div', {'class': 'description'})
        if description:
            abstract_section = description.find('div', string=lambda text: text and 'abstract' in text.lower())
            if abstract_section and abstract_section.find_next('div'):
                text = abstract_section.find_next('div').get_text(strip=True)
                # Clean up the text
                text = ' '.join(text.split())  # Normalize whitespace
                # Remove any non-English text (usually appears before "An apparatus" or similar)
                if "An " in text:
                    text = text[text.index("An "):]
                elif "The " in text:
                    text = text[text.index("The "):]
                return text.replace('\n', ' ').strip()
        
        # Fallback to regular abstract tag if no English translation found
        abstract = soup.find('abstract')
        if abstract:
            text = abstract.get_text(strip=True)
            # Clean up the text
            text = ' '.join(text.split())  # Normalize whitespace
            # Remove any non-English text
            if "An " in text:
                text = text[text.index("An "):]
            elif "The " in text:
                text = text[text.index("The "):]
            return text.replace('\n', ' ').strip()
            
        return None
    except Exception as e:
        print(f"Error scraping patent abstract: {str(e)}")
        return None

def extract_summary(text: str, max_length: int = 200) -> str:
    """
    Extract a concise summary from the patent text.
    Tries to get the first meaningful sentence or paragraph.
    """
    if not text:
        return "No description available"
    
    # Try to find the first complete sentence that's not too short
    sentences = text.split('.')
    for sentence in sentences:
        cleaned = sentence.strip()
        if len(cleaned) > 30:  # Only consider sentences with meaningful length
            summary = cleaned + '.'
            return summary if len(summary) <= max_length else summary[:max_length-3] + '...'
    
    # If no good sentence found, just take the first part of the text
    return text[:max_length-3] + '...' if len(text) > max_length else text

def search_patents(category: str, num_patents: int = 10) -> List[Dict[str, Any]]:
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
        )
        
        # Extract just the essential information from the results
        simplified_results = []
        if hasattr(response, 'results') and response.results:
            for result in response.results:
                url = getattr(result, 'url', '')
                # Get the abstract by scraping the patent page
                abstract = scrape_google_patent_abstract(url) if url else None
                
                # Ensure the abstract is a single string without line breaks
                if abstract:
                    abstract = ' '.join(abstract.split())
                
                simplified_result = {
                    'title': getattr(result, 'title', 'No title'),
                    'url': url,
                    'score': getattr(result, 'score', 0.0),
                    'summary': abstract if abstract else "No abstract available",
                    'metadata': getattr(result, 'metadata', {})
                }
                simplified_results.append(simplified_result)
        
        if not simplified_results:
            return [{"error": "No patents found for the given category"}]
            
        return simplified_results
    except Exception as e:
        return [{"error": f"Error searching patents: {str(e)}"}] 