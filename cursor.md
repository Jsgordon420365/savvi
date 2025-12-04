# SAVVI Project - Cursor IDE Development Guide

## 🎯 Purpose & Context

This document guides **Cursor IDE** (with Claude's advanced capabilities) through systematic development of the SAVVI system. It leverages Cursor's **file system access**, **MCP servers**, and **custom tool capabilities** to accelerate development while maintaining architectural integrity.

**Project Goal**: Build an MVP CLI tool that transforms restaurant menu PDFs into personalized, allergen-safe documents.

---

## 📋 HOW TO USE THIS GUIDE

### For Each Development Phase:
1. **Read the Phase Overview** - Understand objectives & dependencies
2. **Review Code Standards** - Ensure consistency
3. **Follow Task Sequence** - Tasks build on each other
4. **Use Cursor Commands** - Leverage IDE capabilities
5. **Validate Outputs** - Test before committing

### Cursor Capabilities You'll Use:
- ✅ File system access (read/write/create)
- ✅ Code generation & completion
- ✅ Test file generation
- ✅ Documentation generation
- ✅ Refactoring & optimization
- ✅ Multi-file awareness (view entire project structure)
- ✅ Error analysis & debugging

---

## 🚀 QUICK START

### Initial Setup (Do This First)

```bash
# 1. Run scaffold script (Windows)
cd $env:USERPROFILE\projects
.\savvi\savvi_scaffold.ps1

# 2. Create virtual environment
cd savvi
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.template .env
# Edit .env with your settings

# 5. Install Tesseract (Windows)
choco install tesseract

# 6. Open project in Cursor
cursor .
```

### Ask Cursor to Verify Setup:
```
"Verify the project structure is complete and all files exist. 
Create a verification script that checks all dependencies."
```

---

## 📁 PROJECT STRUCTURE REFERENCE

Keep this structure in mind as you navigate:

```
savvi/
├── src/
│   ├── core/              # Business logic
│   │   ├── __init__.py
│   │   ├── menu_parser.py         ⬅️ Extract text from PDFs
│   │   ├── allergen_database.py   ⬅️ Allergen rules & definitions
│   │   └── dietary_mapper.py      ⬅️ Map dishes to user preferences
│   ├── processors/        # Data transformation
│   │   ├── __init__.py
│   │   ├── pdf_processor.py       ⬅️ Handle PDF images & OCR
│   │   ├── recipe_searcher.py     ⬅️ Online recipe lookup
│   │   ├── ingredient_analyzer.py ⬅️ NLP analysis
│   │   └── marking_engine.py      ⬅️ Generate marked PDFs
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py              ⬅️ Configuration loading
│   │   ├── logger.py              ⬅️ Logging setup
│   │   └── validators.py          ⬅️ Input validation
│   ├── api/               # REST API (Phase 2)
│   │   ├── main.py
│   │   ├── routes.py
│   │   └── models.py
│   └── main.py            ⬅️ CLI entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── config/
│   ├── savvi_config.yaml  ⬅️ Allergen rules, preferences
│   └── allergen_rules.json
├── data/
│   ├── recipes/
│   ├── allergens/
│   ├── uploaded_menus/
│   └── processed_menus/
└── requirements.txt
```

**Key Files to Edit**: Look for `⬅️` markers above

---

## 🎓 PHASE 1: MVP DEVELOPMENT

### PHASE 1 OVERVIEW

**Goal**: Build a working CLI tool that:
1. Accepts a restaurant menu PDF
2. Extracts dishes and descriptions
3. Researches recipes online
4. Detects allergens
5. Outputs a marked-up PDF

**Timeline**: 4-5 weeks (~140 hours estimated)
**Success Criteria**:
- Extract text with >95% accuracy
- Identify ≥80% of menu items
- Classify dishes correctly in manual testing
- Process 20-page menu in <5 minutes

---

## 🔧 PHASE 1A: CORE INFRASTRUCTURE

### Task 1.A.1: Configuration Management

**Goal**: Load environment variables & config files properly

**Cursor Commands**:
```
1. Open: src/utils/config.py
2. Read: .env.template, config/savvi_config.yaml
3. Ask Cursor:

"Create a Config class in src/utils/config.py that:
- Loads environment variables from .env file
- Loads YAML configuration from config/savvi_config.yaml
- Provides property accessors for all settings
- Validates required settings on init
- Includes comprehensive docstrings

Include methods:
- get_allergen_rules() -> dict
- get_dietary_preferences() -> dict
- get_pdf_settings() -> dict
- validate_settings() -> bool

Use dataclasses or pydantic for structure.
Create unit tests in tests/unit/test_config.py"
```

**Validation**:
```bash
# Run config tests
pytest tests/unit/test_config.py -v

# Check manual load
python -c "from src.utils.config import Config; c = Config(); print(c.get_allergen_rules())"
```

### Task 1.A.2: Logging Setup

**Goal**: Structured logging throughout application

**Cursor Commands**:
```
1. Open: src/utils/logger.py
2. Ask Cursor:

"Create a logging utility in src/utils/logger.py that:
- Sets up structured logging (console + file)
- Supports debug, info, warning, error levels
- Rotates log files daily
- Includes timestamps and module names
- Can be imported and used as: from src.utils.logger import logger

Provide:
- get_logger(name: str) -> logging.Logger
- Configure for development (verbose) and production (less verbose)

Create tests that verify log output"
```

**Validation**:
```bash
pytest tests/unit/test_logger.py -v
ls -la logs/
```

### Task 1.A.3: Input Validation

**Goal**: Validate all user inputs early

**Cursor Commands**:
```
1. Open: src/utils/validators.py
2. Ask Cursor:

"Create validators in src/utils/validators.py for:
- File path validation (must be valid PDF, <50MB)
- Dietary preference validation (valid enum)
- Allergen list validation
- Configuration validation

Functions:
- validate_pdf_file(file_path: str) -> Tuple[bool, str]
- validate_dietary_prefs(prefs: list) -> Tuple[bool, str]
- validate_allergen_list(allergens: list) -> Tuple[bool, str]

Each returns (is_valid: bool, error_message: str)

Create comprehensive tests with edge cases"
```

**Validation**:
```bash
pytest tests/unit/test_validators.py -v
```

---

## 📄 PHASE 1B: PDF PROCESSING

### Task 1.B.1: PDF Text Extraction

**Goal**: Extract text from native PDFs reliably

**Cursor Commands**:
```
1. Create: src/core/menu_parser.py
2. Ask Cursor:

"Create menu_parser.py class MenuParser that:

Methods:
- __init__(pdf_path: str)
- extract_text() -> str
  * Extract text from PDF using PyPDF2
  * Handle multi-page PDFs
  * Preserve section structure (detect by whitespace/formatting)
  * Return full text with page breaks marked
  
- extract_by_page() -> Dict[int, str]
  * Return dict mapping page_number -> text
  * Useful for layout analysis
  
- extract_metadata() -> Dict
  * Get PDF title, author, creation date
  * Count pages

Include:
- Error handling for corrupted PDFs
- Logging for debug info
- Type hints
- Comprehensive docstrings

Create tests in tests/unit/test_menu_parser.py with:
- Test on simple PDF
- Test on multi-page PDF
- Test on corrupted PDF (should raise appropriate error)
- Test text extraction accuracy"
```

**Validation**:
```bash
pytest tests/unit/test_menu_parser.py -v
```

### Task 1.B.2: OCR for Scanned Menus

**Goal**: Handle scanned menu images using Tesseract

**Cursor Commands**:
```
1. Create: src/processors/pdf_processor.py
2. Ask Cursor:

"Create pdf_processor.py class PDFProcessor that:

Methods:
- __init__(pdf_path: str, config: Config)
- is_scanned_menu() -> bool
  * Detect if PDF is image-based (scanned) vs text-based
  * Compare text extraction vs. expected page size
  
- convert_to_images(dpi: int = 150) -> List[PIL.Image]
  * Convert PDF pages to images using pdf2image
  * Return list of PIL Image objects
  
- ocr_image(image: PIL.Image) -> str
  * Apply Tesseract OCR to single image
  * Include image preprocessing (contrast, deskew)
  * Return extracted text
  
- process() -> str
  * Intelligently handle both native PDF and scanned
  * Fall back to OCR if text extraction yields <50 chars per page
  * Return full extracted text

Include:
- Image preprocessing (grayscale, contrast enhancement)
- Tesseract language support (start with 'eng')
- Timeout handling for slow OCR
- Caching of processed images
- Comprehensive error handling

Create tests with:
- Sample scanned menu (generate or find)
- Verify OCR accuracy
- Test performance (should be <1min for 3-page menu)"
```

**Validation**:
```bash
pytest tests/unit/test_pdf_processor.py -v
```

### Task 1.B.3: Text Normalization

**Goal**: Clean extracted text for further processing

**Cursor Commands**:
```
1. Add to: src/processors/pdf_processor.py
2. Ask Cursor:

"Add to PDFProcessor:

Methods:
- normalize_text(text: str) -> str
  * Remove extra whitespace (multiple spaces/newlines)
  * Fix encoding issues (smart quotes, etc.)
  * Normalize line breaks
  * Remove page numbers and headers/footers
  * Return clean text

- detect_sections(text: str) -> Dict[str, str]
  * Identify menu sections (Appetizers, Entrees, Sides, etc.)
  * Use heuristics: ALL CAPS, followed by items
  * Return dict mapping section_name -> section_text

Include tests for:
- Various whitespace patterns
- Special characters
- Section detection accuracy"
```

---

## 🍽️ PHASE 1C: DISH EXTRACTION & PARSING

### Task 1.C.1: Dish Identification

**Goal**: Extract individual menu items from text

**Cursor Commands**:
```
1. Create: src/processors/dish_extractor.py
2. Ask Cursor:

"Create DishExtractor class that:

Classes/Types:
- MenuItem(name: str, description: str, price: Optional[str], section: str)

Methods:
- __init__(menu_text: str, sections: Dict[str, str])
- extract_dishes() -> List[MenuItem]
  * Parse text to find individual dishes
  * Common patterns:
    - Name | Description (dotted line) | $Price
    - Name ... Description ... $XX.XX
    - Name\\nDescription\\n$Price
  * Handle edge cases (missing prices, long descriptions)
  
- extract_from_section(section_text: str, section_name: str) -> List[MenuItem]
  * Parse single section
  * Use regex or heuristics
  
- normalize_dish_name(name: str) -> str
  * Capitalize properly
  * Remove special characters
  * Remove asterisks/symbols that indicate notes

Create MenuItem dataclass with fields:
- name: str (dish name)
- description: str (full description)
- price: Optional[str]
- section: str (menu section)
- ingredients_mentioned: List[str] (parsed from description)
- confidence: float (0-1, based on parsing success)

Create comprehensive tests with:
- Real menu sections
- Edge cases (long descriptions, missing prices)
- Verify ≥80% accuracy on known menus"
```

**Validation**:
```bash
pytest tests/unit/test_dish_extractor.py -v
```

### Task 1.C.2: Ingredient Parsing

**Goal**: Extract ingredients mentioned in dish descriptions

**Cursor Commands**:
```
1. Create: src/processors/ingredient_analyzer.py
2. Ask Cursor:

"Create IngredientAnalyzer class that:

Methods:
- __init__(config: Config)
- extract_ingredients(description: str) -> List[str]
  * Parse parenthetical ingredients: \"(with garlic, tomato)\"
  * Look for 'contains:', 'made with:', 'includes:' patterns
  * Extract common allergen keywords (nuts, dairy, gluten, etc.)
  * Normalize ingredient names
  * Return deduplicated list
  
- normalize_ingredient(ingredient: str) -> str
  * Remove articles (a, an, the)
  * Standardize names (e.g., 'peanuts' and 'peanut' both -> 'peanut')
  * Fix common typos/abbreviations
  
- score_confidence(description: str) -> float
  * How confident are we about ingredients mentioned?
  * 1.0 if explicitly listed
  * 0.5 if inferred from keywords
  * 0.0 if no info available

Include unit tests with:
- Various description formats
- Edge cases
- Allergen keyword detection"
```

---

## 🔍 PHASE 1D: RECIPE RESEARCH & VALIDATION

### Task 1.D.1: Recipe Search Integration

**Goal**: Look up recipes online to find ingredients

**Cursor Commands**:
```
1. Create: src/processors/recipe_searcher.py
2. Ask Cursor:

"Create RecipeSearcher class that:

Methods:
- __init__(config: Config, cache_dir: str)
- search_recipe(dish_name: str, cuisine: Optional[str] = None) -> Dict
  * Query Spoonacular API (primary)
  * Return:
    {
      'name': str,
      'cuisine': str,
      'ingredients': List[str],
      'source': str,
      'source_url': str,
      'confidence': float,
      'search_date': datetime
    }
  * Implement retry logic (up to 3 attempts)
  * Use caching to avoid repeated API calls
  
- extract_ingredients_from_recipe(recipe: Dict) -> List[str]
  * Parse ingredient list from API response
  * Normalize names
  
- search_with_fallback(dish_name: str, cuisine: str) -> Dict
  * Try Spoonacular first
  * Fall back to web scraping (BeautifulSoup) if API fails
  * Implement timeout (10 seconds per request)

Include:
- API rate limiting (log warnings if approaching limit)
- Error handling (API down, network errors)
- Caching with expiration (30 days)
- Logging of search attempts

Create tests with:
- Mock API responses
- Test cache functionality
- Test fallback mechanisms"
```

**Important**: Obtain Spoonacular API key first:
```
1. Go to https://spoonacular.com/food-api
2. Sign up for free account
3. Get API key
4. Add to .env: SPOONACULAR_API_KEY=your_key_here
```

### Task 1.D.2: Confidence Scoring

**Goal**: Rate how confident we are about ingredient data

**Cursor Commands**:
```
1. Create: src/core/confidence_engine.py
2. Ask Cursor:

"Create ConfidenceEngine class that:

Methods:
- score_ingredient_match(mentioned: str, found: str) -> float
  * String similarity (Levenshtein distance or fuzzy matching)
  * Return 0-1 confidence
  
- score_recipe_result(recipe: Dict, dish_name: str) -> float
  * How well does recipe match dish?
  * Factors:
    - Name similarity
    - Cuisine match
    - Recipe source quality
  * Return 0-1 confidence
  
- aggregate_confidence(confidences: List[float]) -> float
  * Average confidence with 90% threshold
  * Flag results with <0.9 confidence
  
- validate_against_threshold(confidence: float, threshold: float = 0.9) -> bool
  * Return True if confidence >= threshold

Include fuzzy matching for similar ingredient names"
```

---

## 🚨 PHASE 1E: ALLERGEN DETECTION & CLASSIFICATION

### Task 1.E.1: Allergen Database

**Goal**: Define all allergens and dietary rules

**Cursor Commands**:
```
1. Edit: config/savvi_config.yaml
2. Review the existing YAML structure
3. Ask Cursor:

"Review savvi_config.yaml and create accompanying
config/allergen_rules.json with comprehensive allergen definitions.

For each allergen include:
- Aliases (peanut, peanuts, groundnut, etc.)
- Common sources/foods
- Severity level (critical, moderate, mild)
- Cross-contamination notes
- Prevalence in cuisines

Structure:
{
  'peanuts': {
    'aliases': ['peanut', 'groundnut', ...],
    'severity': 'critical',
    'sources': ['nuts', 'Asian dishes', ...],
    'cross_contamination': True,
    'cuisines': ['Thai', 'Indian', ...]
  },
  ...
}

Include all major allergens:
- Critical: peanuts, tree nuts, shellfish, fish, sesame, milk, eggs, wheat, soy
- Moderate: gluten, processed in shared facilities
- Mild: high sodium, spicy"
```

### Task 1.E.2: Allergen Detection

**Goal**: Identify allergens in dish descriptions and recipes

**Cursor Commands**:
```
1. Create: src/core/allergen_database.py
2. Ask Cursor:

"Create AllergenDatabase class that:

Methods:
- __init__(config_path: str = 'config/allergen_rules.json')
  * Load allergen rules from JSON
  * Build lookup indices for fast matching
  
- find_allergens(ingredients: List[str]) -> List[Dict]
  * Search ingredients for known allergens
  * Return list of: {name, severity, aliases_matched}
  * Use fuzzy matching for similar names
  * Return empty list if no allergens found
  
- get_allergen_aliases(allergen: str) -> List[str]
  * Return all known names for allergen
  
- get_severity(allergen: str) -> str
  * Return: 'critical', 'moderate', or 'mild'

Include:
- Case-insensitive matching
- Whitespace handling
- Fast lookup (use sets for performance)
- Comprehensive docstrings

Create tests with:
- Known allergen patterns
- Edge cases (misspellings, plurals)
- Performance test (100+ ingredients)"
```

### Task 1.E.3: Dietary Mapping Engine

**Goal**: Map dishes to user dietary preferences

**Cursor Commands**:
```
1. Create: src/core/dietary_mapper.py
2. Ask Cursor:

"Create DietaryMapper class that:

Types:
- DietaryProfile(vegan: bool, vegetarian: bool, gluten_free: bool, keto: bool, allergies: List[str])
- DishSafety(level: Literal['safe', 'caution', 'avoid', 'unknown'], reason: str, confidence: float)

Methods:
- __init__(allergen_db: AllergenDatabase, config: Config)
- evaluate_dish(dish: MenuItem, profile: DietaryProfile) -> DishSafety
  * Analyze dish against user preferences
  * Consider:
    - Mentioned ingredients (high confidence)
    - Found recipe ingredients (depends on confidence)
    - Known preparation methods
    - Cross-contamination risks
  * Return DishSafety with:
    - level: 'safe' | 'caution' | 'avoid' | 'unknown'
    - reason: explanation
    - confidence: 0-1
  
- color_code(safety: DishSafety) -> str
  * Map to color: 🟢 safe, 🟡 caution, 🔴 avoid, ⚠️ unknown
  
- summarize_profile(dishes: List[MenuItem], profile: DietaryProfile) -> Dict
  * Return summary: {safe_count, caution_count, avoid_count, unknown_count}

Classification Logic:
- SAFE (🟢): No allergens/excluded ingredients + confidence >0.9
- CAUTION (🟡): Can be modified OR low confidence OR trace allergens
- AVOID (🔴): Contains allergen at critical/high severity OR explicitly excluded
- UNKNOWN (⚠️): Missing ingredient data, needs staff clarification

Create tests with:
- Various dietary profiles
- Edge cases (mixed allergens, partial info)
- Verify classification accuracy"
```

---

## 📑 PHASE 1F: PDF MARKING & OUTPUT

### Task 1.F.1: PDF Annotation Engine

**Goal**: Generate marked-up PDFs with safety classifications

**Cursor Commands**:
```
1. Create: src/processors/marking_engine.py
2. Ask Cursor:

"Create MarkingEngine class that:

Methods:
- __init__(config: Config)
- mark_pdf(pdf_path: str, marked_dishes: Dict[str, DishSafety], output_path: str)
  * Read original PDF
  * For each page, add annotations:
    - Color overlays (green/yellow/red/gray)
    - Safety labels
    - Confidence badges
    - Notes field
  * Preserve original menu layout
  * Save to output_path
  
- add_summary_page(doc, summary: Dict, profile: DietaryProfile)
  * Create new first page with:
    - Summary statistics (% safe, caution, avoid, unknown)
    - Legend/key
    - User profile used
    - Generation date
    - Instructions for using the marked menu
  
- add_ask_server_section(doc, unknowns: List[MenuItem])
  * Create section at end for items needing clarification
  * Include space for staff notes
  * List all 'unknown' dishes
  
- add_editable_fields(doc)
  * Add form fields for user to write notes
  * Attach notes to specific dishes

Output PDF should include:
- Color-coded overlays (don't obscure original menu)
- Legend on summary page
- Editable text fields
- Metadata (date, user profile, confidence scores)

Create tests with:
- Sample PDF input
- Verify output is readable
- Check file size (shouldn't bloat too much)"
```

**Note**: You may need to use ReportLab or PyPDF2's capabilities. If marking existing PDFs is complex, alternative: Generate new marked PDF from scratch.

### Task 1.F.2: Output Formatting

**Goal**: Generate professional, user-friendly output

**Cursor Commands**:
```
1. Add to: src/processors/marking_engine.py
2. Ask Cursor:

"Add methods to MarkingEngine for formatting:

Methods:
- generate_summary_report(dishes: List[MenuItem], 
                         safeties: Dict[str, DishSafety],
                         profile: DietaryProfile) -> str
  * Return formatted text report
  * Include:
    - Profile summary
    - Statistics
    - List of safe/caution/avoid/unknown dishes
    - Recommendations
  
- format_dish_note(dish: MenuItem, safety: DishSafety) -> str
  * Return formatted text for single dish
  * Example: '🔴 AVOID - Contains peanuts (95% confidence)'
  
- export_json_summary(dishes, safeties, profile) -> str
  * Export findings as JSON for programmatic use
  * Useful for Phase 2 API

Include styling/formatting for:
- Console output (colored text)
- PDF output (overlays)
- JSON output (structured)"
```

---

## 💾 PHASE 1G: CLI INTERFACE & MAIN ENTRY POINT

### Task 1.G.1: Command-Line Interface

**Goal**: Create user-friendly CLI for the tool

**Cursor Commands**:
```
1. Edit: src/main.py
2. Ask Cursor:

"Create main.py as CLI entry point using Click library:

Usage should be:
  python src/main.py --menu ~/menu.pdf --vegan --gluten-free --output ~/marked_menu.pdf

Arguments:
- menu (required): Path to restaurant menu PDF
- output (optional): Output file path (default: ./output/marked_[menu_name].pdf)

Options:
- --vegan: Flag as vegan
- --vegetarian: Flag as vegetarian
- --gluten-free: Flag as gluten-free
- --keto: Flag as keto
- --allergies: Comma-separated list (nuts, shellfish, etc.)
- --confidence-threshold: Override 90% default
- --verbose: Enable debug logging
- --no-recipe-search: Skip online recipe lookup (use only menu description)

Include:
- Input validation
- Progress bar/logging
- Error messages
- Help text

Example execution:
  python src/main.py --menu ~/restaurant_menu.pdf --vegan --gluten-free
  # Outputs: ./output/marked_restaurant_menu.pdf
  # With colored console output showing results

Create main() function that:
1. Validates inputs
2. Loads config
3. Initializes components
4. Processes PDF
5. Outputs marked file
6. Prints summary"
```

### Task 1.G.2: Error Handling & User Feedback

**Goal**: Graceful error handling with helpful messages

**Cursor Commands**:
```
1. Update: src/main.py
2. Ask Cursor:

"Add comprehensive error handling to main.py:

Handle errors gracefully:
- Invalid PDF file -> 'Cannot read PDF: [reason]. Check file format.'
- API failures -> 'Recipe lookup failed. Using menu description only.'
- OCR failures -> 'OCR failed on page X. Using text extraction instead.'
- Missing config -> 'Configuration file missing. Using defaults.'

For each error:
- Log with context
- Suggest remediation
- Allow continuation if possible
- Exit cleanly if not

Add progress indicators:
- Loading PDF... ✓
- Extracting dishes... ✓ (Found 45 items)
- Researching recipes... ✓ (75% complete)
- Analyzing allergens... ✓
- Generating output... ✓
- Done! Output: ./output/marked_menu.pdf"
```

---

## 🧪 PHASE 1H: TESTING SUITE

### Task 1.H.1: Unit Tests

**Goal**: Comprehensive unit tests for all modules

**Cursor Commands**:
```
1. Create: tests/conftest.py (pytest configuration)
2. Ask Cursor:

"Create tests/conftest.py with pytest fixtures:

Fixtures:
- sample_menu_pdf: Path to test menu PDF
- sample_config: Config object
- allergen_db: Loaded AllergenDatabase
- sample_dishes: List of MenuItem objects
- dietary_profile: DietaryProfile (vegan + gluten-free)
- recipe_data: Sample recipe API response

Include helpers:
- assert_dish_safety(dish, profile, expected_level)
- compare_confidences(actual, expected, tolerance)

Then create individual test files:
- tests/unit/test_config.py
- tests/unit/test_menu_parser.py
- tests/unit/test_pdf_processor.py
- tests/unit/test_dish_extractor.py
- tests/unit/test_recipe_searcher.py
- tests/unit/test_allergen_database.py
- tests/unit/test_dietary_mapper.py
- tests/unit/test_marking_engine.py

Each test file should have:
- Setup/teardown
- Happy path tests
- Error case tests
- Edge case tests
- Assertions for outputs

Target coverage: >80%"
```

**Run tests**:
```bash
pytest tests/unit/ -v --cov=src
```

### Task 1.H.2: Integration Tests

**Goal**: Test end-to-end workflow

**Cursor Commands**:
```
1. Create: tests/integration/test_end_to_end.py
2. Ask Cursor:

"Create end-to-end integration test:

Test Case: Full Workflow
1. Load sample menu PDF
2. Extract text
3. Parse dishes
4. Search recipes (mock API to avoid rate limits)
5. Detect allergens
6. Classify dishes
7. Generate output PDF

Verify:
- Output PDF is created
- All dishes are classified
- No errors occur
- Output is readable
- Performance is acceptable (<5min for 20 pages)

Create test with:
- Real sample menu (create if needed)
- Assertions on output quality
- Performance benchmarking"
```

---

## 📚 PHASE 1I: DOCUMENTATION

### Task 1.I.1: API Documentation

**Goal**: Document all public APIs

**Cursor Commands**:
```
1. Create: docs/API.md
2. Ask Cursor:

"Create comprehensive API documentation:

Sections:
1. Module Overview
   - src.core.menu_parser
   - src.core.allergen_database
   - src.core.dietary_mapper
   - src.processors.pdf_processor
   - src.processors.recipe_searcher
   - src.processors.marking_engine
   - etc.

2. For each module:
   - Class/function signature
   - Parameters with types
   - Return values with types
   - Usage examples
   - Error cases
   - Performance notes

3. Common workflows:
   - How to process a PDF
   - How to add custom allergens
   - How to modify dietary rules
   - How to extend recipe search

4. Configuration reference
   - All config options
   - Environment variables
   - Default values

Include code examples for:
- Basic usage
- Advanced usage
- Error handling
- Extension points"
```

### Task 1.I.2: Architecture & Design

**Goal**: Document system design

**Cursor Commands**:
```
1. Create: docs/ARCHITECTURE.md
2. Ask Cursor:

"Create architecture documentation:

Sections:
1. System Overview
   - Data flow diagram (text-based)
   - Component relationships
   
2. Module Design
   - Purpose of each module
   - Interfaces/contracts
   - Dependencies
   
3. Data Models
   - MenuItem structure
   - DietaryProfile
   - DishSafety
   - Recipe data structure
   
4. Processing Pipeline
   - Step-by-step workflow
   - Error handling strategy
   - Caching strategy
   
5. Extensibility
   - How to add new allergens
   - How to add new recipe sources
   - How to add new dietary preferences
   
6. Performance Considerations
   - Bottlenecks
   - Optimization strategies
   - Caching benefits
   
7. Security Considerations
   - API key management
   - File handling safety
   - Input validation"
```

---

## ✅ VALIDATION CHECKLIST

Use this checklist to verify Phase 1 completion:

### Code Quality
- [ ] All code follows PEP 8 (use `black` formatter)
- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] No console warnings or errors
- [ ] No hardcoded values (use config)
- [ ] No secrets in code (use .env)

