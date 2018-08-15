import unittest
from url_downloader import url_argument_parser
from urllib.error import URLError

import os


class TestUrlParser(unittest.TestCase):
    def setUp(self):
        self.parser = url_argument_parser.Parser()

    def test_argument_received(self):
        user_input = ''
        with self.assertRaises(ValueError):
            self.parser.build_clean_url(user_input)

        user_input = None
        with self.assertRaises(ValueError):
            self.parser.build_clean_url(user_input)

        user_input = 13245
        with self.assertRaises(ValueError):
            self.parser.build_clean_url(user_input)

    def test_extract_base_url(self):
        user_input = 'http://example.com/+++1***2300+++'
        base_url = self.parser.extract_base_url(user_input)
        self.assertEqual(base_url, 'http://example.com')

        user_input = 'https://www.example.com/+++1***2300+++'
        base_url = self.parser.extract_base_url(user_input)
        self.assertEqual(base_url, 'https://www.example.com')

    def test_base_url_valid_connection(self):
        url = 'https://google.com'
        http_response_code = self.parser.validate_base_url_connection(url)
        self.assertEqual(http_response_code, 200)

    def test_connection_exception_on_(self):
        with self.assertRaises(URLError):
            url = 'https://non-existing-url-dsad.com/'
            self.parser.validate_base_url_connection(url)

    def test_extract_custom_part(self):
        user_input = 'http://example.com/++1**2300++'
        self.assertEqual('/++1**2300++', self.parser.extract_custom_url_part(user_input))

        user_input = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed+++0001***0928+++.xml.gz'
        self.assertEqual('/pubmed/baseline/pubmed+++0001***0928+++.xml.gz', self.parser.extract_custom_url_part(user_input))

    def test_extract_ranges(self):
        custom_url_part = '/pubmed++0001**0928++.xml.gz'
        ranges = [{
            'start_from': '0001',
            'end_at': '0928'
        }]
        self.assertEqual(ranges, self.parser.extract_ranges(custom_url_part))

        custom_url_part = 'http://datagoodie.com/month/++1**12++/day/++1**30++'
        ranges = [{
            'start_from': '1',
            'end_at': '12'
        },
        {
            'start_from': '1',
            'end_at': '30'
        }
        ]
        self.assertEqual(ranges, self.parser.extract_ranges(custom_url_part))

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
