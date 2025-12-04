# SAVVI Project - TODO Tracking

## Project Status: MVP Development 🚀

Last Updated: 2025-12-03
Current Phase: Phase 1 - Core MVP Development
Current Focus: Phase 1B - PDF Processing (30% complete)

### 🎯 IMMEDIATE NEXT STEPS
1. ✅ **Task 1.B.1**: PDF Text Extraction (`src/core/menu_parser.py`) - **COMPLETED**
2. 🔄 **Task 1.B.2**: OCR for Scanned Menus (`src/processors/pdf_processor.py`) - **IN PROGRESS**
3. **Task 1.B.3**: Text Normalization - **NEXT**

**See `cursor.md` for detailed Cursor IDE prompts for each task.**

---

## PHASE 1: MVP - Menu Parsing & Dietary Marking

**Current Focus**: Phase 1B - PDF Processing (30% complete)
**Next Task**: Task 1.B.2 - OCR for Scanned Menus (in progress)

### ✅ COMPLETED
- [x] Project scaffolding structure
- [x] Configuration templates
- [x] Documentation framework
- [x] Cursor AI guidance document
- [x] Scaffold script executed - Project structure created at `C:\Users\Gordo\projects\savvi`
- [x] Requirements.txt updated with all dependencies (20 packages)
- [x] Scaffold scripts updated for future use
- [x] **Task 1.A.1**: Configuration Management (`src/utils/config.py`) - COMPLETED ✅ (2025-12-03 14:30:00)
  - Pydantic-based configuration system
  - Environment variable and YAML loading
  - Comprehensive validation and accessor methods
  - 329 lines of production-ready code
- [x] **Task 1.A.2**: Logging Setup (`src/utils/logger.py`) - COMPLETED ✅ (2025-12-03 15:15:00)
  - Structured logging with console and file output
  - Daily log rotation (10MB per file, 5 backups)
  - Configurable log levels for development and production
  - Comprehensive unit tests created
  - 166 lines of production-ready code
- [x] **Task 1.A.3**: Input Validation (`src/utils/validators.py`) - COMPLETED ✅ (2025-12-03 16:00:00)
  - PDF file validation (existence, format, size limits)
  - Dietary preference validation against config
  - Allergen list validation against config
  - File path and confidence threshold validation
  - Comprehensive unit tests (43 tests, all passing)
  - 300+ lines of production-ready code

### 🎯 NEXT UP (Phase 1B - PDF Processing)
- [x] **Task 1.B.1**: PDF Text Extraction (`src/core/menu_parser.py`) - **COMPLETED** ✅ (2025-12-03 17:30:00)
  - ✅ Extract text from native PDFs using PyPDF2
  - ✅ Handle multi-page PDFs with page break markers
  - ✅ Extract metadata and text by page
  - ✅ Detect text-based vs image-based PDFs
  - ✅ 15 unit tests, all passing
  - **Priority**: CRITICAL | **Effort**: 8h | **Status**: ✅ Done

- [ ] **Task 1.B.2**: OCR for Scanned Menus (`src/processors/pdf_processor.py`) - **IN PROGRESS** (Started: 2025-12-03 18:00:00)
  - ✅ PDFProcessor class created
  - ✅ is_scanned_menu() detection
  - ✅ convert_to_images() using pdf2image
  - ✅ ocr_image() with Tesseract and preprocessing
  - ✅ process() method for intelligent handling
  - [ ] Unit tests pending
  - **Priority**: HIGH | **Effort**: 6h | **Status**: 80% complete

### 📋 PHASE 1 DETAILED TASKS

#### 1.1 PDF Processing Pipeline
- [x] **menu_parser.py**: PDF text extraction - **COMPLETED**
  - [x] Handle native PDF text
  - [x] Extract text by page
  - [x] Extract metadata
  - [x] Detect text-based vs scanned PDFs
  - [x] Error handling for corrupted PDFs
  - **Priority**: CRITICAL | **Effort**: 8h | **Status**: ✅ Done

- [ ] **pdf_processor.py**: Image & OCR handling - **IN PROGRESS**
  - [x] Convert PDF to images (pdf2image)
  - [x] Tesseract OCR integration
  - [x] Image preprocessing (contrast, sharpness)
  - [x] Intelligent text/OCR fallback
  - [ ] Unit tests
  - [ ] Handle low-quality scans (testing needed)
  - **Priority**: HIGH | **Effort**: 6h | **Status**: 80% complete

