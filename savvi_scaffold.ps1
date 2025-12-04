# SAVVI Project Scaffold Generator - PowerShell Edition
# Creates complete project structure for Windows 11
# Usage: ./savvi_scaffold.ps1

param(
    [string]$ProjectPath = "$env:USERPROFILE\projects\savvi"
)

# Color output helper
function Write-ColorOutput($message, $color = "Green") {
    Write-Host $message -ForegroundColor $color
}

Write-ColorOutput "================================================================" "Cyan"
Write-ColorOutput "         SAVVI Project Scaffold Generator                   " "Cyan"
Write-ColorOutput "  Sensitive * Allergic * Vegan * Vegetarian * Intolerant   " "Cyan"
Write-ColorOutput "================================================================" "Cyan"

Write-ColorOutput "`nTarget: $ProjectPath`n" "Yellow"

# Create root directory
if (-not (Test-Path $ProjectPath)) {
    New-Item -ItemType Directory -Path $ProjectPath -Force | Out-Null
    Write-ColorOutput "[OK] Created root directory: $ProjectPath" "Green"
} else {
    Write-ColorOutput "[OK] Root directory exists" "Yellow"
}

# Directory structure
$directories = @(
    "src",
    "src\core",
    "src\processors",
    "src\utils",
    "src\api",
    "data",
    "data\recipes",
    "data\allergens",
    "data\uploaded_menus",
    "data\processed_menus",
    "tests",
    "tests\unit",
    "tests\integration",
    "docs",
    "scripts",
    "config",
    "output",
    "logs"
)

Write-ColorOutput "`n[1/5] Creating directory structure..." "Cyan"
foreach ($dir in $directories) {
    $fullPath = Join-Path $ProjectPath $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-ColorOutput "  [OK] $dir" "Green"
    }
}

# Python requirements file
Write-ColorOutput "`n[2/5] Creating Python configuration..." "Cyan"
$requirementsPath = Join-Path $ProjectPath "requirements.txt"
$requirements = @"
# SAVVI - Dietary Menu Analysis System
# Core Dependencies
PyPDF2==3.0.1
pdf2image==1.16.3
pillow==10.0.1
pytesseract==0.3.10
python-dotenv==1.0.0
reportlab==4.0.7

# Data Processing
pandas==2.0.3
numpy==1.24.3
requests==2.31.0

# Database & API
sqlalchemy==2.0.21
fastapi==0.103.0
uvicorn==0.23.2
psycopg2-binary==2.9.7
asyncpg==0.29.0
pydantic==2.5.0
pydantic-settings==2.1.0

# NLP & Recipe Analysis
textblob==0.17.1
nltk==3.8.1

# Search & Scraping
beautifulsoup4==4.12.2
selenium==4.13.0
lxml==4.9.3

# Testing
pytest==7.4.0
pytest-cov==4.1.0
pytest-asyncio==0.21.1
httpx==0.25.2

# Utilities
pyyaml==6.0.1
click==8.1.7
colorama==0.4.6
"@
Set-Content -Path $requirementsPath -Value $requirements
Write-ColorOutput "  [OK] requirements.txt created" "Green"

# Create .env template
Write-ColorOutput "`n[3/5] Creating configuration templates..." "Cyan"
$envPath = Join-Path $ProjectPath ".env.template"
$envContent = @"
# SAVVI Environment Configuration
# Copy this file to .env and fill in actual values

# Application
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Database
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=savvi_db
DB_USER=savvi_user
DB_PASSWORD=your_secure_password

# PDF Processing
PDF_MAX_SIZE_MB=50
OCR_ENABLED=true
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe

# API Configuration
API_PORT=8000
API_HOST=0.0.0.0
CORS_ORIGINS="http://localhost:3000,http://localhost:8000"

# Recipe Search
RECIPE_API_KEY=your_recipe_api_key
INGREDIENT_CONFIDENCE_THRESHOLD=0.90

# File Storage
UPLOAD_DIR=data/uploaded_menus
OUTPUT_DIR=data/processed_menus
LOG_DIR=logs
"@
Set-Content -Path $envPath -Value $envContent
Write-ColorOutput "  [OK] .env.template created" "Green"

# Create config YAML
$configPath = Join-Path $ProjectPath "config\savvi_config.yaml"
$configContent = @"
# SAVVI Configuration File

application:
  name: SAVVI
  version: 0.1.0
  environment: development

pdf_processing:
  max_file_size_mb: 50
  supported_formats:
    - pdf
    - image
  ocr:
    enabled: true
    language: eng
    quality_threshold: 0.75

allergen_categories:
  critical:
    - peanuts
    - tree nuts
    - shellfish
    - fish
    - sesame
    - milk
    - eggs
    - wheat
    - soy
  moderate:
    - gluten
    - processed in shared facilities
  mild:
    - high sodium
    - spicy

dietary_preferences:
  vegan:
    excludes: []
    flags: [animal_product, dairy, eggs, honey]
  vegetarian:
    excludes: []
    flags: [meat, poultry, fish, shellfish]
  gluten_free:
    excludes: [wheat, barley, rye]
    flags: [cross_contamination]
  keto:
    excludes: [grains, sugar, legumes]
    flags: [carb_heavy]

recipe_search:
  confidence_threshold: 0.90
  max_results: 5
  timeout_seconds: 10

output:
  format: pdf_marked
  include_confidence_scores: true
  include_recipe_notes: true
  editable_fields: true
"@
Set-Content -Path $configPath -Value $configContent
Write-ColorOutput "  [OK] savvi_config.yaml created" "Green"

# Create .gitignore
Write-ColorOutput "`n[4/5] Creating project files..." "Cyan"
$gitignorePath = Join-Path $ProjectPath ".gitignore"
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
.env.*.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
logs/
*.log

# Data
data/uploaded_menus/*
data/processed_menus/*
*.pdf

# Temporary
temp/
tmp/
*.tmp
"@
Set-Content -Path $gitignorePath -Value $gitignoreContent
Write-ColorOutput "  [OK] .gitignore created" "Green"

Write-ColorOutput "`n[5/5] Project structure ready!" "Cyan"
Write-ColorOutput "`nNext steps:" "Yellow"
Write-ColorOutput "1. cd $ProjectPath" "White"
Write-ColorOutput "2. Copy .env.template to .env and configure" "White"
Write-ColorOutput "3. python -m venv venv" "White"
Write-ColorOutput "4. .\venv\Scripts\Activate.ps1" "White"
Write-ColorOutput "5. pip install -r requirements.txt" "White"
Write-ColorOutput "6. Review cursor.md for AI-assisted development" "White"

Write-ColorOutput "`n[OK] Scaffolding complete!" "Green"
