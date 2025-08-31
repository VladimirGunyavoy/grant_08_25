# LaTeX Compilation in VSCode

This project is configured for proper LaTeX compilation in VSCode with automatic bibliography processing.

## Setup

1. **Install LaTeX Workshop Extension**
   - Open VSCode
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "LaTeX Workshop" by James Yu
   - Install the extension

2. **Install LaTeX Distribution**
   - **Windows**: Install [MiKTeX](https://miktex.org/) or [TeX Live](https://tug.org/texlive/)
   - **macOS**: Install [MacTeX](https://tug.org/mactex/) or [TeX Live](https://tug.org/texlive/)
   - **Linux**: `sudo apt-get install texlive-full` (Ubuntu/Debian)

## Features

✅ **Automatic compilation** on save  
✅ **Bibliography support** (bibtex)  
✅ **Proper compilation sequence**: pdflatex → bibtex → pdflatex → pdflatex  
✅ **PDF viewer** in VSCode tab  
✅ **Error highlighting** in source code  
✅ **Auto-clean** temporary files  

## Usage

### Automatic Compilation
- Simply save your `.tex` file (Ctrl+S)
- VSCode will automatically compile to PDF
- PDF opens in a new tab

### Manual Compilation
- **Ctrl+Alt+B**: Build LaTeX document
- **Ctrl+Alt+C**: Clean auxiliary files
- **Ctrl+Alt+V**: View PDF

### Build Tasks
- **Ctrl+Shift+P** → "Tasks: Run Task"
- Choose "Build LaTeX" or "Build LaTeX with Bibliography"

## Configuration Files

- `.vscode/settings.json` - LaTeX Workshop settings
- `.vscode/extensions.json` - Recommended extensions
- `.vscode/tasks.json` - Build tasks

## Compilation Sequence

1. **pdflatex** - First pass (creates aux files)
2. **bibtex** - Process bibliography (if .bib file exists)
3. **pdflatex** - Second pass (resolves references)
4. **pdflatex** - Third pass (resolves cross-references)

## Troubleshooting

### "pdflatex not found"
- Install a LaTeX distribution
- Make sure it's in your system PATH

### Bibliography not working
- Ensure your .bib file is in the same directory
- Check that you have `\bibliography{filename}` in your .tex file

### PDF not updating
- Try manual build: Ctrl+Alt+B
- Check the LaTeX Workshop output panel for errors
