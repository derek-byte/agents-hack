import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from anthropic import Anthropic
from exa_py import Exa
import json

class AIAgent:
    def __init__(self):
        """Initialize the AI agent with Claude and Exa clients."""
        load_dotenv()
        
        # Initialize Anthropic (Claude) client
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Initialize Exa client
        self.exa = Exa(api_key=os.getenv("EXA_API_KEY"))
        
        # Set up a conversation memory
        self.conversation_history = []

    def search_code(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for code using Exa's code search capabilities.
        
        Args:
            query: The search query
        
        Returns:
            List of search results
        """
        try:
            response = self.exa.search(query)
            # Extract just the essential information from the results
            simplified_results = []
            if hasattr(response, 'results'):
                for result in response.results:
                    simplified_result = {
                        'title': getattr(result, 'title', 'No title'),
                        'url': getattr(result, 'url', ''),
                        'score': getattr(result, 'score', 0.0),
                        'text': getattr(result, 'text', '')
                    }
                    simplified_results.append(simplified_result)
            return simplified_results
        except Exception as e:
            print(f"Error searching code: {e}")
            return []

    def analyze_code(self, code: str) -> str:
        """
        Analyze code using Claude's capabilities.
        
        Args:
            code: The code to analyze
        
        Returns:
            Analysis results as a string
        """
        try:
            message = self.anthropic.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"Please analyze this code and provide insights about its quality, potential issues, and suggestions for improvement:\n\n```\n{code}\n```"
                }]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error analyzing code: {e}")
            return f"Error analyzing code: {str(e)}"

    def ask_question(self, question: str, context: str = "") -> str:
        """
        Ask a question to Claude, optionally with additional context.
        
        Args:
            question: The question to ask
            context: Optional additional context
        
        Returns:
            Claude's response as a string
        """
        try:
            # Prepare the prompt with context if provided
            prompt = question if not context else f"Context:\n{context}\n\nQuestion: {question}"
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            
            message = self.anthropic.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=1000,
                messages=self.conversation_history
            )
            
            # Add Claude's response to history
            self.conversation_history.append({"role": "assistant", "content": message.content[0].text})
            
            return message.content[0].text
        except Exception as e:
            print(f"Error asking question: {e}")
            return f"Error asking question: {str(e)}"

def main():
    """Main function to demonstrate the agent's capabilities."""
    agent = AIAgent()
    
    while True:
        print("\n1. Search code")
        print("2. Analyze code")
        print("3. Ask a question")
        print("4. Exit")
        
        choice = input("\nChoose an option (1-4): ")
        
        if choice == "1":
            query = input("Enter your code search query: ")
            results = agent.search_code(query)
            print("\nSearch Results:")
            print(json.dumps(results, indent=2))
            
        elif choice == "2":
            code = input("Enter or paste the code to analyze: ")
            analysis = agent.analyze_code(code)
            print("\nAnalysis Results:")
            print(analysis)
            
        elif choice == "3":
            question = input("Enter your question: ")
            context = input("Enter any additional context (optional): ")
            response = agent.ask_question(question, context)
            print("\nResponse:")
            print(response)
            
        elif choice == "4":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 