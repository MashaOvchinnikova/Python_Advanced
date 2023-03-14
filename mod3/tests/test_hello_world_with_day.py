import unittest
from mod3.hello_world_with_day import app
from datetime import datetime

weekdays_dict: dict = {0: 'Понедельника',
                       1: 'Вторника',
                       2: 'Среды',
                       3: 'Четверга',
                       4: 'Пятницы',
                       5: 'Субботы',
                       6: 'Воскресенья'}


class TestHelloWorldWithDay(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello_world/'

    def test_can_get_correct_username_with_weekdate(self):
        username = 'any'
        weekday = weekdays_dict[datetime.today().weekday()]
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(weekday in response_text)


if __name__ == '__main__':
    unittest.main()
