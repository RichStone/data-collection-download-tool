import unittest
from SimpleDownload import downloader
from urllib.error import URLError

import os


class TestSimpleDownload(unittest.TestCase):
    def setUp(self):
        pass

    def test_argument_received(self):
        arg = 'http://example.com/+++1***2300+++'
        self.downloader = downloader.Downloader(arg)
        self.assertIsNotNone(self.downloader.user_input, '')

    def test_extract_base_url(self):
        arg = 'http://example.com/+++1***2300+++'
        self.downloader = downloader.Downloader(arg)
        self.assertEqual(self.downloader.BASE_URL, 'http://example.com')

        arg = 'https://www.example.com/+++1***2300+++'
        self.downloader = downloader.Downloader(arg)
        self.assertEqual(self.downloader.BASE_URL, 'https://www.example.com')

    def test_base_url_valid_connection(self):
        arg = 'https://google.com'
        self.downloader = downloader.Downloader(arg)
        http_response_code = self.downloader.validate_connection()
        self.assertGreaterEqual(http_response_code, 200)
        self.assertLessEqual(http_response_code, 299)

    def test_connection_exception_on_(self):
        with self.assertRaises(URLError):
            arg = 'https://non-existing-url-dsad.com/'
            dl = downloader.Downloader(arg)

    @unittest.skip("complete after main functions exist")
    def test_except_on_invalid_argument(self):
        with self.assertRaises(ValueError):
            # 'invalid base URL'
            arg = 'xkcd.com/+++1***2300+++'
            self.downloader = downloader.Downloader(arg)

        with self.assertRaises(ValueError):
            # 'incorrect concat delimiter'
            arg = 'https://xkcd.com/+++1***2300+++'
            self.downloader = downloader.Downloader(arg)

        with self.assertRaises(ValueError):
            # 'incorrect range delimiter'
            arg = 'https://xkcd.com/+++1***2300+++'
            self.downloader = downloader.Downloader(arg)

    @unittest.skip("find correct syntax")
    def test_except_without_argument(self):
        with self.assertRaises(ValueError):
            # something like this:
            # https://stackoverflow.com/a/3781869/5925094
            os.system("downloader.py arg")


if __name__ == '__main__':
    unittest.main()
