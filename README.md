# QA Automation Project — Version 1

A Flask REST API with SQLite backend, full CRUD operations, and Pytest automation suite.

## Stack
- Python 3.12+
- Flask 3.x (REST API)
- SQLite (database)
- Pytest + pytest-html (test runner + reports)
- GitHub Actions (CI/CD)

## Setup

```bash
# Clone the repo
git clone <your-repo-url>
cd qa_automation_project

# Install dependencies
pip install -r requirements.txt

# Run the API server
python -m app.main
```

The API will be available at `http://localhost:5000`

## API Endpoints

| Method | Endpoint                          | Description            |
|--------|-----------------------------------|------------------------|
| GET    | /health                           | Health check           |
| GET    | /testcases                        | List all test cases    |
| POST   | /testcases                        | Create a test case     |
| GET    | /testcases/:id                    | Get a test case        |
| PUT    | /testcases/:id                    | Update a test case     |
| DELETE | /testcases/:id                    | Delete a test case     |
| POST   | /testcases/:id/defects            | Create a defect        |
| GET    | /testcases/:id/defects            | List defects for case  |
| GET    | /defects                          | List all defects       |

## Running Tests

```bash
# Run all tests
pytest -v

# Run with HTML report
pytest --html=report.html --self-contained-html -v

# Run specific test file
pytest tests/test_api.py -v
```

## Example Usage

```bash
# Create a test case
curl -X POST http://localhost:5000/testcases \
  -H "Content-Type: application/json" \
  -d '{"title": "Login Test", "description": "Verify user login", "priority": "High"}'

# List all test cases
curl http://localhost:5000/testcases

# Log a defect
curl -X POST http://localhost:5000/testcases/1/defects \
  -H "Content-Type: application/json" \
  -d '{"defect_title": "Login button unresponsive", "severity": "Major"}'
```

## Project Structure

```
qa_automation_project/
├── app/
│   ├── __init__.py
│   ├── database.py      # DB connection context manager
│   ├── models.py        # SQL schema
│   ├── services.py      # Business logic / CRUD
│   └── main.py          # Flask routes
├── tests/
│   ├── conftest.py      # Fixtures (isolated test DB)
│   ├── test_services.py # Unit tests for service layer
│   └── test_api.py      # Integration tests via Flask test client
├── .github/workflows/
│   └── qa.yml           # GitHub Actions CI
├── requirements.txt
└── README.md
```
