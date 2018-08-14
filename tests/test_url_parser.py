import unittest
from url_downloader import url_argument_parser
from urllib.error import URLError

import os


class TestUrlParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_argument_received(self):
        arg = 'http://example.com/+++1***2300+++'
        self.parser = url_argument_parser.Parser(arg)
        self.assertIsNotNone(self.parser.user_input, '')

    def test_extract_base_url(self):
        arg = 'http://example.com/+++1***2300+++'
        self.parser = url_argument_parser.Parser(arg)
        self.assertEqual(self.parser.BASE_URL, 'http://example.com')

        arg = 'https://www.example.com/+++1***2300+++'
        self.parser = url_argument_parser.Parser(arg)
        self.assertEqual(self.parser.BASE_URL, 'https://www.example.com')

    def test_base_url_valid_connection(self):
        arg = 'https://google.com'
        self.parser = url_argument_parser.Parser(arg)
        http_response_code = self.parser.validate_connection()
        self.assertGreaterEqual(http_response_code, 200)
        self.assertLessEqual(http_response_code, 299)

    def test_connection_exception_on_(self):
        with self.assertRaises(URLError):
            arg = 'https://non-existing-url-dsad.com/'
            dl = url_argument_parser.Parser(arg)

    def test_extract_custom_part(self):
        arg = 'http://example.com/+++1***2300+++'
        self.parser = url_argument_parser.Parser(arg)
        self.assertEqual('/+++1***2300+++', self.parser.extract_custom_part())

        arg = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed+++0001***0928+++.xml.gz'
        self.parser = url_argument_parser.Parser(arg)
        self.assertEqual('/pubmed/baseline/pubmed+++0001***0928+++.xml.gz', self.parser.extract_custom_part())

    @unittest.skip('activate after finishing parser')
    def test_except_on_invalid_concat_input(self):
        with self.assertRaises(ValueError):
            # 'incorrect concat delimiter'
            arg = 'https://xkcd.com/+++1***2300+++'
            self.parser = url_argument_parser.Parser(arg)

        with self.assertRaises(ValueError):
            # 'incorrect range delimiter'
            arg = 'https://xkcd.com/##1++2300##'
            self.parser = url_argument_parser.Parser(arg)

    @unittest.skip("find correct syntax")
    def test_except_without_argument(self):
        with self.assertRaises(ValueError):
            # something like this:
            # https://stackoverflow.com/a/3781869/5925094
            os.system("downloader.py arg")


if __name__ == '__main__':
    unittest.main()
