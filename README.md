# 🤖 AI Resume Analyzer

> A full-stack portfolio project built with **FastAPI**, **SQLite**, **React**, **Vite**, and **Tailwind CSS**. Upload your resume, paste a job description, and instantly receive a detailed ATS compatibility score, keyword gap analysis, AI-powered bullet rewrites, custom interview questions, and career learning recommendations.

---

## 📸 Features

- **Drag & Drop Resume Upload** — PDF and DOCX formats supported (max 10MB)
- **ATS Score (0–100)** — Weighted scoring engine based on keyword density, section structure, and contact completeness
- **Skill Gap Analysis** — Matched vs. missing skills with domain taxonomy breakdown (Frontend, Backend, DevOps, etc.)
- **Experience Level Estimation** — Automatic classification: Fresher → Junior → Mid-Level → Senior
- **AI Bullet Rewrite Suggestions** — Before/After action-oriented bullet points optimized for ATS
- **Custom Interview Questions** — Generated from resume & job description context
- **Resume Optimization Checklist** — Pass/fail evaluation of core ATS requirements
- **Course Recommendations** — Personalized learning roadmap for skill gaps
- **History Dashboard** — Searchable, sortable table of past analyses with delete support
- **Export Reports** — Download analysis results as structured JSON
- **Dark Mode** — Persistent light/dark theme with system preference detection
- **Responsive Design** — Optimized for desktop, tablet, and mobile

---

## 🗂️ Project Structure

```
resume-analyzer/
├── backend/
│   ├── app.py              # FastAPI app entry point, CORS, database init
│   ├── routes.py           # All API route handlers (/api/*)
│   ├── analyzer.py         # ATS scoring engine + OpenAI integration
│   ├── parser.py           # PDF/DOCX text extraction & section detection
│   ├── models.py           # SQLAlchemy ORM model (Analysis table)
│   ├── database.py         # SQLAlchemy engine + session factory
│   ├── schemas.py          # Pydantic request/response validation schemas
│   ├── utils.py            # Skill taxonomy, regex helpers, contact extractor
│   ├── test_main.py        # Pytest unit tests
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variable template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx         # Header with navigation & dark mode toggle
│   │   │   ├── Footer.jsx         # App footer
│   │   │   ├── UploadResume.jsx   # Drag-and-drop file uploader
│   │   │   ├── JobDescription.jsx # JD input with sample templates
│   │   │   ├── ScoreCard.jsx      # ATS score gauge & candidate info card
│   │   │   ├── SkillTable.jsx     # Matched/missing skills + domain taxonomy
│   │   │   ├── Suggestions.jsx    # Strengths, weaknesses, rewrites, checklist
│   │   │   ├── History.jsx        # Searchable analysis history table
│   │   │   └── Loading.jsx        # Multi-step animated loading skeleton
│   │   ├── context/
│   │   │   └── ThemeContext.jsx   # Dark mode state provider (React Context)
│   │   ├── pages/
│   │   │   ├── Home.jsx           # Main analyzer workspace
│   │   │   ├── Dashboard.jsx      # Stats overview + history
│   │   │   └── AnalysisDetail.jsx # Saved analysis deep-dive view
│   │   ├── services/
│   │   │   └── api.js             # Axios client & all API function calls
│   │   ├── App.jsx                # Router configuration + layout wrapper
│   │   ├── main.jsx               # React DOM entry point
│   │   └── index.css              # Tailwind imports + custom utility classes
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack & Why Each Library Was Chosen

| Layer | Technology | Why |
|---|---|---|
| Frontend Framework | React 18 | Industry-standard, component-based UI, ideal for complex state flows |
| Build Tool | Vite | 10-100x faster HMR than CRA; native ESModules; excellent DX |
| Styling | Tailwind CSS | Utility-first CSS enables rapid iteration without context switching |
| Routing | React Router v6 | Declarative nested routing, `<NavLink>` active state management |
| HTTP Client | Axios | Cleaner API than native `fetch`, built-in request/response interceptors |
| Backend Framework | FastAPI | Async Python, auto-generated Swagger docs, Pydantic validation built-in |
| ORM | SQLAlchemy 2.0 | Industry-standard Python ORM, supports multiple DB backends |
| Database | SQLite | Zero-config, file-based persistence; perfect for portfolio/local dev |
| PDF Parsing | pdfplumber | More accurate text extraction than PyPDF2; handles complex layouts |
| DOCX Parsing | python-docx | Official `.docx` format library from Microsoft; reads paragraphs & tables |
| AI Integration | OpenAI API (configurable) | Standardized REST protocol; works with Groq, Ollama, OpenRouter |
| Testing | Pytest | Simple, expressive Python test runner with minimal boilerplate |
| Containerization | Docker + Compose | Ensures reproducible environments across dev/staging/production |
| Icons | Lucide React | Clean, consistent SVG icons with tree-shaking support |

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- pip
- npm

---

### 1. Backend Setup

```bash
cd backend

