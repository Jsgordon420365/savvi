# 🚀 SAVVI Complete Deliverable Package

## Project: Sensitive • Allergic • Vegan • Vegetarian • Intolerant
### A Dietary Menu Intelligence System

---

## 📦 WHAT YOU'RE RECEIVING

This is a **complete, production-ready scaffolding and development package** for building SAVVI, a sophisticated dietary menu analysis system. Everything is included to go from zero to working MVP.

### Components Included:

1. **Scaffolding Scripts** (Platform-specific)
   - `savvi_scaffold.ps1` - Windows PowerShell
   - `savvi_scaffold_mac.sh` - Mac/Linux Bash
   - `LAUNCH_GUIDE.md` - Platform-agnostic instructions

2. **Project Documentation**
   - `README.md` - Complete project overview
   - `TODO.md` - Detailed task tracking and milestones
   - `cursor.md` - AI-assisted development guide

3. **Configuration Templates**
   - `.env.template` - Environment variables
   - `config/savvi_config.yaml` - Application configuration
   - `requirements.txt` - Python dependencies

4. **Complete Directory Structure**
   - All necessary folders pre-created
   - Python package markers (\_\_init\_\_.py)
   - Data directories with .gitkeep files

---

## ⚡ QUICK START (5 MINUTES)

### Windows 11 Users:

```powershell
# 1. Open PowerShell (Admin recommended)
cd ~\Desktop\savvi-deliverable

# 2. Run the scaffold
.\savvi_scaffold.ps1

# 3. Done! Project created at ~\projects\savvi
cd $env:USERPROFILE\projects\savvi

# 4. Open in Cursor IDE
cursor .

# 5. Follow cursor.md for development
```

### Mac/Linux Users:

```bash
# 1. Open Terminal
cd ~/Desktop/savvi-deliverable

# 2. Run the scaffold
bash savvi_scaffold_mac.sh

# 3. Done! Project created at ~/projects/savvi
cd ~/projects/savvi

# 4. Open in Cursor IDE
cursor .

# 5. Follow cursor.md for development
```

---

## 📋 FILE MANIFEST

### Scaffolding & Initialization
| File | Purpose | Platform |
|------|---------|----------|
| `savvi_scaffold.ps1` | Create project structure + config | Windows |
| `savvi_scaffold_mac.sh` | Create project structure + config | Mac/Linux |
| `LAUNCH_GUIDE.md` | Setup instructions (all platforms) | All |

### Documentation
| File | Purpose | Size |
|------|---------|------|
| `README.md` | Project overview, problem statement, technical stack | 8KB |
| `TODO.md` | Phase 1-3 tasks, sprints, completion tracking | 15KB |
| `cursor.md` | AI development guide with per-task prompts | 25KB |

### Configuration
| File | Purpose | Auto-created |
|------|---------|--------------|
| `.env.template` | Environment variable template | ✓ Yes |
| `config/savvi_config.yaml` | Allergen rules, preferences | ✓ Yes |
| `.gitignore` | Git ignore patterns | ✓ Yes |
| `requirements.txt` | Python dependencies | ✓ Yes |

---

## 🎯 PROJECT OVERVIEW

### The Problem
Restaurant menus don't list complete ingredients. For people with dietary restrictions (allergies, vegan, gluten-free, etc.), it's a nightmare to figure out what's safe to eat.

### The Solution
**SAVVI** transforms restaurant menu PDFs into personalized dietary documents:
- Marks safe dishes (🟢)
- Marks caution dishes (🟡)
- Marks dishes to avoid (🔴)
- Flags uncertain dishes (⚠️)
- Researches recipes online to find likely ingredients
- Outputs marked PDF with editable fields

### Three Phases

**Phase 1 (MVP)**: CLI tool that processes individual PDFs
- User runs: `python src/main.py --menu menu.pdf --vegan --gluten-free`
- Output: Marked PDF highlighting safe dishes

**Phase 2 (Platform)**: Web interface + user profiles
- Upload menus
- Save dietary preferences
- Auto-personalize for each user
- REST API

**Phase 3 (SaaS)**: Restaurant integration
- Restaurant admin dashboard
- Auto-process new menus
- Ingredient crowdsourcing
- Subscription model

---

## 🛠️ TECHNICAL STACK

**Language**: Python 3.10+
**PDF Processing**: PyPDF2, pdf2image, Pytesseract (OCR)
**Recipe Research**: Spoonacular API + web scraping
**Data Analysis**: Pandas, NLTK, TextBlob
**API (Phase 2)**: FastAPI
**Database**: PostgreSQL (Phase 2+)
**Testing**: Pytest
**CLI**: Click

**Key Dependencies** (in requirements.txt):
- PyPDF2 - PDF text extraction
- pytesseract - OCR for scanned menus
- requests - API calls
- pandas - Data manipulation
- beautifulsoup4 - Web scraping
- nltk - NLP analysis

---

## 📁 GENERATED PROJECT STRUCTURE

After running the scaffold, you'll have:

