SCHEMA = '''
CREATE TABLE IF NOT EXISTS test_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT,
    priority TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Open'
);

CREATE TABLE IF NOT EXISTS defects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_case_id INTEGER NOT NULL,
    defect_title TEXT NOT NULL,
    severity TEXT NOT NULL,
    FOREIGN KEY(test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE
);
'''
