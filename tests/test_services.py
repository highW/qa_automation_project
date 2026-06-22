from app.services import (
    create_test_case, get_test_cases, get_test_case,
    update_test_case, delete_test_case, create_defect, get_defects
)

class TestCreateTestCase:
    def test_creates_and_returns_id(self):
        tc_id = create_test_case('Login Test', 'Verify login flow', 'High')
        assert isinstance(tc_id, int)
        assert tc_id > 0

    def test_case_appears_in_list(self):
        create_test_case('Logout Test', 'Verify logout', 'Medium')
        cases = get_test_cases()
        assert any(c['title'] == 'Logout Test' for c in cases)

    def test_default_status_is_open(self):
        tc_id = create_test_case('Status Test', '', 'Low')
        tc = get_test_case(tc_id)
        assert tc['status'] == 'Open'

class TestGetTestCase:
    def test_get_existing(self):
        tc_id = create_test_case('Get Test', 'desc', 'High')
        tc = get_test_case(tc_id)
        assert tc['title'] == 'Get Test'
        assert tc['priority'] == 'High'

    def test_get_nonexistent_returns_none(self):
        assert get_test_case(9999) is None

class TestUpdateTestCase:
    def test_update_status(self):
        tc_id = create_test_case('Update Test', '', 'High')
        update_test_case(tc_id, status='Closed')
        tc = get_test_case(tc_id)
        assert tc['status'] == 'Closed'

    def test_update_priority(self):
        tc_id = create_test_case('Priority Test', '', 'Low')
        update_test_case(tc_id, priority='Critical')
        tc = get_test_case(tc_id)
        assert tc['priority'] == 'Critical'

class TestDeleteTestCase:
    def test_delete_removes_case(self):
        tc_id = create_test_case('Delete Test', '', 'Low')
        delete_test_case(tc_id)
        assert get_test_case(tc_id) is None

class TestDefects:
    def test_create_defect(self):
        tc_id = create_test_case('Defect Parent', '', 'High')
        d_id = create_defect(tc_id, 'Button not clickable', 'Major')
        assert d_id > 0

    def test_defects_linked_to_test_case(self):
        tc_id = create_test_case('Defect Link Test', '', 'High')
        create_defect(tc_id, 'Broken layout', 'Minor')
        defects = get_defects(tc_id)
        assert len(defects) == 1
        assert defects[0]['defect_title'] == 'Broken layout'

    def test_cascade_delete(self):
        tc_id = create_test_case('Cascade Test', '', 'High')
        create_defect(tc_id, 'Some bug', 'Critical')
        delete_test_case(tc_id)
        assert get_defects(tc_id) == []