```
~/projects/savvi/
├── src/
│   ├── core/
│   │   ├── menu_parser.py         ← Extract PDF text
│   │   ├── allergen_database.py   ← Allergen rules
│   │   └── dietary_mapper.py      ← User preferences
│   ├── processors/
│   │   ├── pdf_processor.py       ← OCR & image handling
│   │   ├── recipe_searcher.py     ← Online lookup
│   │   ├── ingredient_analyzer.py ← NLP analysis
│   │   └── marking_engine.py      ← PDF annotation
│   ├── utils/
│   │   ├── config.py              ← Config loading
│   │   ├── logger.py              ← Logging
│   │   └── validators.py          ← Input validation
│   ├── api/                       ← FastAPI (Phase 2)
│   └── main.py                    ← CLI entry point
├── tests/
│   ├── unit/                      ← Unit tests
│   └── integration/               ← E2E tests
├── config/
│   ├── savvi_config.yaml
│   └── allergen_rules.json
├── data/
│   ├── uploaded_menus/
│   ├── processed_menus/
│   ├── recipes/ (cache)
│   └── allergens/
├── docs/
│   ├── API.md
│   └── ARCHITECTURE.md
├── requirements.txt
├── .env.template
├── .gitignore
├── README.md
├── TODO.md
└── cursor.md
```

---

## 🚀 DEVELOPMENT WORKFLOW

### Step 1: Initialize Project
```bash
# Windows
.\savvi_scaffold.ps1

# Mac/Linux
bash savvi_scaffold_mac.sh
```

### Step 2: Configure Environment
```bash
cd ~/projects/savvi
cp .env.template .env
# Edit .env with:
# - Spoonacular API key
# - Tesseract path (if using OCR)
# - Other settings
```

### Step 3: Create Python Environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
.\venv\Scripts\Activate.ps1  # Windows

pip install -r requirements.txt
```

### Step 4: Open in Cursor IDE
```bash
cursor .
```

### Step 5: Follow Development Guide
- Read `cursor.md` for detailed task breakdown
- Follow Phase 1A → 1B → 1C → ... → 1I
- Use provided Cursor prompts for each task
- Run tests after each module

### Step 6: Validate MVP
- Run `pytest tests/ -v`
- Test with real restaurant menu PDFs
- Generate marked PDFs
- Verify output quality

---

## 📊 PHASE BREAKDOWN

### Phase 1: MVP (4-5 weeks, ~140 hours)
**Goal**: Working CLI tool
**Deliverable**: `python src/main.py --menu menu.pdf --vegan`

**Key Tasks**:
- [ ] PDF text extraction (native + OCR)
- [ ] Dish parsing & normalization
- [ ] Recipe research integration
- [ ] Allergen detection
- [ ] PDF marking/annotation
- [ ] CLI interface
- [ ] Testing & validation

### Phase 2: Platform (6-8 weeks, ~200 hours)
**Goal**: Web-based user platform
**Deliverable**: Web app with user profiles

**Key Tasks**:
- [ ] User authentication
- [ ] FastAPI REST endpoints
- [ ] Database schema
- [ ] React/Next.js frontend
- [ ] Personalized menu generation

### Phase 3: SaaS (8-10+ weeks, ~300 hours)
**Goal**: Commercialized platform
**Deliverable**: Subscription service

**Key Tasks**:
- [ ] Restaurant admin dashboard
- [ ] Ingredient crowdsourcing
- [ ] Analytics & reporting
- [ ] Mobile app
- [ ] API commercialization

---

## 🔧 CONFIGURATION GUIDE

### .env File (Essential)
```bash
# API Keys
SPOONACULAR_API_KEY=your_api_key_here

# PDF Processing
TESSERACT_PATH=/usr/local/bin/tesseract  # Mac
# or
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe  # Windows

# Paths
UPLOAD_DIR=data/uploaded_menus
OUTPUT_DIR=data/processed_menus
LOG_DIR=logs

