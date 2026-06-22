import pytest
from pathlib import Path
import app.database as db_module

TEST_DB = Path(__file__).parent.parent / "qa_test.db"
db_module.DB_PATH = TEST_DB

@pytest.fixture(autouse=True)
def clean_db():
    """Fresh DB for every test."""
    if TEST_DB.exists():
        TEST_DB.unlink()
    from app.services import init_db
    init_db()
    yield
    if TEST_DB.exists():
        TEST_DB.unlink()
