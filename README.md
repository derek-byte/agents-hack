# AI Agent with Claude and Exa

This project implements an AI agent that combines Anthropic's Claude for natural language processing and Exa for code search and analysis capabilities.

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your API keys:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   EXA_API_KEY=your_exa_api_key_here
   ```

## Usage

Run the agent:
```bash
python agent.py
```

The agent provides the following capabilities:
1. Search code: Search through codebases using Exa's semantic search
2. Analyze code: Get detailed analysis and suggestions for improvement using Claude
3. Ask questions: Get answers about code, programming concepts, and more
4. Interactive mode: Choose from different options in an interactive command-line interface 