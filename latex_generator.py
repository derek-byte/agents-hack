#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime
import anthropic
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

class LatexGenerator:
    def __init__(self):
        self.template_dir = "latex_template"
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env file")
        
        self.model = os.getenv('MODEL')
        if not self.model:
            raise ValueError("MODEL not found in .env file")
            
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self._setup_template_directory()

    def _setup_template_directory(self):
        """Create template directory if it doesn't exist"""
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
        
        # Create a proper template if it doesn't exist
        template_path = os.path.join(self.template_dir, "main.tex")
        if not os.path.exists(template_path):
            self._create_template()

    def _create_template(self):
        """Create a proper LaTeX template"""
        template_content = r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{cite}
\usepackage[margin=1in]{geometry}
\usepackage{fancyhdr}
\usepackage{abstract}

% Set up page style
\pagestyle{fancy}
\fancyhf{}
\rhead{\thepage}
\lhead{PAPER_TITLE_SHORT}

% Abstract styling
\renewcommand{\abstractname}{Abstract}

\begin{document}

% Title and author information
\title{PAPER_TITLE}
\author{PAPER_AUTHORS}
\date{PAPER_DATE}

% Custom title format without separate title page
\begin{center}
{\Large \textbf{PAPER_TITLE}} \\[0.5em]
{\normalsize PAPER_AUTHORS} \\[0.3em]
{\small PAPER_AFFILIATIONS} \\[0.5em]
{\small \today}
\end{center}

\vspace{1em}

% Abstract
\begin{abstract}
PAPER_ABSTRACT
\end{abstract}

\noindent \textbf{Index Terms:} PAPER_KEYWORDS

\vspace{1em}

% Main content starts here
PAPER_CONTENT

\end{document}
"""
        
        with open(os.path.join(self.template_dir, "main.tex"), "w") as f:
            f.write(template_content)

    def _check_if_content_is_structured(self, content):
        """Check if content already has LaTeX section structure"""
        section_patterns = [
            r'\\section\{',
            r'\\subsection\{',
            r'\\subsubsection\{'
        ]
        
        for pattern in section_patterns:
            if re.search(pattern, content):
                return True
        return False

    def _extract_abstract_from_content(self, content):
        """Extract or generate abstract from content"""
        # Look for existing abstract
        abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
        if abstract_match:
            return abstract_match.group(1).strip()
        
        # Look for text after "Abstract" heading
        abstract_match = re.search(r'Abstract\s*:?\s*(.*?)(?=\n\s*\n|\n\s*[A-Z])', content, re.DOTALL | re.IGNORECASE)
        if abstract_match:
            return abstract_match.group(1).strip()
        
        # Extract first meaningful paragraph
        lines = content.strip().split('\n')
        abstract_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('\\') and not re.match(r'^\d+\s', line):
                abstract_lines.append(line)
                joined = ' '.join(abstract_lines)
                if len(joined) > 200:  # Stop when we have enough text
                    break
        
        abstract = ' '.join(abstract_lines)[:500]
        if abstract and not abstract.endswith('.'):
            abstract += '.'
        
        return abstract or "This research paper presents findings on the given topic."

    def _clean_duplicate_sections(self, content):
        """Remove duplicate sections from content"""
        # Split content into sections
        sections = re.split(r'(\\section\{[^}]+\})', content)
        
        seen_sections = set()
        cleaned_parts = []
        current_section = None
        
        for part in sections:
            if re.match(r'\\section\{[^}]+\}', part):
                section_title = re.match(r'\\section\{([^}]+)\}', part).group(1).lower().strip()
                if section_title not in seen_sections:
                    seen_sections.add(section_title)
                    cleaned_parts.append(part)
                    current_section = section_title
                else:
                    current_section = None  # Skip this section
            else:
                if current_section is not None:  # Only add content if section wasn't skipped
                    cleaned_parts.append(part)
        
        return ''.join(cleaned_parts)

    def _process_content_with_claude(self, content):
        """Use Claude to process and structure the content"""
        
        # Check if content is already structured
        if self._check_if_content_is_structured(content):
            print("Content already has LaTeX structure, cleaning duplicates...")
            return self._clean_duplicate_sections(content)
        
        print("Processing unstructured content with Claude...")
        prompt = f"""Please convert the following content into a well-structured LaTeX research paper format.

IMPORTANT REQUIREMENTS:
1. Use standard academic sections: \\section{{Introduction}}, \\section{{Methodology}}, \\section{{Results}}, \\section{{Discussion}}, \\section{{Conclusion}}
2. Do NOT include \\documentclass, \\begin{{document}}, \\end{{document}}, \\title, \\author, \\maketitle, or abstract sections
3. Start directly with \\section{{Introduction}}
4. Avoid creating duplicate sections
5. Use proper LaTeX formatting for lists, equations, citations
6. Maintain academic tone and proper paragraph structure

Content to process:
{content}

