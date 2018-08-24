import unittest
from url_downloader import url_argument_parser, downloader
from urllib.error import URLError

import os


class TestUrlParser(unittest.TestCase):
    def setUp(self):
        self.parser = url_argument_parser.Parser()

    def test_argument_received(self):
        user_input = ''
        with self.assertRaises(ValueError):
            self.parser.get_ranges_and_clean_start_url(user_input)

        user_input = None
        with self.assertRaises(ValueError):
            self.parser.get_ranges_and_clean_start_url(user_input)

        user_input = 13245
        with self.assertRaises(ValueError):
            self.parser.get_ranges_and_clean_start_url(user_input)

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

        user_input = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed++0001**0928++.xml.gz'
        self.assertEqual('/pubmed/baseline/pubmed++0001**0928++.xml.gz', self.parser.extract_custom_url_part(user_input))

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

    def test_except_on_invalid_concat_input(self):
        with self.assertRaises(ValueError):
            # 'incorrect concat delimiter'
            user_input = 'https://xkcd.com/sdfgsdfg'
            self.parser = self.parser.extract_ranges(user_input)

    def test_build_start_url(self):
        parser_url = self.parser.get_ranges_and_clean_start_url('https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed18n++0001**0928++.xml.gz')
        start_url = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed18n###.xml.gz'
        self.assertEqual(start_url, self.parser.clean_url)

        parser_url = self.parser.get_ranges_and_clean_start_url('http://datagoodie.com/month/++1**12++/day/++1**30++')
        start_url = 'http://datagoodie.com/month/###/day/###'
        self.assertEqual(start_url, self.parser.clean_url)


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.dl_handler = downloader.Downloader(url_argument_parser.Parser().final_url_wildcard)

    def tearDown(self):
        # TODO: delete everything from downloads if exists
        pass

    def test_build_download_start_url(self):
        start_url = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed18n###.xml.gz'
        download_range = [
            {'start_from': '0001', 'end_at': '0928'},
        ]
        clean_download_url = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed18n0001.xml.gz'
        parsed_url = self.dl_handler.build_download_url(start_url, download_range)
        self.assertEqual(clean_download_url, parsed_url)

        start_url = 'http://datagoodie.com/month/###/day/###'
        download_range = [
            {'start_from': '1', 'end_at': '12'},
            {'start_from': '1', 'end_at': '30'}
        ]
        clean_download_url = 'http://datagoodie.com/month/1/day/1'
        parsed_url = self.dl_handler.build_download_url(start_url, download_range)
        self.assertEqual(clean_download_url, parsed_url)

    @unittest.skip('later')
    def test_ranges_delimiters_should_be_same_between_parser_and_downloader(self):
        pass

    @unittest.skip('later')
    def test_should_raise_exception_gracefully_when_url_not_downloadable(self):
        pass

    @unittest.skip('later')
    def test_download_first_file_with_clean_simple_start_url(self):
        url = 'https://xkcd.com/1'
        download_target_file_name = 'xkcd1.html'
        # get first file in
        download_actual_file_name = os.listdir(os.getcwd() + '/downloads')[0]
        self.assertEqual(download_target_file_name, download_actual_file_name)


if __name__ == '__main__':
    unittest.main()