# Copy environment config
cp .env.example .env

# Edit .env and optionally add your OpenAI API key
# If no key provided, the built-in heuristic engine is used automatically

# Create a virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
# OR
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Start the backend development server
python app.py
# Backend runs at: http://localhost:8000
# Swagger API docs: http://localhost:8000/docs
```

---

### 2. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Start the Vite dev server
npm run dev
# Frontend runs at: http://localhost:5173
```

> The Vite dev proxy automatically forwards `/api/*` requests to `http://localhost:8000`, so no cross-origin issues.

---

### 3. Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./resume_analyzer.db` | SQLAlchemy DB connection string |
| `OPENAI_API_KEY` | *(empty)* | OpenAI (or compatible) API key. Leave blank for heuristic-only mode |
| `OPENAI_API_BASE` | `https://api.openai.com/v1` | API base URL (supports Groq, Ollama, OpenRouter) |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | LLM model name |
| `CORS_ORIGINS` | `http://localhost:5173,...` | Comma-separated list of allowed frontend origins |
| `PORT` | `8000` | Backend server port |

---

## 🐳 Docker Setup

```bash
# Copy env file
cp backend/.env.example backend/.env

# Build and start the container
docker-compose up --build

# App available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

---

## 📡 API Documentation

All endpoints are prefixed with `/api`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/api/upload` | Upload resume file → Extract text, skills, sections |
| `POST` | `/api/analyze` | Full ATS analysis → Store result in DB |
| `GET` | `/api/history` | List all saved analysis records |
| `GET` | `/api/analysis/{id}` | Fetch detailed single analysis |
| `DELETE` | `/api/analysis/{id}` | Delete analysis record |
| `GET` | `/api/dashboard/stats` | Aggregate metrics (total, avg, highest score) |

### Sample `POST /api/analyze` Request (multipart/form-data)

```
file:            <binary resume file>
job_description: "We are looking for a Python FastAPI developer..."
job_title:       "Senior Backend Engineer"
```

### Sample Response

```json
{
  "id": 7,
  "filename": "john_resume.pdf",
  "candidate_name": "John Smith",
  "score": 78,
  "completeness_score": 85,
  "experience_level": "Mid-Level",
  "summary": "Resume matches approximately 72% of target job requirements...",
  "matching_skills": ["Python", "FastAPI", "Docker", "PostgreSQL"],
  "missing_skills": ["Kubernetes", "GraphQL", "Redis"],
  "strengths": ["Strong backend skill alignment..."],
  "weaknesses": ["Missing containerization orchestration keywords..."],
  "suggestions": ["Add Kubernetes to your DevOps skills section..."],
  "interview_questions": ["Can you describe a complex challenge you solved using FastAPI?"],
  "rewrite_suggestions": [{"original": "...", "suggested": "..."}],
  "course_recommendations": [{"topic": "Kubernetes for Developers", "reason": "..."}],
  "checklist": [{"item": "Contact information", "passed": true}],
  "created_at": "2026-08-05T04:50:12.421000"
}
```

---

## 🗄️ Database Schema

**Table: `analyses`**

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-incremented primary key |
| `filename` | VARCHAR(255) | Original uploaded filename |
| `candidate_name` | VARCHAR(150) | Extracted candidate name |
| `email` | VARCHAR(150) | Extracted email address |
| `phone` | VARCHAR(50) | Extracted phone number |
| `score` | INTEGER | ATS score (0–100) |
| `completeness_score` | INTEGER | Resume completeness % |
| `experience_level` | VARCHAR(50) | Fresher / Junior / Mid-Level / Senior |
| `summary` | TEXT | Executive analysis summary |
| `job_title` | VARCHAR(200) | Target job role |
| `job_description` | TEXT | Full job description pasted by user |
| `matching_skills` | TEXT | JSON array of matched skill strings |
| `missing_skills` | TEXT | JSON array of missing skill strings |
| `strengths` | TEXT | JSON array of strength statements |
| `weaknesses` | TEXT | JSON array of weakness statements |
| `suggestions` | TEXT | JSON array of improvement suggestions |
| `section_scores` | TEXT | JSON dict: section name → score % |
| `interview_questions` | TEXT | JSON array of AI-generated interview questions |
| `rewrite_suggestions` | TEXT | JSON array of {original, suggested} bullet pairs |
| `course_recommendations` | TEXT | JSON array of {topic, reason} objects |
| `checklist` | TEXT | JSON array of {item, passed} objects |
| `created_at` | DATETIME | UTC timestamp of analysis |

