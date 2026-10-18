# AI Resume Analyzer

An intelligent resume analysis tool that evaluates a resume against a job description to identify matching skills, potential skill gaps, and opportunities for improvement.

AI Resume Analyzer accepts resumes in PDF and DOCX formats, extracts relevant information, and generates an analysis report with an estimated match score, skill comparisons, and actionable recommendations.

The project combines rule-based analysis with optional OpenAI-compatible API integration to explore practical applications of AI in resume evaluation.

## Features

- **Resume Upload:** Supports PDF and DOCX resume files.
- **Text Extraction:** Extracts resume content for further analysis.
- **Resume Information Detection:** Identifies common details, including contact information and resume sections.
- **Job Description Matching:** Compares resume content against a provided job description.
- **Match Score:** Calculates an estimated compatibility score based on the implemented analysis logic.
- **Skills Analysis:** Identifies matching skills and potential skill gaps.
- **Improvement Suggestions:** Provides recommendations to improve resume relevance and clarity.
- **Interview Preparation:** Generates suggestions to help candidates prepare for relevant interview topics.
- **Analysis History:** Stores analysis results in a database for future reference.
- **Optional AI Integration:** Supports an OpenAI-compatible API for enhanced analysis when configured.
- **Rule-Based Fallback:** Provides a rule-based analysis path when external AI integration is not enabled.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | REST API framework |
| Uvicorn | Application server |
| SQLAlchemy | Database ORM |
| SQLite | Default database |
| Pydantic | Data validation and schemas |
| pdfplumber | PDF text extraction |
| python-docx | DOCX text extraction |
| pytest | Automated testing |

## Project Structure

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

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python 3.10 or newer
- pip
- Git

**Windows users:** A 64-bit Python installation is recommended.

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd AIResumeAnalyzer-main
```

Replace `<YOUR_REPOSITORY_URL>` with the URL of your GitHub repository.

### 2. Create a Virtual Environment

**Windows — PowerShell**

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

To verify your Python version:

```bash
python --version
```

### 3. Install Dependencies

Navigate to the backend directory:

```bash
cd backend
```

Upgrade pip and install the required packages:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from the provided example.

**Windows — PowerShell**

```powershell
Copy-Item .env.example .env
```

**macOS / Linux**

```bash
cp .env.example .env
```

Update `backend/.env` with the configuration required for your environment.

- SQLite is used by default.
- AI-powered analysis is optional.
- Configure the appropriate API endpoint, API key, and model settings if your implementation requires them.

Keep API credentials private. Never commit your `.env` file or expose API keys in source code.

### 5. Run the Application

From the `backend` directory, start the server:

```bash
python app.py
```

Once the server is running, access the following endpoints:

| URL | Description |
|---|---|
| http://localhost:8000/ | API root or health check |
| http://localhost:8000/docs | Interactive Swagger API documentation |
| http://localhost:8000/redoc | ReDoc API documentation |

The repository currently provides a backend API. A browser-based frontend is not included in this version.

## Running Tests

From the `backend` directory, execute:

```bash
pytest
```

This runs the project's automated tests.

## How It Works

The analysis process follows these general steps:

1. **Upload:** Provide a resume in PDF or DOCX format.
2. **Extract:** Parse the document and extract its text.
3. **Analyze:** Identify relevant resume details and skills.
4. **Compare:** Evaluate the extracted content against the job description.
5. **Score:** Calculate an estimated resume-to-job match score.
6. **Report:** Return matching skills, potential gaps, and improvement suggestions.
7. **Store:** Save the analysis results for future reference.

The exact analysis depends on the rules and optional AI integration implemented in the project.

## API Usage

The API can be explored using the automatically generated Swagger interface:

http://localhost:8000/docs

Use this interface to inspect the available endpoints, review their request and response schemas, and test supported API operations.

## Limitations

- The match score is an estimate generated by the project's analysis logic. It is not an official Applicant Tracking System (ATS) score.
- Resume parsing accuracy depends on document formatting, layout, and extractable text.
- Skill matching may not capture every synonym, equivalent qualification, or contextual relationship.
- Recommendations depend on the rules and AI capabilities configured in the application.
- The project does not guarantee shortlisting, interviews, or employment outcomes.

## Security and Privacy

Resumes may contain personally identifiable and sensitive information. When using this project:

- Use sample or anonymized resumes during development and testing.
- Protect stored analysis results and restrict access to the database.
- Never commit API keys, credentials, or personal resume data to version control.
- Review the data retention and deletion behavior of the application.
- If an external AI provider is configured, review its privacy policy and data-handling terms before sending resume content or job descriptions.

## Future Improvements

Potential enhancements include:

- Building a responsive web frontend for resume uploads and analysis reports.
- Improving skill extraction and semantic job matching.
- Making match-score calculations more transparent and explainable.
- Expanding test coverage for malformed files and unusual resume layouts.
- Adding user authentication and access controls.
- Providing controls to view and delete analysis history.
- Supporting additional document formats and configurable analysis criteria.

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes and add relevant tests.
4. Commit your changes with a descriptive message.
5. Open a pull request describing your changes.

For major changes, consider opening an issue first to discuss the proposed implementation.

## License

No license has been specified yet. If you intend to make this project open source, add an appropriate `LICENSE` file and update this section.

---

**Built with Python and FastAPI.**
