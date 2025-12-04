# SAVVI Project - README
## Sensitive • Allergic • Vegan • Vegetarian • Intolerant

**Repository**: https://github.com/Jsgordon420365/savvi  
**Status**: Phase 1A - Infrastructure (100% complete) ✅ | Overall: 25%  
**Last Updated**: 2025-12-03  
**Recent**: ✅ Phase 1A Complete - Configuration, Logging & Input Validation

### Mission
Transform restaurant PDF menus into personalized, dietary-safe documents that clearly indicate which dishes are safe, which can be modified, and which must be avoided based on individual dietary needs, allergies, and preferences.

### Problem Solved
- **Dietary Navigation Nightmare**: Users can't easily identify safe menu items
- **Language Barriers**: Ingredient information unclear across cuisines
- **Restaurant Communication**: No standard way to flag dietary needs
- **Data Gaps**: Menu PDFs lack ingredient details; guesswork required
- **Scalability**: Manual menu review is tedious and error-prone

### Solution Overview

SAVVI is a three-phase system:

#### Phase 1: MVP (Current)
- **Input**: Restaurant menu PDF
- **Processing**: 
  - PDF parsing & OCR
  - Dish extraction
  - Online recipe research (90% confidence threshold)
  - Allergen detection & flagging
- **Output**: Marked-up PDF with:
  - Color-coded safety levels
  - Ingredient confidence scores
  - Notes on unique/ambiguous items
  - Editable fields for staff/user input

#### Phase 2: Platform Enhancement
- User authentication & profiles
- Dietary preference management
- Restaurant database integration
- Dynamic menu generation per user

#### Phase 3: Full SaaS
- Restaurant admin dashboard
- Auto-menu processing
- Ingredient crowdsourcing
- API for integrations

### Technical Stack

**Backend**
- Python 3.10+
- FastAPI for REST API
- PostgreSQL for data persistence
- SQLAlchemy ORM

**PDF Processing**
- PyPDF2 (extraction)
- pdf2image (visualization)
- Pytesseract (OCR for scanned menus)
- ReportLab (PDF generation with annotations)

**Data & Search**
- Pandas (data manipulation)
- BeautifulSoup (web scraping)
- TextBlob (NLP analysis)
- NLTK (tokenization)

**Recipe Intelligence**
- Spoonacular API / Edamam API (fallback)
- Custom recipe database
- Ingredient matching engine

**Testing & Deployment**
- Pytest for unit/integration tests
- Docker for containerization
- GitHub Actions for CI/CD

### Project Structure

```
savvi/
├── src/
│   ├── core/
│   │   ├── menu_parser.py         # PDF extraction & parsing
│   │   ├── allergen_database.py   # Allergen & dietary rules
│   │   └── dietary_mapper.py      # User preference mapping
│   ├── processors/
│   │   ├── pdf_processor.py       # PDF handling
│   │   ├── recipe_searcher.py     # Online recipe lookup
│   │   ├── ingredient_analyzer.py # NLP analysis
│   │   └── marking_engine.py      # PDF annotation
│   ├── utils/
│   │   ├── config.py              # Configuration management
│   │   ├── logger.py              # Logging setup
│   │   └── validators.py          # Input validation
│   ├── api/
│   │   ├── main.py                # FastAPI application
│   │   ├── routes.py              # API endpoints
│   │   └── models.py              # Pydantic schemas
│   └── main.py                    # CLI entry point
├── data/
│   ├── recipes/                   # Cached recipe data
│   ├── allergens/                 # Allergen database
│   ├── uploaded_menus/            # User uploads
│   └── processed_menus/           # Generated outputs
├── config/
│   ├── savvi_config.yaml          # Configuration
│   └── allergen_rules.json        # Allergen definitions
├── tests/
│   ├── unit/                      # Unit tests
│   └── integration/               # Integration tests
├── docs/
│   ├── API.md                     # API documentation
│   └── ARCHITECTURE.md            # System design
├── scripts/
│   └── setup_db.py                # Database initialization
├── requirements.txt               # Python dependencies
├── .env.template                  # Environment template
├── README.md                      # This file
├── TODO.md                        # Task tracking
└── cursor.md                      # Cursor AI guidance
```

### Key Features

1. **Multi-Level Safety Classification**
   - 🟢 **Safe**: Verified safe or naturally compliant
   - 🟡 **Caution**: Can be made safe with modifications
   - 🔴 **Avoid**: Contains flagged allergens/preferences
   - ⚠️ **Unknown**: Insufficient ingredient data (flagged for staff verification)

2. **Intelligent Recipe Research**
   - Searches online databases for common recipes
   - Flags items with <90% confidence
   - Identifies alternative ingredients
   - Tracks research metadata

3. **Unique Item Management**
   - Special section for "cutesy" or unique names
   - Prompts for restaurant staff clarification
   - Editable notes field for future reference

4. **User Profiles** (Phase 2+)
   - Multiple dietary preferences
   - Custom sensitivity levels
   - Preference history
   - Restaurant-specific notes

5. **Editable PDF Output**
   - Form fields for staff notes
   - Version tracking
   - Comments & annotations
   - Export capability

### MVP Workflow