- [ ] **Validation & Testing**
  - [ ] Test with 5-10 real restaurant menus
  - [ ] Verify text extraction accuracy >95%
  - [ ] Handle edge cases (multi-language, complex layouts)
  - **Priority**: HIGH | **Effort**: 4h | **Owner**: TBD

#### 1.2 Dish Parsing & Normalization
- [ ] **dish_extractor.py**: Menu item identification
  - [ ] Regex patterns for common formats (Name | $Price | Description)
  - [ ] Section-aware parsing (Appetizers, Entrees, etc.)
  - [ ] Extract description text
  - [ ] Separate pricing info
  - **Priority**: HIGH | **Effort**: 6h | **Owner**: TBD

- [ ] **ingredient_parser.py**: Extract ingredients from descriptions
  - [ ] Parse parenthetical ingredients (e.g., "with (garlic, tomato)")
  - [ ] Handle abbreviated ingredients
  - [ ] Normalize ingredient names (capitalize, remove articles)
  - [ ] Cross-reference with allergen database
  - **Priority**: HIGH | **Effort**: 5h | **Owner**: TBD

- [ ] **Test Fixtures**: Create sample menus
  - [ ] Generate 3 test PDFs (simple, complex, scanned)
  - [ ] Create expected output fixtures
  - [ ] Unit tests for parsing accuracy
  - **Priority**: MEDIUM | **Effort**: 3h | **Owner**: TBD

#### 1.3 Recipe Search & Ingredient Research
- [ ] **recipe_searcher.py**: Online recipe lookup
  - [ ] Integrate Spoonacular API
  - [ ] Query by dish name + cuisine
  - [ ] Extract ingredient lists from results
  - [ ] Implement fallback to web scraping (BeautifulSoup)
  - [ ] Cache results locally (avoid API limits)
  - **Priority**: CRITICAL | **Effort**: 8h | **Owner**: TBD

- [ ] **Confidence Scoring**
  - [ ] Implement 90% confidence threshold
  - [ ] Cross-validate results from 2+ sources
  - [ ] Track recipe source & date found
  - [ ] Flag ambiguous/uncertain ingredients
  - **Priority**: HIGH | **Effort**: 5h | **Owner**: TBD

- [ ] **API Integration**
  - [ ] Obtain Spoonacular API key
  - [ ] Test rate limiting
  - [ ] Handle API failures gracefully
  - [ ] Implement retry logic
  - **Priority**: HIGH | **Effort**: 4h | **Owner**: TBD

#### 1.4 Allergen Detection & Classification
- [ ] **allergen_database.py**: Build allergen rules engine
  - [ ] Create comprehensive allergen list (critical, moderate, mild)
  - [ ] Implement dietary preference rules
  - [ ] Create JSON configuration file
  - [ ] Support custom allergen profiles
  - **Priority**: CRITICAL | **Effort**: 5h | **Owner**: TBD

- [ ] **dietary_mapper.py**: Match dishes to user preferences
  - [ ] Implement safety classification (Safe | Caution | Avoid | Unknown)
  - [ ] Color-code mapping (Green | Yellow | Red | Gray)
  - [ ] Generate confidence scores
  - [ ] Handle partial matches
  - **Priority**: CRITICAL | **Effort**: 6h | **Owner**: TBD

- [ ] **Unique Item Flagging**
  - [ ] Identify items with unknown/cutesy names
  - [ ] Create "Ask Server" section
  - [ ] Flag items with <90% confidence
  - [ ] Generate clarification prompts
  - **Priority**: HIGH | **Effort**: 4h | **Owner**: TBD

#### 1.5 PDF Marking & Output Generation
- [ ] **marking_engine.py**: PDF annotation
  - [ ] Install ReportLab library
  - [ ] Implement color-coded overlays
  - [ ] Add confidence score badges
  - [ ] Insert safety classifications
  - **Priority**: CRITICAL | **Effort**: 10h | **Owner**: TBD

- [ ] **PDF Annotation Features**
  - [ ] Add inline comments (Safe/Avoid/Caution)
  - [ ] Create special section for "Ask Server" items
  - [ ] Add editable form fields
  - [ ] Include reference metadata (search date, sources)
  - **Priority**: HIGH | **Effort**: 8h | **Owner**: TBD

- [ ] **Output Formatting**
  - [ ] Preserve original menu layout
  - [ ] Add legend/key for color codes
  - [ ] Summary page (% safe, % caution, % avoid)
  - [ ] Include dietary profile used
  - **Priority**: MEDIUM | **Effort**: 6h | **Owner**: TBD

