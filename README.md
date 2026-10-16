# AI Resume Analyzer

I built this project to experiment with analyzing a resume against a job description. It takes a PDF or DOCX resume, extracts the text, and returns a report with a match score, skills that match, skills that may be missing, and suggestions for improving the resume.

The project currently contains the **backend API**. There isn't a frontend in this repository yet.

## What it does

- Accepts resumes in PDF and DOCX format.
- Extracts resume text and looks for common details such as contact information and resume sections.
- Compares the resume with a job description and estimates a match score.
- Shows matching skills and skills mentioned in the job description that may be missing.
- Gives suggestions for improving the resume and preparing for interviews.
- Saves analysis results in a database so previous analyses can be viewed.
- Can use an OpenAI-compatible API for additional analysis if configured. The app also has a rule-based analysis path.

The score is an estimate based on the project's current logic. It isn't an official ATS score and shouldn't be treated as a guarantee that a company will shortlist a resume.

## Built with

- Python
- FastAPI and Uvicorn
- SQLAlchemy and SQLite
- Pydantic
- `pdfplumber` for PDF files
- `python-docx` for DOCX files
- `pytest` for tests

## Project layout

```text
AIResumeAnalyzer-main/
├── backend/
│   ├── app.py
│   ├── routes.py
│   ├── analyzer.py
│   ├── parser.py
│   ├── utils.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   ├── test_main.py
│   ├── requirements.txt
│   └── .env.example
├── .gitignore
└── README.md
```

## Run it locally

You'll need Python 3.10 or newer and `pip`.

### 1. Get the code

```bash
git clone <YOUR_REPOSITORY_URL>
cd AIResumeAnalyzer-main
```

Replace `<YOUR_REPOSITORY_URL>` with your GitHub repository URL.

### 2. Create a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` in the `backend` folder.

**Windows (PowerShell)**

```powershell
Copy-Item .env.example .env
```

**macOS / Linux**

```bash
cp .env.example .env
```

Open `backend/.env` and update the values you need. The app uses SQLite by default. LLM-based analysis is optional; configure the relevant API settings if you want to use it.

Don't commit your `.env` file or share API keys publicly.

### 5. Start the server

From inside the `backend` folder, run:

```bash
python app.py
```

Then open these URLs in your browser:

- API root / health check: http://localhost:8000/
- Interactive API docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running tests

From the `backend` folder:

```bash
pytest
```

## Notes

- This repository currently provides an API, not a complete web application.
- Resume parsing and skill matching depend on the text that can be extracted and the rules implemented in the project, so results may not always be accurate.
- Avoid testing with real resumes unless you are comfortable with how the data is stored and handled. Use sample or anonymized resumes while developing.

## Possible next steps

- Build a frontend for uploading a resume and viewing the report.
- Add more tests for unusual resume layouts and parsing errors.
- Improve the skill-matching rules and make the scoring easier to explain.
- Add clearer controls for deleting saved analysis history.

## Contributing

If you want to improve the project, feel free to fork the repository and open a pull request. For larger changes, opening an issue first would help keep the work focused.