```
1. User uploads restaurant menu PDF
   ↓
2. SAVVI extracts text & images
   ↓
3. For each dish:
   a) Parse name & description
   b) Search online for common recipe/ingredients
   c) Cross-reference with allergen database
   d) Generate confidence scores
   ↓
4. Categorize dishes:
   - Safe (90%+ confidence, no allergens)
   - Caution (modifiable or partial matches)
   - Avoid (contains flagged ingredients)
   - Unknown (needs clarification)
   ↓
5. Generate marked PDF with:
   - Color coding
   - Inline notes
   - Special section for unknowns
   ↓
6. Output editable PDF for user/staff
```

### Configuration

Edit `config/savvi_config.yaml` to:
- Define allergen severity levels
- Set dietary preference rules
- Adjust recipe search thresholds
- Configure output formatting

Edit `.env` file for:
- Database credentials
- API keys
- File paths
- Logging levels

### Getting Started

1. **Run Scaffolding Script** ✅ COMPLETED (2025-12-03)
   ```powershell
   .\savvi_scaffold.ps1
   # Project created at: C:\Users\Gordo\projects\savvi
   ```

2. **Setup Environment** ✅ COMPLETED (2025-12-03)
   ```powershell
   cd $env:USERPROFILE\projects\savvi
   cp .env.template .env  # ✅ Ready
   python -m venv venv  # ✅ Done
   .\venv\Scripts\Activate.ps1  # ✅ Done
   pip install -r requirements.txt  # ✅ Ready
   ```

3. **Configure**
   - Update `.env` with your settings
   - Configure API keys for recipe search
   - Review `config/savvi_config.yaml`

4. **Test MVP**
   ```powershell
   pytest tests/
   python src/main.py --help
   ```

### Development Phases

**Phase 1 (MVP): Menu Parsing & Marking** [CURRENT - 25% Complete] (Updated: 251203213515)
- [x] Project scaffolding & configuration ✅ (251203120000)
- [x] Configuration management module (Task 1.A.1) ✅ (251203143000)
- [x] Logging setup (Task 1.A.2) ✅ (251203151500)
- [x] Input validation (Task 1.A.3) ✅ (251203160000)
- [x] PDF text extraction (Task 1.B.1) ✅ (251203173000)
- [x] PDF OCR for scanned menus (Task 1.B.2) ✅ (251203213500)
- [ ] Dish parsing & normalization
- [ ] Recipe search integration
- [ ] Allergen detection
- [ ] PDF marking engine
- [ ] CLI interface

**Phase 2: User Platform** [PLANNED]
- [ ] User authentication
- [ ] Profile management
- [ ] Dietary preference storage
- [ ] FastAPI REST endpoints
- [ ] Dynamic menu generation
- [ ] Web UI (React/Next.js)

**Phase 3: SaaS Launch** [FUTURE]
- [ ] Restaurant admin dashboard
- [ ] Database schema for restaurants
- [ ] Ingredient crowdsourcing
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] API commercialization

### Allergen Database

Organized by severity:

**Critical** (can cause severe reactions):
- Peanuts, Tree nuts, Shellfish, Fish, Sesame, Milk, Eggs, Wheat, Soy

**Moderate** (significant impact):
- Gluten, Cross-contamination traces

**Mild** (dietary preferences):
- High sodium, Spicy, Processed sugar

**Dietary Flags**:
- Vegan: No animal products
- Vegetarian: No meat/fish/shellfish
- Gluten-free: No wheat/barley/rye
- Keto: No grains/sugar/legumes

### Recipe Search Strategy

1. **Primary**: Spoonacular API (comprehensive, structured)
2. **Fallback**: Custom web scraper (AllRecipes, Food Network)
3. **Validation**: Cross-reference multiple sources
4. **Confidence**: Only flag items >90% matched
5. **Tracking**: Log search metadata for ML training

### API Endpoints (Phase 2+)

```
POST   /api/v1/menu/process        # Upload & process menu
GET    /api/v1/menu/{id}           # Retrieve processed menu
POST   /api/v1/user/profile        # Create user profile
GET    /api/v1/user/menu/{id}      # Get personalized menu
PUT    /api/v1/dish/{id}/note      # Add staff note
```

### Performance Targets

- **MVP**: 5-minute processing for 20-page menu
- **Phase 2**: Sub-30-second personalization per user
- **Phase 3**: Real-time ingredient updates

### Testing Strategy

- **Unit Tests**: Individual components (parsers, validators)
- **Integration Tests**: End-to-end workflow (PDF → marked PDF)
- **Data Tests**: Recipe search accuracy, allergen detection

### Deployment

**Development**:
```powershell
python src/main.py
```

**Production** (Phase 2+):
```bash
docker build -t savvi .
docker run -p 8000:8000 savvi
```

### Contributing

See [TODO.md](TODO.md) for current tasks and phases.

### License

MIT License - Open source for community contribution

### Support & Questions

For setup issues or feature requests, check the [Cursor guidance](cursor.md) for AI-assisted development or consult the [Architecture docs](docs/ARCHITECTURE.md).

---

**SAVVI: Empowering dietary autonomy through intelligent menu analysis** ✨
