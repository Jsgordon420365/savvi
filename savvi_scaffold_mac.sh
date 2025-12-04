#!/bin/bash
# SAVVI Project Scaffold Generator - Bash Edition (Mac/Linux)
# Creates complete project structure for Mac and Linux systems
# Usage: bash savvi_scaffold_mac.sh

PROJECT_PATH="${1:-$HOME/projects/savvi}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║         SAVVI Project Scaffold Generator                   ║${NC}"
    echo -e "${CYAN}║  Sensitive • Allergic • Vegan • Vegetarian • Intolerant   ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
}

print_step() {
    echo -e "\n${BLUE}[*] $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Start
print_header
echo -e "\nTarget: ${YELLOW}$PROJECT_PATH${NC}\n"

# Check if directory exists
if [ -d "$PROJECT_PATH" ]; then
    print_warning "Directory exists: $PROJECT_PATH"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
else
    print_step "Creating root directory..."
    mkdir -p "$PROJECT_PATH"
    print_success "Created: $PROJECT_PATH"
fi

# Create directory structure
print_step "Creating directory structure..."
DIRS=(
    "src"
    "src/core"
    "src/processors"
    "src/utils"
    "src/api"
    "data"
    "data/recipes"
    "data/allergens"
    "data/uploaded_menus"
    "data/processed_menus"
    "tests"
    "tests/unit"
    "tests/integration"
    "docs"
    "scripts"
    "config"
    "output"
    "logs"
)

for dir in "${DIRS[@]}"; do
    full_path="$PROJECT_PATH/$dir"
    if [ ! -d "$full_path" ]; then
        mkdir -p "$full_path"
        print_success "$dir"
    fi
done

# Create __init__.py files
print_step "Creating Python package markers..."
for dir in "src" "src/core" "src/processors" "src/utils" "src/api" "tests" "tests/unit" "tests/integration"; do
    touch "$PROJECT_PATH/$dir/__init__.py"
done
print_success "Python package markers created"

# Create requirements.txt
print_step "Creating Python dependencies..."
cat > "$PROJECT_PATH/requirements.txt" << 'EOF'
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
EOF
print_success "requirements.txt created"

# Create .env template
print_step "Creating environment configuration..."
cat > "$PROJECT_PATH/.env.template" << 'EOF'
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
TESSERACT_PATH=/usr/local/bin/tesseract

# API Configuration
API_PORT=8000
API_HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Recipe Search
RECIPE_API_KEY=your_recipe_api_key
INGREDIENT_CONFIDENCE_THRESHOLD=0.90

# File Storage
UPLOAD_DIR=data/uploaded_menus
OUTPUT_DIR=data/processed_menus
LOG_DIR=logs
EOF
print_success ".env.template created"

# Create config YAML
print_step "Creating configuration file..."
cat > "$PROJECT_PATH/config/savvi_config.yaml" << 'EOF'
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
EOF
print_success "savvi_config.yaml created"

# Create .gitignore
print_step "Creating Git ignore rules..."
cat > "$PROJECT_PATH/.gitignore" << 'EOF'
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
EOF
print_success ".gitignore created"

# Create setup script
print_step "Creating setup script..."
cat > "$PROJECT_PATH/setup.sh" << 'EOF'
#!/bin/bash
# SAVVI Setup Script - Run after scaffold

set -e

echo "🚀 SAVVI Setup"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate it
echo "Activating venv..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if missing
if [ ! -f .env ]; then
    echo "Creating .env from template..."
    cp .env.template .env
    echo "⚠️  IMPORTANT: Edit .env with your settings (API keys, paths, etc.)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your configuration"
echo "2. For OCR support:"
echo "   - Mac: brew install tesseract"
echo "   - Linux: sudo apt-get install tesseract-ocr"
echo "3. source venv/bin/activate"
echo "4. pytest tests/ -v"
EOF
chmod +x "$PROJECT_PATH/setup.sh"
print_success "setup.sh created"

# Create setup script (Mac specific)
cat > "$PROJECT_PATH/setup_mac.sh" << 'EOF'
#!/bin/bash
# SAVVI Setup Script for Mac

set -e

echo "🚀 SAVVI Setup for Mac"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Install from https://brew.sh"
    exit 1
fi

# Install Tesseract
echo "Installing Tesseract..."
brew install tesseract

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate it
echo "Activating venv..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if missing
if [ ! -f .env ]; then
    echo "Creating .env from template..."
    cp .env.template .env
    echo "⚠️  IMPORTANT: Edit .env with your settings (API keys, paths, etc.)"
    echo "For Mac, Tesseract path should be: /usr/local/bin/tesseract"
fi

echo ""
echo "✅ Mac setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your configuration"
echo "2. source venv/bin/activate"
echo "3. pytest tests/ -v"
EOF
chmod +x "$PROJECT_PATH/setup_mac.sh"
print_success "setup_mac.sh created"

# Create .gitkeep files to ensure empty directories are tracked
print_step "Creating directory markers..."
for dir in "data/recipes" "data/allergens" "data/uploaded_menus" "data/processed_menus" "logs" "output"; do
    touch "$PROJECT_PATH/$dir/.gitkeep"
done
print_success "Directory markers created"

# Summary
echo ""
print_header
echo -e "\n${GREEN}✅ Scaffolding complete!${NC}\n"
echo -e "${YELLOW}📁 Project location:${NC} $PROJECT_PATH"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. cd $PROJECT_PATH"
echo "2. bash setup_mac.sh  (or setup.sh for Linux)"
echo "3. Edit .env with your configuration"
echo "4. source venv/bin/activate"
echo "5. pytest tests/ -v"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo "  • README.md - Project overview"
echo "  • TODO.md - Task tracking"
echo "  • cursor.md - AI development guide"
echo ""
echo -e "${CYAN}For Windows, use: savvi_scaffold.ps1${NC}"
echo ""
