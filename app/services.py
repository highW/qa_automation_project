from app.database import get_connection
from app.models import SCHEMA

def init_db():
    with get_connection() as conn:
        conn.executescript(SCHEMA)
        conn.commit()

def create_test_case(title, description, priority):
    with get_connection() as conn:
        cur = conn.execute(
            'INSERT INTO test_cases(title,description,priority) VALUES (?,?,?)',
            (title, description, priority)
        )
        conn.commit()
        return cur.lastrowid
    
def get_test_cases_paginated(limit=20, offset=0):
    with get_connection() as conn:
        # Use SQL LIMIT and OFFSET to fetch only a slice of data
        query = 'SELECT * FROM test_cases LIMIT ? OFFSET ?'
        rows = conn.execute(query, (limit, offset)).fetchall()
        return [dict(r) for r in rows]

def get_test_cases_count():
    with get_connection() as conn:
        row = conn.execute('SELECT COUNT(*) as total FROM test_cases').fetchone()
        return row['total'] if row else 0

def get_test_case(tc_id):
    with get_connection() as conn:
        row = conn.execute('SELECT * FROM test_cases WHERE id=?', (tc_id,)).fetchone()
        return dict(row) if row else None

def update_test_case(tc_id, **kwargs):
    fields = ', '.join(f"{k}=?" for k in kwargs)
    values = list(kwargs.values()) + [tc_id]
    with get_connection() as conn:
        conn.execute(f'UPDATE test_cases SET {fields} WHERE id=?', values)
        conn.commit()

def delete_test_case(tc_id):
    with get_connection() as conn:
        conn.execute('DELETE FROM test_cases WHERE id=?', (tc_id,))
        conn.commit()

def create_defect(test_case_id, defect_title, severity):
    with get_connection() as conn:
        cur = conn.execute(
            'INSERT INTO defects(test_case_id, defect_title, severity) VALUES (?,?,?)',
            (test_case_id, defect_title, severity)
        )
        conn.commit()
        return cur.lastrowid

def get_defects(test_case_id=None):
    with get_connection() as conn:
        if test_case_id:
            rows = conn.execute('SELECT * FROM defects WHERE test_case_id=?', (test_case_id,)).fetchall()
        else:
            rows = conn.execute('SELECT * FROM defects').fetchall()
        return [dict(r) for r in rows]