### Testing
- [ ] Unit test coverage >80%
- [ ] All tests passing (`pytest tests/ -v`)
- [ ] Integration tests working
- [ ] Manual testing on real menus

### Performance
- [ ] PDF extraction <1 minute for 20-page menu
- [ ] Recipe search completes within 10s per dish
- [ ] Total processing <5 minutes for 20-page menu

### Documentation
- [ ] README.md comprehensive
- [ ] API documentation complete
- [ ] Architecture documented
- [ ] Cursor guide complete (this file)

### CLI
- [ ] Help text works (`python src/main.py --help`)
- [ ] Basic usage works
- [ ] Output PDF is readable
- [ ] Error messages are helpful

### Deployment Ready
- [ ] .env.template filled out
- [ ] requirements.txt complete
- [ ] Setup script works
- [ ] All dependencies install cleanly
- [ ] No broken imports

---

## 🔗 PHASE 1 → PHASE 2 TRANSITION

**When to move to Phase 2**:
- ✅ All Phase 1 tasks complete
- ✅ CLI tool working reliably
- ✅ Tested on 5+ real restaurant menus
- ✅ Users can generate marked PDFs

**Phase 2 Preview** (Web Platform):
- User authentication
- Web UI for PDF upload
- Database for user profiles
- REST API
- Automatic personalization