#### 1.6 CLI Interface & Main Entry Point
- [ ] **main.py**: Command-line interface
  - [ ] Accept PDF file path argument
  - [ ] Support dietary preference flags (--vegan, --gluten-free, etc.)
  - [ ] Output to specified file
  - [ ] Show progress/logging
  - **Priority**: HIGH | **Effort**: 4h | **Owner**: TBD | **Status**: Blocked by Phase 1A

- [ ] **Configuration Management** ⬅️ MOVED TO PHASE 1A (Task 1.A.1)
  - [x] Load .env variables (part of Task 1.A.1)
  - [x] Load config/savvi_config.yaml (part of Task 1.A.1)
  - [ ] Support CLI argument overrides (will be in main.py)
  - [x] Validate configuration on startup (part of Task 1.A.1)
  - **Priority**: CRITICAL | **Effort**: 4h | **Status**: Ready to start (Phase 1A)

#### 1.7 Error Handling & Logging
- [ ] **Comprehensive Error Handling**
  - [ ] File validation (PDF format, size limits) ⬅️ Part of Task 1.A.3
  - [ ] API error handling & retries
  - [ ] Graceful degradation (use cached data if API fails)
  - [ ] User-friendly error messages
  - **Priority**: HIGH | **Effort**: 4h | **Owner**: TBD | **Status**: Partial - validation in Phase 1A

- [ ] **Logging Setup** ⬅️ MOVED TO PHASE 1A (Task 1.A.2)
  - [x] Structured logging (file + console) (Task 1.A.2)
  - [x] Debug, info, warning, error levels (Task 1.A.2)
  - [x] Rotation for log files (Task 1.A.2)
  - [ ] Request/response tracing (Phase 2+)
  - **Priority**: HIGH | **Effort**: 3h | **Status**: Ready to start (Phase 1A)

#### 1.8 Testing Suite
- [ ] **Unit Tests** (pytest)
  - [ ] Test PDF extraction (sample menus)
  - [ ] Test ingredient parsing (edge cases)
  - [ ] Test allergen detection (all preference types)
  - [ ] Test classification logic
  - [ ] Target: >80% code coverage
  - **Priority**: HIGH | **Effort**: 10h | **Owner**: TBD

- [ ] **Integration Tests**
  - [ ] End-to-end: PDF upload → marked PDF output
  - [ ] Test with real restaurant menus
  - [ ] Verify output quality
  - [ ] Performance benchmarking (<5min for 20-page menu)
  - **Priority**: HIGH | **Effort**: 8h | **Owner**: TBD

#### 1.9 Documentation
- [ ] **API Documentation** (docs/API.md)
  - [ ] Document all functions/classes
  - [ ] Include usage examples
  - [ ] Error code reference
  - **Priority**: MEDIUM | **Effort**: 4h | **Owner**: TBD

- [ ] **Architecture Guide** (docs/ARCHITECTURE.md)
  - [ ] Data flow diagrams
  - [ ] Module interactions
  - [ ] Database schema (if applicable)
  - [ ] Deployment considerations
  - **Priority**: MEDIUM | **Effort**: 5h | **Owner**: TBD

### PHASE 1 SUMMARY
- **Total Estimated Effort**: ~140 hours
- **Target Timeline**: 4-5 weeks (assuming ~30h/week)
- **Key Dependencies**: Spoonacular API account, Tesseract installation
- **Risk Areas**: OCR accuracy, API rate limits, recipe search reliability

---

## PHASE 2: User Platform & Personalization

### 📋 PHASE 2 PLANNED TASKS (Post-MVP)
- [ ] User authentication system
- [ ] User profile & dietary preference storage
- [ ] Database schema (PostgreSQL)
- [ ] FastAPI REST API endpoints
- [ ] Web frontend (React/Next.js)
- [ ] Dynamic menu generation per user
- [ ] User history & saved menus
- [ ] **Estimated Effort**: 200+ hours
- **Target Timeline**: Weeks 6-12

---

## PHASE 3: SaaS & Scaling

### 📋 PHASE 3 FUTURE TASKS
- [ ] Restaurant admin dashboard
- [ ] Restaurant profile management
- [ ] Ingredient crowdsourcing
- [ ] ML model training on user feedback
- [ ] Analytics & reporting
- [ ] Mobile app (iOS/Android)
- [ ] API commercialization
- [ ] **Estimated Effort**: 300+ hours
- **Target Timeline**: Weeks 13-26+

---

## DEPENDENCIES & SETUP

