import json
import os
import pytest
from app.main import app
from app.auth import generate_token
from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

@pytest.fixture
def auth_headers():
    """Valid JWT token headers for protected routes."""
    token = generate_token('admin')
    return {'Authorization': f'Bearer {token}'}

class TestHealth:
    def test_health_returns_200(self, client):
        res = client.get('/health')
        assert res.status_code == 200
        assert res.get_json()['status'] == 'OK'

class TestAuth:

    def test_login_returns_token(self, client):
        res = client.post('/login',
        data=json.dumps({
            'username': os.environ.get('ADMIN_USERNAME', 'admin'),
            'password': os.environ.get('ADMIN_PASSWORD', 'qa_secure_pass_2024!')
        }),
        content_type='application/json')
        assert res.status_code == 200
        assert 'token' in res.get_json()

    def test_login_wrong_password_returns_401(self, client):
        res = client.post('/login',
            data=json.dumps({'username': 'admin', 'password': 'wrongpass'}),
            content_type='application/json')
        assert res.status_code == 401

    def test_login_missing_fields_returns_400(self, client):
        res = client.post('/login',
            data=json.dumps({'username': 'admin'}),
            content_type='application/json')
        assert res.status_code == 400

    def test_protected_route_without_token_returns_401(self, client):
        res = client.post('/testcases',
            data=json.dumps({'title': 'No Token', 'priority': 'Low'}),
            content_type='application/json')
        assert res.status_code == 401

    def test_protected_route_with_invalid_token_returns_401(self, client):
        res = client.post('/testcases',
            data=json.dumps({'title': 'Bad Token', 'priority': 'Low'}),
            content_type='application/json',
            headers={'Authorization': 'Bearer totally.fake.token'})
        assert res.status_code == 401

    def test_protected_route_with_valid_token_succeeds(self, client, auth_headers):
        res = client.post('/testcases',
            data=json.dumps({'title': 'Auth Test', 'priority': 'High'}),
            content_type='application/json',
            headers=auth_headers)
        assert res.status_code == 201

class TestTestCasesAPI:
    def test_create_test_case(self, client, auth_headers):
        res = client.post('/testcases',
            data=json.dumps({'title': 'API Login Test', 'priority': 'High'}),
            content_type='application/json',
            headers=auth_headers)
        assert res.status_code == 201
        assert 'id' in res.get_json()

    def test_missing_required_fields_returns_400(self, client, auth_headers):
        res = client.post('/testcases',
            data=json.dumps({'title': 'No Priority'}),
            content_type='application/json',
            headers=auth_headers)
        assert res.status_code == 400

    def test_list_test_cases_returns_envelope(self, client, auth_headers):
        client.post('/testcases',
            data=json.dumps({'title': 'List Test', 'priority': 'Low'}),
            content_type='application/json',
            headers=auth_headers)
        res = client.get('/testcases')
        assert res.status_code == 200
        body = res.get_json()
        assert 'data' in body
        assert 'metadata' in body
        assert isinstance(body['data'], list)

    def test_list_test_cases_metadata_fields(self, client):
        res = client.get('/testcases')
        meta = res.get_json()['metadata']
        assert 'current_page' in meta
        assert 'per_page' in meta
        assert 'total_records' in meta
        assert 'total_pages' in meta

    def test_get_single_test_case(self, client, auth_headers):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Single Test', 'priority': 'Medium'}),
            content_type='application/json',
            headers=auth_headers)
        tc_id = post.get_json()['id']
        res = client.get(f'/testcases/{tc_id}')
        assert res.status_code == 200
        assert res.get_json()['title'] == 'Single Test'

    def test_get_nonexistent_returns_404(self, client):
        res = client.get('/testcases/9999')
        assert res.status_code == 404

    def test_update_test_case(self, client, auth_headers):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Update Me', 'priority': 'Low'}),
            content_type='application/json',
            headers=auth_headers)
        tc_id = post.get_json()['id']
        res = client.put(f'/testcases/{tc_id}',
            data=json.dumps({'status': 'Closed'}),
            content_type='application/json',
            headers=auth_headers)
        assert res.status_code == 200

    def test_update_without_token_returns_401(self, client, auth_headers):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Update Auth Test', 'priority': 'Low'}),
            content_type='application/json',
            headers=auth_headers)
        tc_id = post.get_json()['id']
        res = client.put(f'/testcases/{tc_id}',
            data=json.dumps({'status': 'Closed'}),
            content_type='application/json')
        assert res.status_code == 401

    def test_delete_test_case(self, client, auth_headers):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Delete Me', 'priority': 'Low'}),
            content_type='application/json',
            headers=auth_headers)
        tc_id = post.get_json()['id']
        res = client.delete(f'/testcases/{tc_id}', headers=auth_headers)
        assert res.status_code == 200

    def test_delete_without_token_returns_401(self, client, auth_headers):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Delete Auth Test', 'priority': 'Low'}),
            content_type='application/json',
            headers=auth_headers)
        tc_id = post.get_json()['id']
        res = client.delete(f'/testcases/{tc_id}')
        assert res.status_code == 401