---

## 🎯 KEY CURSOR PROMPTS

Keep these ready for quick asks:

### Generate Test Data
```
"Create a sample restaurant menu PDF with:
- 3 sections (Appetizers, Entrees, Sides)
- 15 total dishes
- Mixed allergens (nuts, gluten, dairy, shellfish)
- Realistic prices and descriptions"
```

### Code Review
```
"Review src/core/menu_parser.py for:
- Code quality and PEP 8 compliance
- Missing error handling
- Performance issues
- Suggestions for improvement"
```

### Bug Investigation
```
"I'm getting [error message]. 
Debug this issue by:
1. Analyzing the error
2. Identifying likely causes
3. Suggesting fixes
4. Providing test cases"
```

### Performance Optimization
```
"Optimize [module_name] for performance:
1. Profile the code
2. Identify bottlenecks
3. Suggest optimizations
4. Implement improvements"
```

---

## 📞 TROUBLESHOOTING

### Common Issues & Solutions

**Issue**: Tesseract not found
```
Solution:
1. Install: choco install tesseract (Windows)
2. Add to .env: TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
3. Verify: tesseract --version
```

**Issue**: Spoonacular API rate limit exceeded
```
Solution:
1. Implement caching (already in recipe_searcher.py)
2. Reduce batch size
3. Upgrade API plan
4. Contact support for limit increase
```

