#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime
import anthropic
from dotenv import load_dotenv

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

    def _process_content_with_claude(self, content):
        """Use Claude to process and structure the content"""
        prompt = f"""Please rephrase and structure the following content into a formal academic research paper format. 
        Include appropriate section headings and maintain academic tone throughout.
        Keep LaTeX formatting intact and add appropriate LaTeX commands where needed.
        Here's the content:

        {content}

        Format the response as a proper LaTeX document with sections. Preserve any existing LaTeX commands and add new ones where appropriate.
        Make it more formal and academic in tone."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text

    def generate_latex(self, content, title="Research Paper", authors=None, affiliations=None, keywords=None):
        """Generate LaTeX document with the given content"""
        print("generating latex")
        if authors is None:
            authors = ["Author Name"]
        if affiliations is None:
            affiliations = ["Institution Name"]
        if keywords is None:
            keywords = ["Keyword1", "Keyword2"]

        # Process content through Claude
        processed_content = self._process_content_with_claude(content)
        print("processed content")

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

        # Read the template file
        with open(f"{self.template_dir}/main.tex", "r") as f:
            template = f.read()

        # Extract abstract from processed content (first paragraph or up to 500 chars)
        abstract = processed_content.split('\n\n')[0][:500]

        # Replace the placeholders in the template
        latex_content = template.replace(
            "An Article Title That Spans Multiple Lines to Show Line Wrapping",
            title
        ).replace(
            "Author One\\textsuperscript{1,2}, \n    Author Two\\textsuperscript{3} \n    and Author Three\\textsuperscript{1}",
            authors_str
        ).replace(
            "\\textsuperscript{\\textbf{1}}\n    School of Computer Science, The University of City \\\\ \\textsuperscript{\\textbf{2}}\n    Computer Science Department, The University of City \\\\ \\textsuperscript{\\textbf{3}}\n    Computer Science Department, The University of Village",
            affiliations_str
        ).replace(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent porttitor arcu luctus, imperdiet urna iaculis, mattis eros. Pellentesque iaculis odio vel nisl ullamcorper, nec faucibus ipsum molestie. Sed dictum nisl non aliquet porttitor. Etiam vulputate arcu dignissim, finibus sem et, viverra nisl. Aenean luctus congue massa, ut laoreet metus ornare in. Nunc fermentum nisi imperdiet lectus tincidunt vestibulum at ac elit. Nulla mattis nisl eu malesuada suscipit. Aliquam arcu turpis, ultrices sed luctus ac, vehicula id metus. Morbi eu feugiat velit, et tempus augue. Proin ac mattis tortor. Donec tincidunt, ante rhoncus luctus semper, arcu lorem lobortis justo, nec convallis ante quam quis lectus. Aenean tincidunt sodales massa, et hendrerit tellus mattis ac. Sed non pretium nibh. Donec cursus maximus luctus. Vivamus lobortis eros et massa porta porttitor.",
            abstract
        ).replace(
            "Keyword A, Keyword B, Keyword C",
            ", ".join(keywords)
        ).replace(
            "\\blindtext",
            processed_content
        )
        
        # Write the LaTeX content to a file
        with open(f"{self.template_dir}/paper.tex", "w") as f:
            f.write(latex_content)
        
        print("generated latex file")
        return f"{self.template_dir}/paper.tex"

    def compile_pdf(self, tex_file):
        """Compile the LaTeX file to PDF"""
        print("compiling pdf")
        try:
            # Use latexmk for faster compilation
            subprocess.run(['latexmk', '-pdf', '-interaction=nonstopmode', 
                          '-output-directory=' + self.template_dir, tex_file], 
                         check=True, capture_output=True)

            print("compiled pdf")
            
            pdf_file = tex_file.replace('.tex', '.pdf')
            if os.path.exists(pdf_file):
                return pdf_file
            else:
                raise Exception("PDF file was not generated")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error compiling LaTeX: {e.stderr.decode()}")
            
        finally:
            # Clean up auxiliary files
            subprocess.run(['latexmk', '-c', '-output-directory=' + self.template_dir, tex_file],
                         capture_output=True)

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