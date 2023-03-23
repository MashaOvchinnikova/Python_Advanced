import unittest
from unittest.mock import patch
from mod5.task2.run_code_form import app
import json
import requests


class TestRunCodeForm(unittest.TestCase):
    def setUp(self) -> None:
        self.form_fields: dict = {
            'code': "print('Hello World!')",
            'time_out': 30,
        }
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/run_code'

    @patch('requests.post')
    def test_post(self, mock_post):
        """
        POST запрос отправляется
        """
        info = self.form_fields
        resp = requests.post(self.base_url, data=json.dumps(info), headers={'Content-Type': 'application/json'})

        mock_post.assert_called_with(self.base_url, data=json.dumps(info),
                                     headers={'Content-Type': 'application/json'})

    def test_all_fields_passes_validation(self):
        """
        Все поля проходят валидацию. Пользователю возвращается результат работы программы
        """
        request = self.app.post(self.base_url, json=self.form_fields)

        self.assertEqual(request.status_code, 200)

    def test_empty_code_field_fail_validation(self):
        """
        Пустое поле кода не проходит валидацию
        """
        self.form_fields['code'] = ''
        request = self.app.post(self.base_url, json=self.form_fields)

        self.assertEqual(request.status_code, 400)

    def test_time_out_field_as_string_fail_validation(self):
        """
        Некоректный ввод тайм-аута не проходит валидацию
        """
        self.form_fields['time_out'] = '3q'
        request = self.app.post(self.base_url, json=self.form_fields)

        self.assertEqual(request.status_code, 400)

    def test_empty_time_out_field_fail_validation(self):
        """
        Пустое поле тайм-аута не проходит валидацию
        """
        self.form_fields['time_out'] = ''
        request = self.app.post(self.base_url, json=self.form_fields)

        self.assertEqual(request.status_code, 400)

    def test_time_out_field_more_than_30_second_fail_validation(self):
        """
        Тайм-аут больше 30 секунд не проходит валидацию
        """
        self.form_fields['time_out'] = 31
        request = self.app.post(self.base_url, json=self.form_fields)

        self.assertEqual(request.status_code, 400)

    def test_TimeoutExpired_exception(self):
        """
        Тайм-аут ниже, чем время исполнения
        """
        self.form_fields['time_out'] = 0
        request = self.app.post(self.base_url, json=self.form_fields)

        self.assertEqual(request.status_code, 400)

    def test_unsafe_input(self):
        """
        При небезопасном вводе в поле с кодом отправляется сообщение об ошибке
        """
        self.form_fields['code'] = 'print()"; echo "hacked'
        expected_message = 'При работе программы возникла ошибка'
        request = self.app.post(self.base_url, json=self.form_fields)

        self.assertTrue(expected_message in request.data.decode())

    def test_another_unsafe_input(self):
        """
        При небезопасном вводе в поле с кодом отправляется сообщение об ошибке
        """
        self.form_fields['code'] = "from subprocess import run" \
                                   "run(['./kill_the_system.sh'])"
        expected_message = 'При работе программы возникла ошибка'
        request = self.app.post(self.base_url, json=self.form_fields)

        self.assertTrue(expected_message in request.data.decode())




