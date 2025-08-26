#!/usr/bin/env python3
"""
Script to add citation commands for all publications in LaTeX file
"""

import re

def extract_bibtex_keys(bibtex_file):
    """Extract all BibTeX keys from the file"""
    with open(bibtex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all @article{key, patterns
    pattern = r'@article\{([^,]+),'
    keys = re.findall(pattern, content)
    return keys

def add_citations_to_latex(latex_file, bibtex_keys):
    """Add citation commands to LaTeX file"""
    with open(latex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the bibliography section
    bib_pattern = r'(\\bibliography\{my_bib\})'
    
    # Create citation commands
    citations = []
    for key in bibtex_keys:
        citations.append(f'\\nocite{{{key}}}')
    
    citations_text = '\n'.join(citations)
    
    # Replace bibliography command with citations + bibliography
    new_content = re.sub(bib_pattern, f'{citations_text}\n\\1', content)
    
    # Write back to file
    with open(latex_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added {len(citations)} citation commands to {latex_file}")

def main():
    bibtex_file = 'central uni grant/my_bib.bib'
    latex_file = 'central uni grant/Osinenko_list_of_papers_no_preprints.tex'
    
    print("Extracting BibTeX keys...")
    keys = extract_bibtex_keys(bibtex_file)
    print(f"Found {len(keys)} publications")
    
    print("Adding citation commands to LaTeX file...")
    add_citations_to_latex(latex_file, keys)
    
    print("Done!")

if __name__ == "__main__":
    main()