# Settings
INGREDIENT_CONFIDENCE_THRESHOLD=0.90
PDF_MAX_SIZE_MB=50
OCR_ENABLED=true
DEBUG=true
```

### savvi_config.yaml
Pre-configured with:
- Allergen definitions (critical, moderate, mild)
- Dietary preference rules (vegan, vegetarian, gluten-free, keto)
- Recipe search settings
- PDF output formatting

Edit to customize allergen categories or dietary rules.

---

## 📝 KEY DOCUMENTS TO READ

1. **Start Here**: `README.md`
   - Project vision & problem statement
   - Tech stack overview
   - Getting started guide

2. **Track Progress**: `TODO.md`
   - Detailed task breakdown
   - Completion checkboxes
   - Effort estimates
   - Dependencies

3. **Development**: `cursor.md`
   - Phase-by-phase breakdown
   - Specific tasks with Cursor prompts
   - Code standards
   - Validation checkpoints

---

## 💡 CORE CONCEPTS

### Safety Classification
- **🟢 Safe**: Verified no allergens, 90%+ confidence
- **🟡 Caution**: Needs clarification or can be modified
- **🔴 Avoid**: Contains flagged allergen/preference exclusion
- **⚠️ Unknown**: Insufficient ingredient data, needs server clarification

### Confidence Scoring
- Online recipe search must match 90%+ threshold
- Fuzzy matching for ingredient names
- Multiple sources validated
- Cross-contamination risks flagged

### Dietary Profiles
- **Vegan**: No animal products
- **Vegetarian**: No meat/fish/shellfish
- **Gluten-free**: No wheat/barley/rye
- **Keto**: No grains/sugar/legumes
- **Allergies**: Custom allergen lists

---

## 🧪 TESTING

### Run Unit Tests
```bash
pytest tests/unit/ -v
```

### Run Integration Tests
```bash
pytest tests/integration/ -v
```

### Run All Tests with Coverage
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Test with Real Menu
```bash
python src/main.py --menu ~/menu.pdf --vegan --gluten-free --verbose
```

---

## 🚨 TROUBLESHOOTING

### Issue: "Python not found"
```bash
# Install Python 3.10+
# Windows: python-3.10.msi from python.org
# Mac: brew install python3
# Linux: sudo apt-get install python3
```

### Issue: "Tesseract not found"
```bash
# Windows: choco install tesseract
# Mac: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
```

### Issue: "API key invalid"
1. Sign up at https://spoonacular.com/food-api
2. Copy API key
3. Add to .env: SPOONACULAR_API_KEY=your_key

### Issue: PDF markup not showing
- Check ReportLab is installed: `pip list | grep reportlab`
- Try PDF-A format instead of standard PDF
- See cursor.md for PDF handling alternatives

---

## 📞 SUPPORT & RESOURCES

### Provided Resources
- ✅ Scaffolding scripts (PowerShell + Bash)
- ✅ Complete documentation
- ✅ Configuration templates
- ✅ Cursor IDE development guide
- ✅ Task breakdown with prompts
- ✅ Testing framework setup

### External Resources
- **Spoonacular API**: https://spoonacular.com/food-api
- **PyPDF2 Docs**: https://github.com/py-pdf/PyPDF2
- **Pytesseract**: https://github.com/madmaze/pytesseract
- **FastAPI**: https://fastapi.tiangolo.com/
- **Cursor IDE**: https://cursor.com/

---

## ✨ HIGHLIGHTS

### What Makes This Special

1. **Production-Ready Scaffolding**
   - All necessary files pre-configured
   - Best practices built-in
   - Cross-platform support

2. **Comprehensive Documentation**
   - README, TODO, cursor.md all included
   - Task-by-task breakdown
   - Cursor IDE prompts for AI assistance

3. **Scalable Architecture**
   - MVP → Platform → SaaS roadmap
   - Modular design
   - Extension points documented

4. **Developer-Friendly**
   - Clear directory structure
   - Type hints throughout
   - Pytest testing framework
   - Configuration-driven

5. **Real-World Focus**
   - Handles scanned PDFs (OCR)
   - Online recipe validation
   - Confidence scoring
   - Allergen cross-contamination

---

## 🎓 LEARNING PATH

1. **Week 1**: Understand the problem (read README.md)
2. **Week 1-2**: Set up environment, run scaffold
3. **Week 2-3**: Follow cursor.md Phase 1A-1C
4. **Week 3-4**: Follow cursor.md Phase 1D-1F
5. **Week 4-5**: Follow cursor.md Phase 1G-1I
6. **Week 5+**: Begin Phase 2 (web platform)

---

## 🎯 SUCCESS CRITERIA

### MVP (Phase 1) Complete When:
- ✅ Extract text from PDFs >95% accuracy
- ✅ Parse ≥80% of menu items
- ✅ Research recipes for ≥70% of dishes
- ✅ Correctly classify dishes in manual testing
- ✅ Process 20-page menu in <5 minutes
- ✅ All tests passing
- ✅ CLI working with --help, --vegan, etc.

### Phase 2 Complete When:
- ✅ Users can create accounts
- ✅ Web UI for PDF upload
- ✅ Personalized menus generated per user
- ✅ ≥100 users registered
- ✅ API response <1 second

### Phase 3 Complete When:
- ✅ Restaurants using platform
- ✅ Ingredient crowdsourcing working
- ✅ ≥10,000 users
- ✅ Revenue model active

---

## 📄 LICENSE & ATTRIBUTION

This deliverable package is provided as a complete development scaffold for the SAVVI project. All scripts, documentation, and configurations are ready for immediate use and modification.

---

## 🚀 NEXT STEPS

1. **Extract this archive** to your desired location
2. **Run the scaffold script**:
   - Windows: `.\savvi_scaffold.ps1`
   - Mac/Linux: `bash savvi_scaffold_mac.sh`
3. **Read the documentation**:
   - Start with README.md
   - Then cursor.md for development
4. **Configure environment**:
   - Edit .env with your API keys
   - Install Tesseract if needed
5. **Open in Cursor IDE**:
   - `cursor ~/projects/savvi`
   - Follow Phase 1 tasks

---

**SAVVI: Empowering dietary autonomy through intelligent menu analysis** ✨

*Created: 2025-12-03*
*Version: 1.0.0*
*Status: MVP Scaffolding Complete - Ready for Development*
