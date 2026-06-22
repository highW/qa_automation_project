# QA Automation Project

> Production-style Flask REST API with SQLite, full CRUD, and a Pytest automation suite — built as a real-world QA engineering portfolio project.

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-07405E?logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-22%20Tests-0A9EDC?logo=pytest)
![CI](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white)

---

## What This Is

A self-contained QA engineering portfolio project demonstrating:

- **API design** — RESTful Flask routes for test case and defect management
- **Service-layer architecture** — business logic decoupled from routes and DB
- **Automated testing** — 22 Pytest tests covering unit, integration, and edge cases
- **CI/CD** — GitHub Actions pipeline with HTML report artifacts

---

## Stack

| Layer | Technology |
|---|---|
| API | Flask 3.x |
| Database | SQLite via `sqlite3` context manager |
| Testing | Pytest + pytest-html |
| CI/CD | GitHub Actions |
| Language | Python 3.12+ |

---

## Architecture

```
Client
  └── Flask Routes (main.py)
        └── Service Layer (services.py)
              └── SQLite Database (database.py)

Pytest Suite
  ├── test_api.py       → Integration tests via Flask test client
  └── test_services.py  → Unit tests for service layer
```

---

## Setup

```bash
git clone https://github.com/highW/qa_automation_project.git
cd qa_automation_project
pip install -r requirements.txt
python -m app.main
```

API runs at `http://localhost:5000`

---

## API Reference

### Test Cases

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/testcases` | List all test cases |
| `POST` | `/testcases` | Create a test case |
| `GET` | `/testcases/:id` | Get a test case |
| `PUT` | `/testcases/:id` | Update a test case |
| `DELETE` | `/testcases/:id` | Delete a test case |

### Defects

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/testcases/:id/defects` | Create a defect |
| `GET` | `/testcases/:id/defects` | List defects for a case |
| `GET` | `/defects` | List all defects |

### Payloads

**Create test case**
```json
{
  "title": "Login Test",
  "description": "Verify user login flow",
  "priority": "High"
}
```

**Create defect**
```json
{
  "defect_title": "Login button unresponsive",
  "severity": "Major"
}
```

---

## Running Tests

```bash
# All tests
pytest -v

# With HTML report
pytest --html=report.html --self-contained-html -v

# Single file
pytest tests/test_api.py -v
```

**22/22 passing** — isolated per-test DB via `autouse` fixture, no shared state.

---

## Test Strategy

| Layer | File | Coverage |
|---|---|---|
| Unit | `test_services.py` | CRUD logic, default values, cascade delete |
| Integration | `test_api.py` | HTTP routes, status codes, error handling |

Each test runs against a fresh SQLite database — created and destroyed per test via `conftest.py`.

---

## Project Structure

```
qa_automation_project/
├── app/
│   ├── database.py       # DB connection context manager
│   ├── models.py         # SQL schema
│   ├── services.py       # Business logic / CRUD
│   └── main.py           # Flask routes
├── tests/
│   ├── conftest.py       # Fixtures — isolated test DB per test
│   ├── test_services.py  # Unit tests
│   └── test_api.py       # Integration tests
├── .github/workflows/
│   └── qa.yml            # CI pipeline
├── requirements.txt
└── README.md
```

---

## Troubleshooting

**Port already in use**
```bash
killall python
```

**Database locked**
```bash
rm qa.db
```

---

## Roadmap

- [ ] Input validation — enforce allowed values for `priority` and `severity`
- [ ] JWT authentication
- [ ] Pagination on list endpoints
- [ ] Swagger / OpenAPI docs
- [ ] Dockerfile + docker-compose
- [ ] Load tests (k6)
- [ ] Test coverage badge

---

## License

MIT
