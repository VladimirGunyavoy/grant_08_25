# PowerShell script for LaTeX compilation AIDA-T

param(
    [string]$Action = "all"
)

$Target = "result"
$Latex = "pdflatex"

function Test-LaTeX {
    try {
        $null = Get-Command $Latex -ErrorAction Stop
        Write-Host "LaTeX found: $((Get-Command $Latex).Source)"
        return $true
    }
    catch {
        Write-Host "LaTeX not found. Install MiKTeX or TeX Live"
        Write-Host "Download MiKTeX: https://miktex.org/download"
        Write-Host "Download TeX Live: https://www.tug.org/texlive/"
        Write-Host "After installation restart PowerShell"
        return $false
    }
}

function Compile-LaTeX {
    param(
        [int]$Passes = 2
    )
    
    Write-Host "Compiling LaTeX document..."
    
    for ($i = 1; $i -le $Passes; $i++) {
        Write-Host "Pass $i of $Passes..."
        & $Latex -interaction=nonstopmode "$Target.tex"
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Compilation error on pass $i"
            return $false
        }
    }
    
    Write-Host "Document compiled successfully!"
    return $true
}

function Clean-TempFiles {
    $Extensions = @("aux", "log", "out", "toc", "lot", "lof", "blg", "bbl", "bcf", "run.xml", "fdb_latexmk", "fls", "synctex.gz")
    
    Write-Host "Cleaning temporary files..."
    
    foreach ($ext in $Extensions) {
        $file = "$Target.$ext"
        if (Test-Path $file) {
            Remove-Item $file -Force
            Write-Host "Deleted: $file"
        }
    }
    
    Write-Host "Temporary files cleaned!"
}

function Open-PDF {
    $pdfFile = "$Target.pdf"
    if (Test-Path $pdfFile) {
        Write-Host "Opening PDF..."
        Start-Process $pdfFile
    } else {
        Write-Host "PDF file not found. Compile document first."
    }
}

function Show-Help {
    Write-Host "Available commands:"
    Write-Host "  all      - Full compilation with 2 passes"
    Write-Host "  quick    - Quick compilation with 1 pass"
    Write-Host "  clean    - Remove temporary files"
    Write-Host "  cleanall - Full cleanup including PDF"
    Write-Host "  view     - Open PDF in browser"
    Write-Host "  viewall  - Compile and open PDF"
    Write-Host "  check    - Check dependencies"
    Write-Host "  help     - Show this help"
    Write-Host ""
    Write-Host "Usage examples:"
    Write-Host "  .\compile.ps1 all"
    Write-Host "  .\compile.ps1 quick"
    Write-Host "  .\compile.ps1 clean"
}

# Main logic
switch ($Action.ToLower()) {
    "all" {
        if (Test-LaTeX) {
            Compile-LaTeX -Passes 2
        }
    }
    "quick" {
        if (Test-LaTeX) {
            Compile-LaTeX -Passes 1
        }
    }
    "clean" {
        Clean-TempFiles
    }
    "cleanall" {
        Clean-TempFiles
        $pdfFile = "$Target.pdf"
        if (Test-Path $pdfFile) {
            Remove-Item $pdfFile -Force
            Write-Host "PDF file deleted!"
        }
    }
    "view" {
        Open-PDF
    }
    "viewall" {
        if (Test-LaTeX) {
            if (Compile-LaTeX -Passes 2) {
                Open-PDF
            }
        }
    }
    "check" {
        Test-LaTeX
    }
    "help" {
        Show-Help
    }
    default {
        Write-Host "Unknown command: $Action"
        Write-Host ""
        Show-Help
    }
}