**Issue**: OCR quality poor on old menus
```
Solution:
1. Preprocess images (contrast enhancement)
2. Try different DPI settings
3. Consider manual data entry for critical items
4. Flag for server clarification
```

**Issue**: PDF markup doesn't preserve layout
```
Solution:
1. Use ReportLab to generate new PDF if modifying is too complex
2. Create overlay PDF instead of modifying original
3. Consider providing multiple output formats
```

---

## 🚀 FINAL NOTES

### Success Mindset
- **Start Small**: Get basic PDF extraction working first
- **Iterate**: Add features incrementally
- **Test Early**: Write tests as you code
- **Document**: Keep docs in sync with code
- **Refactor**: Improve code quality regularly

### Development Pattern
1. **Plan**: Understand requirements
2. **Implement**: Write code with types & docstrings
3. **Test**: Write unit and integration tests
4. **Document**: Update docs
5. **Review**: Check quality
6. **Iterate**: Improve based on feedback

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/menu-parser

# Commit regularly
git add src/core/menu_parser.py
git commit -m "feat: implement menu text extraction

- Extract text from native PDFs
- Handle multi-page documents
- Preserve section structure"

# Push and create PR
git push origin feature/menu-parser
```

### Asking for Help
When asking Cursor for help, include:
1. What you're trying to achieve
2. What you've tried so far
3. What error you're getting (if any)
4. Relevant code snippets or file names
5. What success looks like

Example:
```
"I'm trying to implement recipe search, but the Spoonacular
API is returning 401 errors even though my API key looks valid.

