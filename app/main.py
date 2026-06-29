from flask import Flask, request, jsonify
from app.services import (
    init_db, create_test_case, get_test_cases_paginated, get_test_cases_count, get_test_case,
    update_test_case, delete_test_case, create_defect, get_defects
)

app = Flask(__name__)
init_db()

@app.get('/health')
def health():
    return jsonify(status='OK', message='QA Automation API is running')

# --- Test Cases ---

@app.post('/testcases')
def add_case():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('priority'):
        return jsonify(error='title and priority are required'), 400
    tc_id = create_test_case(data['title'], data.get('description', ''), data['priority'])
    return jsonify(id=tc_id, message='Test case created'), 201

@app.get('/testcases')
def list_cases():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
    except ValueError:
        return jsonify(error='page and per_page must be integers'), 400

    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 20

    offset = (page - 1) * per_page
    total = get_test_cases_count()
    total_pages = (total + per_page - 1) // per_page

    if page > total_pages and total_pages > 0:
        return jsonify(error='Page out of range'), 404

    return jsonify({
        "data": get_test_cases_paginated(limit=per_page, offset=offset),
        "metadata": {
            "current_page": page,
            "per_page": per_page,
            "total_records": total,
            "total_pages": total_pages
        }
    })

@app.get('/testcases/<int:tc_id>')
def get_case(tc_id):
    tc = get_test_case(tc_id)
    if not tc:
        return jsonify(error='Not found'), 404
    return jsonify(tc)

@app.put('/testcases/<int:tc_id>')
def update_case(tc_id):
    data = request.get_json()
    allowed = {k: v for k, v in data.items() if k in ('title', 'description', 'priority', 'status')}
    if not allowed:
        return jsonify(error='No valid fields to update'), 400
    update_test_case(tc_id, **allowed)
    return jsonify(message='Updated')

@app.delete('/testcases/<int:tc_id>')
def delete_case(tc_id):
    delete_test_case(tc_id)
    return jsonify(message='Deleted')

# --- Defects ---

@app.post('/testcases/<int:tc_id>/defects')
def add_defect(tc_id):
    data = request.get_json()
    if not data or not data.get('defect_title') or not data.get('severity'):
        return jsonify(error='defect_title and severity are required'), 400
    d_id = create_defect(tc_id, data['defect_title'], data['severity'])
    return jsonify(id=d_id, message='Defect created'), 201

@app.get('/testcases/<int:tc_id>/defects')
def list_defects(tc_id):
    return jsonify(get_defects(tc_id))

@app.get('/defects')
def all_defects():
    return jsonify(get_defects())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
