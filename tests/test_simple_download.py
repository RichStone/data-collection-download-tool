import unittest
from SimpleDownload import downloader

import os

class TestSimpleDownload(unittest.TestCase):
    def setUp(self):
        pass

    def test_argument_received(self):
        arg = 'http://xkcd.com/+++1***2300+++'
        self.downloader = downloader.Downloader(arg)
        self.assertIsNotNone(self.downloader.user_input, '')

    def test_except_on_invalid_argument(self):
        with self.assertRaises(ValueError):
            print('invalid base URL')
            arg = 'xkcd.com/+++1***2300+++'
        with self.assertRaises(ValueError):
            print('missing concat sequence')
            arg = 'https://xkcd.com/+++1***2300+++'
        with self.assertRaises(ValueError):
            print('missing range sequence')
            arg = 'https://xkcd.com/+++1***2300+++'

    # TODO:
    # def test_except_without_argument(self):
    #     with self.assertRaises(ValueError):
    #         # something like this:
    #         # https://stackoverflow.com/a/3781869/5925094
    #         os.system("downloader.py arg")


if __name__ == '__main__':
    unittest.main()
