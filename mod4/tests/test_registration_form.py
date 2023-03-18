import unittest
from mod4.task1 import app
import json


class TestRegistrationForm(unittest.TestCase):
    """
    Тестирование коректности работы валидаторов на тестовом клиенте
    """
    def setUp(self) -> None:
        self.form_fields: dict = {
            'email': 'test@example.com',
            'phone': 9998007779,
            'name': 'Иван Иванов',
            'address': 'Крым',
            'index': 6544413,
            'comment': ''
        }
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/registration'

    def test_all_fields_passes_validation(self):
        request = self.app.post(self.base_url, json=self.form_fields)
        self.assertEqual(request.status_code, 200)

    def test_wrong_email_fail_validation(self):
        wrong_email = 'testexample.com'
        self.form_fields['email'] = wrong_email
        request = self.app.post(self.base_url, json=self.form_fields)
        self.assertEqual(request.status_code, 400)

    def test_empty_email_fail_validation(self):
        empty_email = ''
        self.form_fields['email'] = empty_email
        request = self.app.post(self.base_url, json=self.form_fields)
        self.assertEqual(request.status_code, 400)

    def test_wrong_phone_fail_validation(self):
        wrong_phone = 99999999999999999
        self.form_fields['phone'] = wrong_phone
        request = self.app.post(self.base_url, json=self.form_fields)
        self.assertEqual(request.status_code, 400)

    def test_empty_phone_fail_validation(self):
        empty_phone = ''
        self.form_fields['phone'] = empty_phone
        request = self.app.post(self.base_url, json=self.form_fields)
        self.assertEqual(request.status_code, 400)

    def test_empty_name_fail_validation(self):
        empty_name = ''
        self.form_fields['name'] = empty_name
        request = self.app.post(self.base_url, json=self.form_fields)
        self.assertEqual(request.status_code, 400)

    def test_empty_address_fail_validation(self):
        empty_address = ''
        self.form_fields['address'] = empty_address
        request = self.app.post(self.base_url, json=self.form_fields)
        self.assertEqual(request.status_code, 400)

    def test_index_as_string_fail_validation(self):
        wrong_index = '2525345q'
        self.form_fields['index'] = wrong_index
        request = self.app.post(self.base_url, json=self.form_fields)
        self.assertEqual(request.status_code, 400)


if __name__ == '__main__':
    unittest.main()