### ✅ RESOLVED
- [x] Project scaffolding
- [x] Configuration templates
- [x] Scaffold script executed successfully (2025-12-03)
- [x] Project directory structure created
- [x] Configuration files generated (.env.template, savvi_config.yaml, requirements.txt, .gitignore)

### ⏳ REQUIRED (Before development)
- [ ] Spoonacular API account (sign up at https://spoonacular.com/food-api)
- [ ] Tesseract OCR installation (Windows: choco install tesseract)
- [ ] Python 3.10+ installed
- [ ] PostgreSQL installed (Phase 2+)
- [ ] Cursor IDE with file system access

### 🔧 SETUP STEPS
```powershell
# 1. Run scaffold ✅ COMPLETED (2025-12-03)
.\savvi_scaffold.ps1
# Project created at: C:\Users\Gordo\projects\savvi

# 2. Install dependencies (NEXT STEP)
cd $env:USERPROFILE\projects\savvi
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Install Tesseract (Windows)
choco install tesseract

# 4. Create .env file
cp .env.template .env
# Edit .env with API keys and paths
```

---

## CONTRIBUTION GUIDELINES

### Definition of Done (for each task)
- [ ] Code written & reviewed
- [ ] Unit tests passing (>80% coverage for new code)
- [ ] Integration tests passing
- [ ] Documented (docstrings, comments)
- [ ] No console warnings/errors
- [ ] Performance acceptable
- [ ] Commits linked to this TODO

### Code Standards
- PEP 8 compliance (use `black` for formatting)
- Type hints on all functions
- Comprehensive docstrings
- Error handling for all edge cases
- Logging for debugging

---

## KNOWN ISSUES & RISKS

### 🔴 CRITICAL RISKS
1. **Recipe Search Accuracy**
   - Risk: Many dishes have regional variations
   - Mitigation: Use multiple sources, implement confidence scoring, flag unknowns
   - Status: Mitigated by 90% threshold

2. **OCR Quality**
   - Risk: Poor-quality scanned menus may fail
   - Mitigation: Implement image preprocessing, manual fallback
   - Status: Testing needed

3. **API Rate Limits**
   - Risk: Spoonacular rate limits may block batch processing
   - Mitigation: Implement caching, implement queuing
   - Status: Requires testing with real volume

### 🟡 MEDIUM RISKS
1. **Language Support**
   - Risk: International menus (French, Spanish, etc.)
   - Mitigation: Phase 2 enhancement, support multiple languages
   - Status: MVP English-only

2. **Allergen Data Completeness**
   - Risk: Some restaurants hide allergen info
   - Mitigation: Flag as "unknown", require staff verification
   - Status: Mitigated by special section

---

## METRICS & SUCCESS CRITERIA

### MVP Success Criteria
- ✅ Extract text from menu PDF with >95% accuracy
- ✅ Identify ≥80% of menu items
- ✅ Research recipes for ≥70% of items
- ✅ Classify dishes correctly in manual QA (≥90%)
- ✅ Generate marked PDF in <5 minutes for 20-page menu
- ✅ Handle all major dietary preferences (vegan, gluten-free, etc.)

### Phase 2 Success Criteria
- User registration & authentication working
- ≥100 users with profiles
- Personalized menus generated on-demand
- API response time <1 second
- Platform uptime >99%

### Phase 3 Success Criteria
- ≥50 restaurants using platform
- ≥10,000 users
- Revenue metrics defined
- SaaS subscription model active

---

## NOTES & DECISIONS

### Design Decisions Made
1. **MVP Scope**: CLI tool before web platform (faster to MVP)
2. **Recipe Search**: Spoonacular first, web scraping fallback (reliability)
3. **Confidence Threshold**: 90% (balances safety vs. coverage)
4. **Output Format**: PDF with editable fields (familiar to users)

### Open Questions
- [ ] Will restaurants contribute ingredient data?
- [ ] Should MVP include restaurant database?
- [ ] How to handle liability for allergen information?
- [ ] Price model for Phase 3?

---

## CONTACT & ESCALATION

**Project Lead**: TBD
**Technical Architect**: TBD
**QA Lead**: TBD

For blockers or questions, refer to the [Cursor guidance document](cursor.md) for AI-assisted problem-solving.

---

**Last Update**: 2025-12-03 | **Next Review**: Weekly

**Recent Progress**:
- ✅ Scaffold script executed successfully
- ✅ Project structure created at `C:\Users\Gordo\projects\savvi`
- ✅ All configuration files generated (.env.template, savvi_config.yaml, requirements.txt, .gitignore)
- ✅ Complete directory structure initialized (src/, tests/, data/, config/, docs/, etc.)