class TestPaginationAPI:
    def test_default_page_and_per_page(self, client):
        res = client.get('/testcases')
        meta = res.get_json()['metadata']
        assert meta['current_page'] == 1
        assert meta['per_page'] == 20

    def test_custom_page_and_per_page(self, client):
        res = client.get('/testcases?page=1&per_page=5')
        assert res.status_code == 200
        assert res.get_json()['metadata']['per_page'] == 5

    def test_invalid_page_param_returns_400(self, client):
        res = client.get('/testcases?page=abc')
        assert res.status_code == 400

    def test_invalid_per_page_param_returns_400(self, client):
        res = client.get('/testcases?per_page=xyz')
        assert res.status_code == 400

    def test_per_page_above_max_resets_to_default(self, client):
        res = client.get('/testcases?per_page=999')
        assert res.status_code == 200
        assert res.get_json()['metadata']['per_page'] == 20

    def test_page_out_of_range_returns_404(self, client, auth_headers):
        client.post('/testcases',
            data=json.dumps({'title': 'Only One', 'priority': 'Low'}),
            content_type='application/json',
            headers=auth_headers)
        res = client.get('/testcases?page=999&per_page=20')
        assert res.status_code == 404

    def test_empty_db_returns_empty_data(self, client):
        res = client.get('/testcases')
        body = res.get_json()
        assert body['data'] == []
        assert body['metadata']['total_records'] == 0

    def test_data_count_matches_per_page(self, client, auth_headers):
        for i in range(5):
            client.post('/testcases',
                data=json.dumps({'title': f'TC{i}', 'priority': 'Low'}),
                content_type='application/json',
                headers=auth_headers)
        res = client.get('/testcases?page=1&per_page=3')
        assert len(res.get_json()['data']) == 3

class TestDefectsAPI:
    def test_create_defect(self, client, auth_headers):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Defect Parent', 'priority': 'High'}),
            content_type='application/json',
            headers=auth_headers)
        tc_id = post.get_json()['id']
        res = client.post(f'/testcases/{tc_id}/defects',
            data=json.dumps({'defect_title': 'Button broken', 'severity': 'Major'}),
            content_type='application/json',
            headers=auth_headers)
        assert res.status_code == 201

    def test_create_defect_without_token_returns_401(self, client, auth_headers):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Defect Auth Test', 'priority': 'High'}),
            content_type='application/json',
            headers=auth_headers)
        tc_id = post.get_json()['id']
        res = client.post(f'/testcases/{tc_id}/defects',
            data=json.dumps({'defect_title': 'Unauthorized bug', 'severity': 'Minor'}),
            content_type='application/json')
        assert res.status_code == 401

    def test_list_defects_for_case(self, client, auth_headers):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Defect List Parent', 'priority': 'High'}),
            content_type='application/json',
            headers=auth_headers)
        tc_id = post.get_json()['id']
        client.post(f'/testcases/{tc_id}/defects',
            data=json.dumps({'defect_title': 'Layout bug', 'severity': 'Minor'}),
            content_type='application/json',
            headers=auth_headers)
        res = client.get(f'/testcases/{tc_id}/defects')
        assert res.status_code == 200
        assert len(res.get_json()) == 1

    def test_list_all_defects(self, client):
        res = client.get('/defects')
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)
