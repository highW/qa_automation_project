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

    def test_list_test_cases(self, client):
        client.post('/testcases',
            data=json.dumps({'title': 'List Test', 'priority': 'Low'}),
            content_type='application/json')
        res = client.get('/testcases')
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

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
