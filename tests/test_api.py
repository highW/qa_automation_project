import json
import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

class TestHealth:
    def test_health_returns_200(self, client):
        res = client.get('/health')
        assert res.status_code == 200
        assert res.get_json()['status'] == 'OK'

class TestTestCasesAPI:
    def test_create_test_case(self, client):
        res = client.post('/testcases',
            data=json.dumps({'title': 'API Login Test', 'priority': 'High'}),
            content_type='application/json')
        assert res.status_code == 201
        assert 'id' in res.get_json()

    def test_missing_required_fields_returns_400(self, client):
        res = client.post('/testcases',
            data=json.dumps({'title': 'No Priority'}),
            content_type='application/json')
        assert res.status_code == 400

    def test_list_test_cases_returns_envelope(self, client):
        client.post('/testcases',
            data=json.dumps({'title': 'List Test', 'priority': 'Low'}),
            content_type='application/json')
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

    def test_get_single_test_case(self, client):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Single Test', 'priority': 'Medium'}),
            content_type='application/json')
        tc_id = post.get_json()['id']
        res = client.get(f'/testcases/{tc_id}')
        assert res.status_code == 200
        assert res.get_json()['title'] == 'Single Test'

    def test_get_nonexistent_returns_404(self, client):
        res = client.get('/testcases/9999')
        assert res.status_code == 404

    def test_update_test_case(self, client):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Update Me', 'priority': 'Low'}),
            content_type='application/json')
        tc_id = post.get_json()['id']
        res = client.put(f'/testcases/{tc_id}',
            data=json.dumps({'status': 'Closed'}),
            content_type='application/json')
        assert res.status_code == 200

    def test_delete_test_case(self, client):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Delete Me', 'priority': 'Low'}),
            content_type='application/json')
        tc_id = post.get_json()['id']
        res = client.delete(f'/testcases/{tc_id}')
        assert res.status_code == 200

class TestPaginationAPI:
    def test_default_page_and_per_page(self, client):
        res = client.get('/testcases')
        meta = res.get_json()['metadata']
        assert meta['current_page'] == 1
        assert meta['per_page'] == 20

    def test_custom_page_and_per_page(self, client):
        res = client.get('/testcases?page=1&per_page=5')
        assert res.status_code == 200
        meta = res.get_json()['metadata']
        assert meta['per_page'] == 5

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

    def test_page_out_of_range_returns_404(self, client):
        # no records exist, page 2 should be out of range
        client.post('/testcases',
            data=json.dumps({'title': 'Only One', 'priority': 'Low'}),
            content_type='application/json')
        res = client.get('/testcases?page=999&per_page=20')
        assert res.status_code == 404

    def test_empty_db_returns_empty_data(self, client):
        res = client.get('/testcases')
        body = res.get_json()
        assert body['data'] == []
        assert body['metadata']['total_records'] == 0

    def test_data_count_matches_per_page(self, client):
        for i in range(5):
            client.post('/testcases',
                data=json.dumps({'title': f'TC{i}', 'priority': 'Low'}),
                content_type='application/json')
        res = client.get('/testcases?page=1&per_page=3')
        assert len(res.get_json()['data']) == 3

class TestDefectsAPI:
    def test_create_defect(self, client):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Defect Parent', 'priority': 'High'}),
            content_type='application/json')
        tc_id = post.get_json()['id']
        res = client.post(f'/testcases/{tc_id}/defects',
            data=json.dumps({'defect_title': 'Button broken', 'severity': 'Major'}),
            content_type='application/json')
        assert res.status_code == 201

    def test_list_defects_for_case(self, client):
        post = client.post('/testcases',
            data=json.dumps({'title': 'Defect List Parent', 'priority': 'High'}),
            content_type='application/json')
        tc_id = post.get_json()['id']
        client.post(f'/testcases/{tc_id}/defects',
            data=json.dumps({'defect_title': 'Layout bug', 'severity': 'Minor'}),
            content_type='application/json')
        res = client.get(f'/testcases/{tc_id}/defects')
        assert res.status_code == 200
        assert len(res.get_json()) == 1

    def test_list_all_defects(self, client):
        res = client.get('/defects')
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)