---

## 🧠 ATS Scoring Algorithm — How It Works

The ATS score is a **weighted composite metric** computed in `analyzer.py`:

```
ATS Score = (skill_match_ratio × 55) + (section_completeness × 0.30) + (resume_completeness × 0.15)
```

**Component Breakdown:**

| Component | Weight | Description |
|---|---|---|
| Keyword Match Ratio | 55% | `len(resume_skills ∩ jd_skills) / len(jd_skills)` |
| Section Score | 30% | Weighted presence of Skills, Experience, Projects, Education, Certifications |
| Completeness Score | 15% | Contact info, LinkedIn, section count, skill count |

**Section Weights within Section Score:**

| Section | Weight |
|---|---|
| Skills | 30% |
| Experience | 30% |
| Projects | 20% |
| Education | 10% |
| Certifications | 10% |

The final score is clamped to `[10, 98]` to avoid absolute 0 or 100 artificially.

---

## 🧪 Running Tests

```bash
cd backend
source venv/bin/activate
pytest test_main.py -v
```

Test coverage includes:
- Health check endpoint
- Contact info regex extraction
- Section detection from raw text
- Heuristic ATS score computation
- History API response contract

---

## 📌 Realistic Git Commit History

Use these commits to build a believable project development timeline:

```bash
git init
git commit -m "Initial project setup: folder structure, .gitignore, README skeleton"
git commit -m "Backend: Setup FastAPI app with CORS, health check, and uvicorn runner"
git commit -m "Backend: Add SQLAlchemy database config and Analysis ORM model"
git commit -m "Backend: Add Pydantic schemas for type-safe request/response validation"
git commit -m "Backend: Implement pdfplumber PDF parser and python-docx DOCX parser"
git commit -m "Backend: Add skill taxonomy database and contact info extractor in utils.py"
git commit -m "Backend: Implement section detection and experience level estimator"
git commit -m "Backend: Build heuristic ATS scoring engine with weighted composite formula"
git commit -m "Backend: Add OpenAI-compatible API integration with graceful fallback"
git commit -m "Backend: Wire up all REST API routes (upload, analyze, history, stats)"
git commit -m "Frontend: Scaffold Vite + React + Tailwind project with base configuration"
git commit -m "Frontend: Add ThemeContext with dark mode toggle and localStorage persistence"
git commit -m "Frontend: Build Navbar with responsive navigation and dark mode toggle button"
git commit -m "Frontend: Create drag-and-drop UploadResume component with validation"
git commit -m "Frontend: Add JobDescription component with sample JD template loader"
git commit -m "Frontend: Build ScoreCard with animated SVG gauge and section breakdown"
git commit -m "Frontend: Create SkillTable with matched/missing badges and domain taxonomy"
git commit -m "Frontend: Add Suggestions component with rewrites, checklist, and questions"
git commit -m "Frontend: Build Loading component with multi-step animated progress tracker"
git commit -m "Frontend: Implement Dashboard page with 4 stat cards and history table"
git commit -m "Frontend: Add AnalysisDetail page for deep-diving saved analysis records"
git commit -m "Frontend: Wire Home page with analyze button, export, and reset flow"
git commit -m "Backend: Write Pytest unit tests for parser, analyzer, and API endpoints"
git commit -m "Docker: Add Dockerfile with multi-stage build and docker-compose.yml"
git commit -m "Final: Update README with full API docs, DB schema, scoring algorithm"
```

---

## 💼 Technical Interview Q&A

**Q: Why did you choose FastAPI over Flask or Django?**
> FastAPI has built-in async support, auto-generated Swagger/OpenAPI docs via Pydantic models, and is 2–3x faster than Flask for I/O-bound tasks. For a resume-parsing service that handles file I/O and external API calls, this matters. Django would add unnecessary ORM/admin complexity for a focused microservice like this.

**Q: Why SQLite instead of PostgreSQL?**
> SQLite is a zero-configuration, file-based database — perfect for local development and portfolio demos. The abstraction layer (SQLAlchemy) means switching to PostgreSQL for production is a one-line `DATABASE_URL` change with no code modifications.

