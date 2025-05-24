# Catacombs 🏛️

*A Catacomb is an underground cemetery that consists of tombs constructed by the Ancient Romans*

Our agent takes dead ideas and brings them to the 21st century with a new approach.

## Overview

Catacombs is an automated system that excavates expired patents and resurrects them with modern technology solutions. Like archaeological discoveries waiting to be unearthed, many brilliant innovations were buried by the technological limitations of their era. This project acts as a digital wayback machine, systematically identifying these forgotten patents and proposing contemporary implementations that could bring them back to life.

## The Problem

Throughout history, countless patents have expired not because the underlying ideas were flawed, but because the technology of their time couldn't adequately support their implementation. These "technological fossils" represent untapped innovation potential that modern computing, materials science, and engineering could finally realize.

## Architecture

Catacombs operates through a sophisticated multi-agent pipeline that processes expired patents through several optimization stages:

```
Exa Search → Web Scraping → Agent Pipeline → PDF Research Paper
    ↓              ↓              ↓              ↓
Patent Discovery → Data Extraction → Solution Generation → Documentation
```

### Pipeline Components

#### 1. Patent Discovery Engine
- **Exa Search Integration**: Systematically searches Google Patents for expired patents
- **Automated Filtering**: Identifies patents that show promise for modern revival
- **Historical Context Analysis**: Evaluates why patents originally failed or expired

#### 2. Data Extraction Layer
- **Web Scraping Module**: Extracts comprehensive patent information including:
  - Original patent descriptions and claims
  - Historical context and limitations
  - Technical specifications and diagrams
  - Filing dates and expiration status

#### 3. Multi-Agent Processing Pipeline

The core innovation of Catacombs lies in its iterative agent-based approach to solution generation:

##### Agent 1: Approach Creator
- Analyzes expired patent specifications
- Generates multiple modern implementation strategies
- Considers current technological capabilities
- Proposes diverse solution pathways

##### Agent 2: Reward Generator
- Evaluates each proposed approach with numerical scoring
- Considers factors such as:
  - Technical feasibility with current technology
  - Market potential and commercial viability
  - Implementation complexity and cost
  - Innovation factor and differentiation

##### Optimization Loop
The Approach Creator and Reward Generator work in tandem, iteratively refining solutions until no further optimization is possible. This ensures each patent receives the most promising modern implementation strategy.

##### Agent 3: Approach Refiner
- Takes the highest-scoring approaches from the optimization loop
- Performs detailed technical refinement
- Addresses implementation challenges
- Enhances solution robustness

##### Agent 4: Optimal Approach Selector
- Evaluates all refined approaches
- Selects the single best implementation strategy
- Provides comprehensive justification for the selection
- Prepares final recommendations

#### 4. Research Paper Generator
- Converts the optimal approach into a structured research paper
- Generates publication-ready PDF documents
- Includes:
  - Executive summary of the revived patent
  - Historical context and original limitations
  - Proposed modern implementation
  - Technical specifications and requirements
  - Market analysis and potential impact

## Key Features

### Automated Discovery
- Continuous scanning of expired patent databases
- Smart filtering based on revival potential
- Historical trend analysis

### Multi-Agent Intelligence
- Collaborative AI agents with specialized functions
- Iterative optimization for maximum solution quality
- Objective scoring and evaluation systems

### Modern Implementation Focus
- Leverages current technological capabilities
- Considers contemporary materials, computing power, and engineering methods
- Evaluates market readiness and commercial potential

### Professional Documentation
- Generates research-quality papers
- Provides detailed technical specifications
- Includes comprehensive analysis and recommendations

## Use Cases

### Innovation Labs
Research and development teams can use Catacombs to identify overlooked innovations that modern technology can now support.

### Patent Attorneys
Legal professionals can discover expired patents with potential for new filings under updated implementations.

### Entrepreneurs
Startup founders can find validated concepts that were ahead of their time but feasible today.

### Academic Research
Researchers can explore the evolution of ideas and identify gaps in technological development.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv and texlive:

```bash
brew install texlive
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/catacombs/config/agents.yaml` to define your agents
- Modify `src/catacombs/config/tasks.yaml` to define your tasks
- Modify `src/catacombs/crew.py` to add your own logic, tools and specific args
- Modify `src/catacombs/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the catacombs Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Output

Each processed patent generates:
- **Technical Analysis Report**: Detailed evaluation of the original patent and proposed modern implementation
- **Research Paper PDF**: Publication-ready document with comprehensive analysis
- **Implementation Roadmap**: Step-by-step guide for bringing the patent to life with current technology