Return only the LaTeX sections and subsections."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        processed_content = response.content[0].text
        return self._clean_duplicate_sections(processed_content)

    def generate_latex(self, content, title="Research Paper", authors=None, affiliations=None, keywords=None):
        """Generate LaTeX document with the given content"""
        print("Generating LaTeX...")
        
        if authors is None:
            authors = ["Author Name"]
        if affiliations is None:
            affiliations = ["Institution Name"]
        if keywords is None:
            keywords = ["Keyword1", "Keyword2"]

        # Process content through Claude or clean it if already structured
        processed_content = self._process_content_with_claude(content)
        print("Content processed successfully")

        # Format authors with superscripts
        formatted_authors = []
        for i, author in enumerate(authors, 1):
            formatted_authors.append(f"{author}\\textsuperscript{{{i}}}")
        authors_str = ", ".join(formatted_authors)

        # Format affiliations with superscripts
        formatted_affiliations = []
        for i, affiliation in enumerate(affiliations, 1):
            formatted_affiliations.append(f"\\textsuperscript{{\\textbf{{{i}}}}} {affiliation}")
        affiliations_str = " \\\\ ".join(formatted_affiliations)

        # Create short title for header
        short_title = title[:47] + "..." if len(title) > 50 else title

        # Extract or generate abstract
        abstract = self._extract_abstract_from_content(content)

        # Read the template file
        template_path = os.path.join(self.template_dir, "main.tex")
        with open(template_path, "r") as f:
            template = f.read()

        # Replace placeholders in template
        latex_content = (template
                        .replace("PAPER_TITLE", title)
                        .replace("PAPER_TITLE_SHORT", short_title)
                        .replace("PAPER_AUTHORS", authors_str)
                        .replace("PAPER_AFFILIATIONS", affiliations_str)
                        .replace("PAPER_ABSTRACT", abstract)
                        .replace("PAPER_KEYWORDS", ", ".join(keywords))
                        .replace("PAPER_CONTENT", processed_content))
        
        # Write the LaTeX content to a file
        output_path = os.path.join(self.template_dir, "paper.tex")
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"LaTeX file generated: {output_path}")
        return output_path

    def compile_pdf(self, tex_file):
        """Compile the LaTeX file to PDF"""
        print("Compiling PDF...")
        try:
            # Change to template directory for compilation
            original_dir = os.getcwd()
            os.chdir(self.template_dir)
            
            # Get just the filename
            tex_filename = os.path.basename(tex_file)
            
            # Use pdflatex for compilation (more widely available than latexmk)
            result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print("LaTeX compilation errors:")
                print(result.stdout)
                print(result.stderr)
                raise Exception(f"LaTeX compilation failed: {result.stderr}")

            # Run twice for proper cross-references
            subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename], 
                         capture_output=True)

            print("PDF compiled successfully")
            
            pdf_file = tex_filename.replace('.tex', '.pdf')
            full_pdf_path = os.path.join(original_dir, self.template_dir, pdf_file)
            
            if os.path.exists(pdf_file):
                return full_pdf_path
            else:
                raise Exception("PDF file was not generated")
                
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error compiling LaTeX: {e}")
        except FileNotFoundError:
            raise Exception("pdflatex not found. Please install LaTeX (e.g., TeX Live or MiKTeX)")
        finally:
            # Return to original directory
            os.chdir(original_dir)
            
            # Clean up auxiliary files
            aux_extensions = ['.aux', '.log', '.out', '.toc', '.bbl', '.blg', '.fls', '.fdb_latexmk']
            for ext in aux_extensions:
                aux_file = os.path.join(self.template_dir, 'paper' + ext)
                if os.path.exists(aux_file):
                    try:
                        os.remove(aux_file)
                    except:
                        pass

def generate_research_paper(content, title="Research Paper", authors=None, affiliations=None, keywords=None):
    """
    Generate a research paper PDF from the given content.
    
    Args:
        content (str): The main content of the paper
        title (str): The title of the paper
        authors (list): List of author names
        affiliations (list): List of author affiliations
        keywords (list): List of keywords
    
    Returns:
        str: Path to the generated PDF file
    """
    generator = LatexGenerator()
    tex_file = generator.generate_latex(
        content=content,
        title=title,
        authors=authors,
        affiliations=affiliations,
        keywords=keywords
    )
    return generator.compile_pdf(tex_file)

if __name__ == "__main__":
    # Example usage
    content = r"""
This research explores the impact of artificial intelligence on modern software development practices.
We analyze various AI-powered tools and their effects on developer productivity and code quality.

Our methodology involved surveying 500 software developers and analyzing their experiences with AI coding assistants.
The results show a 40% increase in productivity when using AI tools, with particular improvements in:
- Code completion
- Bug detection  
- Documentation generation
- Refactoring suggestions

However, challenges remain in terms of:
1. Code quality assurance
2. Security implications
3. Over-reliance on AI suggestions

We conclude that while AI tools significantly enhance developer productivity, they should be used as assistants rather than replacements for human expertise.
Future work should focus on improving AI model understanding of complex codebases and security implications.
"""
    
    try:
        pdf_path = generate_research_paper(
            content=content,
            title="Impact of AI on Software Development Practices",
            authors=["Claude 4", "Exa"],
            affiliations=["Anthropic", "Exa AI"],
            keywords=["Artificial Intelligence", "Software Development", "Developer Productivity"]
        )
        print(f"PDF generated successfully at: {pdf_path}")
    except Exception as e:
        print(f"Error: {e}")