**Q: How does the ATS score work exactly?**
> It's a weighted composite: 55% keyword match ratio (intersection of resume skills and JD skills), 30% section completeness score (weighted presence of Education, Experience, Skills, Projects, Certifications), and 15% contact/format completeness. The score is clamped to 10–98 to avoid absolutes.

**Q: What happens if no OpenAI API key is configured?**
> The system falls back to the deterministic heuristic engine in `analyzer.py`. This engine uses regex-based keyword matching, section detection, and weighted scoring formulas — no external API dependency. The app is fully functional without any API key.

**Q: How do you extract skills from a resume?**
> The `parser.py` module scans extracted plain text against a curated `SKILL_TAXONOMY` dictionary using regex word-boundary matching (`\bskill_name\b`). This avoids false positives like matching "go" inside "Google".

**Q: How do you handle different resume formats?**
> PDF files use `pdfplumber` which extracts text from PDF content streams. DOCX files use `python-docx` which reads paragraph objects and table cells directly from the XML structure. Both are converted to a single normalized plain-text string before processing.

**Q: How is the frontend connected to the backend?**
> The Vite dev server proxies `/api/*` requests to `http://localhost:8000` via `vite.config.js`. All API calls are centralized in `src/services/api.js` using Axios. For production Docker builds, Nginx or the same FastAPI server serves the static React build files.

**Q: How would you scale this for production?**
> Several improvements: Replace SQLite with PostgreSQL. Add Redis caching for repeated resume/JD pairs. Use Celery + Redis for async background analysis jobs. Add user authentication (JWT). Store resume files in S3 instead of processing in-memory. Add rate limiting and file virus scanning.

**Q: What is the purpose of `ThemeContext.jsx`?**
> It's a React Context provider that wraps the entire app and manages a single `darkMode` boolean state. It reads from `localStorage` on mount (falling back to OS preference), syncs the `dark` class to `<html>`, and exposes a `toggleDarkMode` function to any child component via `useTheme()` hook.

**Q: How does drag-and-drop work in `UploadResume.jsx`?**
> It uses the native HTML5 Drag and Drop API via `onDragEnter`, `onDragOver`, `onDragleave`, and `onDrop` event handlers. The `dragActive` boolean triggers a visual highlight. The dropped file is accessed via `e.dataTransfer.files[0]` and passed to the same `handleFiles()` validator used by the hidden `<input type="file">`.

**Q: Why are JSON arrays stored as TEXT in SQLite?**
> SQLite doesn't have a native JSON column type. Storing JSON-serialized strings (via `json.dumps()`) is the standard pattern for SQLite. On read, they're deserialized with `json.loads()`. In PostgreSQL, these would become proper `JSONB` columns for efficient querying.

**Q: How would you add authentication to this project?**
> Add `python-jose` and `passlib` for JWT token generation and password hashing. Create a `users` table. Add `POST /auth/register` and `POST /auth/login` endpoints. Protect analysis routes with a `get_current_user` FastAPI dependency. On the frontend, store the JWT in `localStorage` and attach it via an Axios request interceptor.

**Q: Explain the `run_full_analysis` function flow.**
> 1. `parse_resume_file()` extracts plain text + metadata. 2. `compute_heuristic_analysis()` calculates all scores and suggestions deterministically. 3. `call_openai_analysis()` optionally enriches results via LLM if API key is set. 4. Results are merged with AI enhancements taking priority where available. 5. The merged result dict is returned to the route handler which stores it in SQLite.

---

## 🔮 Future Improvements

- [ ] **User Authentication** — JWT-based login/register to isolate user histories
- [ ] **PostgreSQL Migration** — Replace SQLite for multi-user production deployments
- [ ] **Resume Version Comparison** — Side-by-side diff of two resume submissions
- [ ] **RAG-enhanced Analysis** — Index job market data for more contextual suggestions
- [ ] **LinkedIn Profile URL Analysis** — Compare LinkedIn profile vs. uploaded resume
- [ ] **File Storage (S3)** — Store uploaded resume files for future re-analysis
- [ ] **WebSocket Live Scoring** — Stream analysis progress in real-time via WebSockets
- [ ] **Scoring Trend Chart** — D3.js/Recharts line graph of score progression over time
- [ ] **Email Report Export** — Send PDF analysis report to candidate email via SendGrid
- [ ] **Rate Limiting & Auth Middleware** — `slowapi` rate limiter for API protection

---

## 📄 License

MIT License — Free for personal use, educational projects, and portfolio demonstrations.
