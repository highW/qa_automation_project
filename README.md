QA Automation Project — Version 1
A production‑style Flask REST API with a SQLite backend, full CRUD operations, and a Pytest automation suite with CI/CD via GitHub Actions.
Designed as a real‑world QA engineering portfolio project demonstrating API testing, service‑layer validation, and automated reporting.

📛 Badges
![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-07405E?logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white)
blue

📌 Tech Stack
Python 3.12+

Flask 3.x — REST API framework

SQLite — lightweight relational DB

Pytest + pytest‑html — automated test suite + HTML reports

GitHub Actions — CI pipeline for automated test execution

📐 Architecture Overview
Code
Client → Flask Routes → Service Layer → SQLite Database
                     ↑
                Pytest Suite
Routes handle HTTP requests

Services contain business logic

Database stores test cases + defects

Pytest validates both API and service layer

⚙️ Setup Instructions
bash
# Clone the repo
git clone https://github.com/highW/qa_automation_project.git
cd qa_automation_project

# Install dependencies
pip install -r requirements.txt

# Run the API server
python -m app.main
API runs at:
👉 http://localhost:5000

🗄️ Environment Variables (Optional)
Create .env if needed:

Code
FLASK_ENV=development
DATABASE_URL=sqlite:///testcases.db
🧩 API Endpoints
Method	Endpoint	Description
GET	/health	Health check
GET	/testcases	List all test cases
POST	/testcases	Create a test case
GET	/testcases/:id	Get a test case
PUT	/testcases/:id	Update a test case
DELETE	/testcases/:id	Delete a test case
POST	/testcases/:id/defects	Create a defect
GET	/testcases/:id/defects	List defects for case
GET	/defects	List all defects


📦 Example JSON Payloads
Create Test Case
json
{
  "title": "Login Test",
  "description": "Verify user login",
  "priority": "High"
}
Create Defect
json
{
  "defect_title": "Login button unresponsive",
  "severity": "Major"
}
🧪 Running Tests
bash
# Run all tests
pytest -v

# Run with HTML report
pytest --html=report.html --self-contained-html -v

# Run specific test file
pytest tests/test_api.py -v
🧱 Database Schema
Test Cases Table
Field	Type
id	INTEGER
title	TEXT
description	TEXT
priority	TEXT


Defects Table
Field	Type
id	INTEGER
testcase_id	INTEGER
defect_title	TEXT
severity	TEXT


🔍 Test Strategy
This project includes:

Unit Tests
Validate service‑layer logic

Mock DB operations

Ensure CRUD correctness

Integration Tests
Use Flask test client

Validate full request → response flow

Test error handling and edge cases

Smoke Tests
/health endpoint

Basic CRUD sanity checks

🚀 CI/CD Pipeline (GitHub Actions)
The workflow:

Installs dependencies

Spins up Flask app

Runs full Pytest suite

Generates HTML report

Fails PRs on test failure

Located at:

Code
.github/workflows/qa.yml
📂 Project Structure
Code
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
🛠️ Troubleshooting
Port already in use
Code
OSError: [Errno 98] Address already in use
Fix:

Code
killall python
Database locked
Delete the SQLite file:

Code
rm testcases.db
📈 Roadmap
[ ] Add JWT authentication

[ ] Add pagination to endpoints

[ ] Add Swagger/OpenAPI docs

[ ] Add Dockerfile + docker-compose

[ ] Add load tests (Locust or k6)

[ ] Add test coverage badge

🤝 Contributing
PRs are welcome.
Follow conventional commits and ensure all tests pass.

📜 License
MIT Licens