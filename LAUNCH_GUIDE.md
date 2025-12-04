# SAVVI Master Scaffold Launcher
# Platform-agnostic entry point
# Usage: 
#   Windows: savvi_init.ps1
#   Mac/Linux: bash savvi_init.sh

# For Windows PowerShell:
# Copy the PowerShell section below to savvi_init.ps1

# For Mac/Linux Bash:
# Copy the Bash section below to savvi_init.sh

#############################################################################
# WINDOWS POWERSHELL VERSION
#############################################################################
# File: savvi_init.ps1

param(
    [string]$ProjectPath = "$env:USERPROFILE\projects\savvi"
)

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         SAVVI - Cross-Platform Scaffold Launcher         ║" -ForegroundColor Cyan
Write-Host "║  Sensitive • Allergic • Vegan • Vegetarian • Intolerant ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

Write-Host "`nWindows 11 / PowerShell Edition" -ForegroundColor Yellow
Write-Host "Target Project: $ProjectPath`n" -ForegroundColor White

# Check if running as administrator
$admin = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object System.Security.Principal.WindowsPrincipal($admin)
$isAdmin = $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  Recommended: Run PowerShell as Administrator for better permissions" -ForegroundColor Yellow
}

# Step 1: Run main scaffold
Write-Host "`n[1/3] Running project scaffold..." -ForegroundColor Cyan
if (Test-Path ".\savvi_scaffold.ps1") {
    & ".\savvi_scaffold.ps1" -ProjectPath $ProjectPath
    Write-Host "✓ Scaffold complete" -ForegroundColor Green
} else {
    Write-Host "✗ Error: savvi_scaffold.ps1 not found in current directory" -ForegroundColor Red
    exit 1
}

# Step 2: Initialize Python environment
Write-Host "`n[2/3] Setting up Python environment..." -ForegroundColor Cyan
$venvPath = Join-Path $ProjectPath "venv"
$pythonExe = Join-Path $venvPath "Scripts\python.exe"

try {
    # Test Python installation
    $pythonVersion = & python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
    
    # Create virtual environment
    Write-Host "  Creating virtual environment..." -ForegroundColor White
    & python -m venv $venvPath
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
    
    # Activate and install dependencies
    Write-Host "  Activating venv..." -ForegroundColor White
    & "$venvPath\Scripts\Activate.ps1"
    
    Write-Host "  Installing dependencies..." -ForegroundColor White
    & pip install --upgrade pip > $null
    & pip install -r (Join-Path $ProjectPath "requirements.txt")
    Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Error during Python setup: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Check for Tesseract (optional but recommended)
Write-Host "`n[3/3] Checking optional dependencies..." -ForegroundColor Cyan
try {
    $tesseract = Get-Command tesseract -ErrorAction SilentlyContinue
    if ($tesseract) {
        Write-Host "✓ Tesseract found: $($tesseract.Source)" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  Tesseract not found (optional for OCR)" -ForegroundColor Yellow
        Write-Host "  To install: choco install tesseract (requires Chocolatey)" -ForegroundColor Gray
    }
} catch {
    Write-Host "ℹ️  Tesseract not found (optional for OCR)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                ✅ Setup Complete!                         ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n📁 Project Structure: $ProjectPath" -ForegroundColor Yellow
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   • $ProjectPath\README.md" -ForegroundColor Gray
Write-Host "   • $ProjectPath\TODO.md" -ForegroundColor Gray
Write-Host "   • $ProjectPath\cursor.md" -ForegroundColor Gray

Write-Host "`n🚀 Quick Start:" -ForegroundColor Cyan
Write-Host "   1. Edit: $ProjectPath\.env" -ForegroundColor White
Write-Host "   2. Copy .env.template → .env and add your API keys" -ForegroundColor White
Write-Host "   3. cd $ProjectPath" -ForegroundColor White
Write-Host "   4. .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   5. python src/main.py --help" -ForegroundColor White

Write-Host "`n🔧 For Cursor IDE Development:" -ForegroundColor Cyan
Write-Host "   cursor $ProjectPath" -ForegroundColor White
Write-Host "   Then review cursor.md for development guide" -ForegroundColor White

Write-Host "`n" -ForegroundColor White

#############################################################################
# MAC/LINUX BASH VERSION
#############################################################################
# File: savvi_init.sh
# #!/bin/bash

PROJECT_PATH="${1:-$HOME/projects/savvi}"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         SAVVI - Cross-Platform Scaffold Launcher         ║"
echo "║  Sensitive • Allergic • Vegan • Vegetarian • Intolerant ║"
echo "╚═══════════════════════════════════════════════════════════╝"

if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="Mac"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    OS="Unknown"
fi

echo ""
echo "Detected OS: $OS"
echo "Target Project: $PROJECT_PATH"
echo ""

# Step 1: Run main scaffold
echo "[1/3] Running project scaffold..."
if [ -f "./savvi_scaffold_mac.sh" ]; then
    bash ./savvi_scaffold_mac.sh "$PROJECT_PATH"
    echo "✓ Scaffold complete"
else
    echo "✗ Error: savvi_scaffold_mac.sh not found in current directory"
    exit 1
fi

# Step 2: Initialize Python environment
echo ""
echo "[2/3] Setting up Python environment..."

if ! command -v python3 &> /dev/null; then
    echo "✗ Error: Python 3 not found"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  Install with: brew install python3"
    else
        echo "  Install with: sudo apt-get install python3 python3-venv"
    fi
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Python found: $PYTHON_VERSION"

cd "$PROJECT_PATH"

echo "  Creating virtual environment..."
python3 -m venv venv
echo "  ✓ Virtual environment created"

echo "  Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "  ✓ Dependencies installed"

# Step 3: Check for Tesseract
echo ""
echo "[3/3] Checking optional dependencies..."

if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version | head -n1)
    echo "✓ Tesseract found: $TESSERACT_VERSION"
else
    echo "ℹ️  Tesseract not found (optional for OCR)"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  To install: brew install tesseract"
    else
        echo "  To install: sudo apt-get install tesseract-ocr"
    fi
fi

# Summary
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                ✅ Setup Complete!                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"

echo ""
echo "📁 Project Structure: $PROJECT_PATH"
echo "📚 Documentation:"
echo "   • $PROJECT_PATH/README.md"
echo "   • $PROJECT_PATH/TODO.md"
echo "   • $PROJECT_PATH/cursor.md"

echo ""
echo "🚀 Quick Start:"
echo "   1. Edit: $PROJECT_PATH/.env"
echo "   2. Copy .env.template → .env and add your API keys"
echo "   3. cd $PROJECT_PATH"
echo "   4. source venv/bin/activate"
echo "   5. python src/main.py --help"

echo ""
echo "🔧 For Cursor IDE Development:"
echo "   cursor $PROJECT_PATH"
echo "   Then review cursor.md for development guide"

echo ""
