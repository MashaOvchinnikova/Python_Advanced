import unittest
from mod3.decrypt import decrypt


class TestDecrypt(unittest.TestCase):

    def test_decrypt_with_one_dot(self):
        self.assertTrue(decrypt('абра-кадабра.') == 'абра-кадабра')
        self.assertTrue(decrypt('.') == '')

    def test_decrypt_with_two_dots(self):
        self.assertTrue(decrypt('абраа..-кадабра') == 'абра-кадабра')
        self.assertTrue(decrypt('абра--..кадабра') == 'абра-кадабра')

    def test_decrypt_with_one_and_two_dots(self):
        self.assertTrue(decrypt('абраа..-.кадабра') == 'абра-кадабра')
        self.assertTrue(decrypt('абрау...-кадабра') == 'абра-кадабра')
        self.assertTrue(decrypt('абра........') == '')
        self.assertTrue(decrypt('абр......a.') == 'a')
        self.assertTrue(decrypt('1..2.3') == '23')
        self.assertTrue(decrypt('1.......................') == '')


if __name__ == '__main__':
    unittest.main()

