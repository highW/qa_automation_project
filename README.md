e# QA Automation Project

> Production-style Flask REST API with SQLite, JWT authentication, pagination, full CRUD, and a Pytest automation suite — built as a real-world QA engineering portfolio project.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-07405E?logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-46%20Tests-0A9EDC?logo=pytest)
![CI](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white)

---

## What This Is

A self-contained QA engineering portfolio project demonstrating:

- **API design** — RESTful Flask routes for test case and defect management
- **JWT authentication** — stateless token-based security on all write operations
- **Pagination** — offset/limit pagination with metadata envelope on list endpoints
- **Service-layer architecture** — business logic decoupled from routes and DB
- **Automated testing** — 46 Pytest tests covering unit, integration, auth, and edge cases
- **CI/CD** — GitHub Actions pipeline with HTML report artifacts

---

## Stack

| Layer | Technology |
|---|---|
| API | Flask 3.x |
| Database | SQLite via `sqlite3` context manager |
| Auth | PyJWT (HS256) + python-dotenv |
| Testing | Pytest + pytest-html |
| CI/CD | GitHub Actions |
| Language | Python 3.11+ |

---

## Architecture

```
Client
  └── Flask Routes (main.py)
        ├── Auth Middleware (auth.py)   ← JWT decorator on write routes
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
```

Create a `.env` file in the project root:

```
JWT_SECRET_KEY=your_random_32_plus_character_secret_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password_here
```

Run the server:

```bash
python -m app.main
```

API runs at `http://localhost:5000`

---

## Authentication

All write operations (`POST`, `PUT`, `DELETE`) require a valid JWT token.  
`GET` endpoints are public.

**Step 1 — Get a token:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

Response:
```json
{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." }
```

**Step 2 — Use the token:**
```bash
curl -X POST http://localhost:5000/testcases \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token>" \
  -d '{"title": "Login Test", "priority": "High"}'
```

Tokens expire after **30 minutes**. Re-authenticate to get a new one.

---

## API Reference

### Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/login` | ❌ | Get a JWT token |

### Test Cases

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/health` | ❌ | Health check |
| `GET` | `/testcases` | ❌ | List test cases (paginated) |
| `POST` | `/testcases` | ✅ | Create a test case |
| `GET` | `/testcases/:id` | ❌ | Get a single test case |
| `PUT` | `/testcases/:id` | ✅ | Update a test case |
| `DELETE` | `/testcases/:id` | ✅ | Delete a test case |

### Defects

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/testcases/:id/defects` | ✅ | Create a defect |
| `GET` | `/testcases/:id/defects` | ❌ | List defects for a case |
| `GET` | `/defects` | ❌ | List all defects |

---

## Pagination

`GET /testcases` supports offset/limit pagination via query parameters:

```
GET /testcases?page=2&per_page=10
```

| Parameter | Default | Max | Description |
|---|---|---|---|
| `page` | `1` | — | Page number |
| `per_page` | `20` | `100` | Results per page |

Response envelope:
```json
{
  "data": [ { "id": 1, "title": "Login Test", ... } ],
  "metadata": {
    "current_page": 1,
    "per_page": 20,
    "total_records": 47,
    "total_pages": 3
  }
}
```

---

## Payloads

**Login**
```json
{ "username": "admin", "password": "your_password" }
```

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
# All tests (use venv Python)
.venv\Scripts\python.exe -m pytest tests/ -v

# With HTML report
.venv\Scripts\python.exe -m pytest tests/ --html=report.html --self-contained-html -v

# Single file
.venv\Scripts\python.exe -m pytest tests/test_api.py -v
```

**46/46 passing** — isolated per-test DB via `autouse` fixture, no shared state.

---

## Test Strategy

| Layer | File | Coverage |
|---|---|---|
| Unit | `test_services.py` | CRUD logic, pagination, default values, cascade delete |
| Integration | `test_api.py` | HTTP routes, JWT auth, pagination, status codes, error handling |

### Auth test cases
- Login returns token ✅
- Wrong password returns 401 ✅
- Missing fields returns 400 ✅
- Protected route without token returns 401 ✅
- Protected route with invalid token returns 401 ✅
- Protected route with valid token succeeds ✅

### Pagination test cases
- Default page and per_page values ✅
- Custom page and per_page ✅
- Invalid params return 400 ✅
- per_page above max resets to default ✅
- Page out of range returns 404 ✅
- Empty DB returns empty data ✅

---

## Project Structure

```
qa_automation_project/
├── app/
│   ├── auth.py           # JWT token generation + middleware decorator
│   ├── database.py       # DB connection context manager
│   ├── models.py         # SQL schema
│   ├── services.py       # Business logic / CRUD + pagination
│   └── main.py           # Flask routes
├── tests/
│   ├── conftest.py       # Fixtures — isolated test DB per test
│   ├── test_services.py  # Unit tests
│   └── test_api.py       # Integration tests
├── .github/workflows/
│   └── qa.yml            # CI pipeline
├── .env                  # Local secrets (gitignored)
├── requirements.txt
└── README.md
```

---

## Troubleshooting

**Windows curl issues**

PowerShell's `curl` is actually `Invoke-WebRequest` and doesn't support `-X`, `-H`, or `-d` flags. Use the `$body` variable approach:
```powershell
$body = '{"username":"yourMan","password":"your_password"}'
curl.exe -X POST http://localhost:5000/login -H "Content-Type: application/json" -d $body
```
If you still get JSON errors, use the Python one-liner instead — see the Authentication section.

**Port already in use**
```bash
killall python
```

**Database locked**
```bash
rm qa.db
```

**ModuleNotFoundError: No module named 'jwt' or 'dotenv'**

Make sure you're using the venv Python, not system Python:
```bash
.venv\Scripts\python.exe -m app.main
.venv\Scripts\python.exe -m pytest tests/ -v
```

---

## Roadmap

- [x] JWT authentication
- [x] Pagination on list endpoints
- [ ] Input validation — enforce allowed values for `priority` and `severity`
- [ ] Swagger / OpenAPI docs
- [ ] Dockerfile + docker-compose
- [ ] Load tests (k6)
- [ ] Test coverage badge

---

## License

MIT