I've:
- Verified the API key in .env
- Tested with curl directly (works)
- Checked the recipes_searcher.py code

Error in logs:
  {'error': 'Unauthorized', 'code': 401}

I need to:
1. Debug the API request being sent
2. Verify headers are correct
3. Add better error logging

Can you help me troubleshoot?"
```

---

## 📊 PROGRESS TRACKING

As you complete tasks, update this section:

```
PHASE 1A (Infrastructure): [██████░░░░] 60%
  ✓ Project scaffolding complete
  ✓ Configuration templates created
  ✓ Directory structure initialized
PHASE 1B (PDF Processing): [░░░░░░░░░░] 0%
PHASE 1C (Dish Extraction): [░░░░░░░░░░] 0%
PHASE 1D (Recipe Search):  [░░░░░░░░░░] 0%
PHASE 1E (Allergen Detect): [░░░░░░░░░░] 0%
PHASE 1F (PDF Marking):    [░░░░░░░░░░] 0%
PHASE 1G (CLI Interface):  [░░░░░░░░░░] 0%
PHASE 1H (Testing):        [░░░░░░░░░░] 0%
PHASE 1I (Documentation):  [██░░░░░░░░] 20%

Overall: [███░░░░░░░] 15%
```

---

**Last Updated**: 2025-12-03
**Recent Progress**: Scaffold script executed - Project structure created at `C:\Users\Gordo\projects\savvi`
**Next Review**: Weekly
**Questions?** Review the relevant task section or ask Cursor for clarification!

🚀 **Let's build SAVVI!** 🚀
