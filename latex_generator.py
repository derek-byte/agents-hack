#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

class LatexGenerator:
    def __init__(self):
        self.template_dir = "latex_template"
        self._setup_template_directory()

    def _setup_template_directory(self):
        """Create template directory and necessary files"""
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
        
        # Create the NobArticle.cls file
        with open(f"{self.template_dir}/NobArticle.cls", "w") as f:
            f.write(r"""
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{NobArticle}[2023/04/18 Nob Article Class]
\LoadClass[twocolumn]{article}

% Required packages
\RequirePackage{geometry}
\RequirePackage{fancyhdr}
\RequirePackage{titlesec}
\RequirePackage{biblatex}
\RequirePackage{hyperref}

% Page geometry
\geometry{
    paper=a4paper,
    top=2.5cm,
    bottom=2.5cm,
    left=2.5cm,
    right=2.5cm
}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\newcommand{\runninghead}[1]{\fancyhead[C]{#1}}
\newcommand{\footertext}[1]{\fancyfoot[C]{#1}}
""")

    def generate_latex(self, content, title="Research Paper", authors=None, affiliations=None, keywords=None):
        """Generate LaTeX document with the given content"""
        if authors is None:
            authors = ["Author Name"]
        if affiliations is None:
            affiliations = ["Institution Name"]
        if keywords is None:
            keywords = ["Keyword1", "Keyword2"]

        template_vars = {
            'title': title,
            'year': datetime.now().year,
            'authors': ", ".join(authors),
            'affiliations': r" \\ ".join(affiliations),
            'abstract': content[:500],
            'keywords': ", ".join(keywords),
            'content': content
        }

        latex_template = r"""
\documentclass[twocolumn]{NobArticle}
\runninghead{%(title)s}
\footertext{\textit{Journal X} (%(year)s)}

\title{%(title)s}
\author{%(authors)s}
\date{%(affiliations)s}

\renewcommand{\maketitlehookd}{%%
\begin{abstract}
    \noindent %(abstract)s
    
    \medskip
    \small{\textbf{Index Terms:} %(keywords)s.}
\end{abstract}
}

\begin{document}
\small
\maketitle

%(content)s

\end{document}
"""
        # Apply the template variables
        latex_content = latex_template % template_vars
        
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
\section{Introduction}
This is the introduction section of the paper.

\section{Methods}
This section describes the methods used in the research.

\section{Results}
Here are the results of our study.

\section{Discussion}
Discussion of the results and their implications.

\section{Conclusion}
Final conclusions and future work.
"""
    
    try:
        pdf_path = generate_research_paper(
            content=content,
            title="Sample Research Paper",
            authors=["John Doe", "Jane Smith"],
            affiliations=["University A", "Research Institute B"],
            keywords=["Research", "Science", "Technology"]
        )
        print(f"PDF generated successfully at: {pdf_path}")
    except Exception as e:
        print(f"Error: {e}") 