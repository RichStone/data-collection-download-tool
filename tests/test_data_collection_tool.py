import unittest
from url_downloader import url_argument_parser, downloader
from urllib.error import URLError, HTTPError

import os

from tests import utils


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

    def test_extract_custom_part_with_queries_in_url_path(self):
        user_input = 'http://www.harkavagrant.com/index.php?id=++1**4++'
        self.assertEqual('/index.php?id=++1**4++', self.parser.extract_custom_url_part(user_input))

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
        self.dl_handler = downloader.Downloader(url_argument_parser.Parser().final_url_range_wildcard)

    def tearDown(self):
        # remove downloaded files
        downloaded_files = utils.get_all_file_names_from_directory(self.dl_handler.download_path)
        if downloaded_files:
            for file in downloaded_files:
                os.unlink(os.path.join(self.dl_handler.download_path, file))

    def test_build_download_url(self):
        start_url = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed19n###.xml.gz'
        download_range = ['0001']
        clean_download_url = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed19n0001.xml.gz'
        parsed_url = self.dl_handler.build_download_url(start_url, download_range, 4)
        self.assertEqual(clean_download_url, parsed_url)

    def test_build_download_url_multiple_wildcards(self):
        start_url = 'http://datagoodie.com/month/###/day/###'
        download_range = ['1', '1']
        clean_download_url = 'http://datagoodie.com/month/1/day/1'
        parsed_url = self.dl_handler.build_download_url(start_url, download_range, 0)
        self.assertEqual(clean_download_url, parsed_url)

    def test_get_starts_from_ranges_with_single_range(self):
        ranges = [
            {'start_from': '0001', 'end_at': '0928'},
        ]
        extracted_starts = self.dl_handler.get_start_indices_from_ranges(ranges)
        target_starts = [1]
        self.assertEqual(target_starts, extracted_starts)

    def test_get_starts_from_ranges_with_multiple_ranges(self):
        ranges = [
            {'start_from': '1', 'end_at': '12'},
            {'start_from': '15', 'end_at': '30'}
        ]
        extracted_starts = self.dl_handler.get_start_indices_from_ranges(ranges)
        target_starts = [1, 15]
        self.assertEqual(target_starts, extracted_starts)

    def test_get_end_at_ranges_with_single_range(self):
        ranges = [
            {'start_from': '0001', 'end_at': '0928'},
        ]
        extracted_starts = self.dl_handler.get_end_at_indices_from_ranges(ranges)
        target_starts = [928]
        self.assertEqual(target_starts, extracted_starts)

    def test_get_end_at_ranges_with_multiple_ranges(self):
        ranges = [
            {'start_from': '1', 'end_at': '12'},
            {'start_from': '15', 'end_at': '30'}
        ]
        extracted_starts = self.dl_handler.get_end_at_indices_from_ranges(ranges)
        target_starts = [12, 30]
        self.assertEqual(target_starts, extracted_starts)

    # @unittest.skip('skip during test phases, because of long download waiting times')
    def test_download_several_html_pages_single_range(self):
        start_url = 'https://xkcd.com/###'
        ranges = [
            {'start_from': '1', 'end_at': '3'},
        ]
        self.dl_handler.download(start_url, ranges)
        downloaded_files = utils.get_all_file_names_from_directory(self.dl_handler.download_path)
        # convert to set because order should not matter for equality at assert
        downloaded_files = set(downloaded_files)
        expected_files = {'1-xkcd.com.html', '2-xkcd.com.html', '3-xkcd.com.html'}
        self.assertEqual(expected_files, downloaded_files)

    # @unittest.skip('skip during test phases, because of long download waiting times')
    def test_download_several_files_with_leading_zeros_in_range(self):
        start_url = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed19n###.xml.gz'
        ranges = [
            {'start_from': '0001', 'end_at': '0002'},
        ]
        self.dl_handler.download(start_url, ranges)
        downloaded_files = utils.get_all_file_names_from_directory(self.dl_handler.download_path)
        # convert to set because order should not matter for equality at assert
        downloaded_files = set(downloaded_files)
        expected_files = {
            '1-ftp.ncbi.nlm.nih.gov.xml.gz',
            '2-ftp.ncbi.nlm.nih.gov.xml.gz'
        }
        self.assertEqual(expected_files, downloaded_files)

    def test_get_target_file_name(self):
        url = 'https://xkcd.com/1'
        file_name = self.dl_handler.get_target_file_name(url, 1)
        self.assertEqual('1-xkcd.com.html', file_name)

    def test_get_target_file_name_with_important_suffix(self):
        url = 'http://datagoodie.com/important-goodie.tar.gz'
        file_name = self.dl_handler.get_target_file_name(url, 1)
        self.assertEqual('1-datagoodie.com.tar.gz', file_name)

    def test_ranges_delimiters_should_be_same_between_parser_and_downloader(self):
        parser = url_argument_parser.Parser()
        parser_wildcard = parser.final_url_range_wildcard
        downloader_wildcard = self.dl_handler.range_wildcard
        self.assertEqual(downloader_wildcard, parser_wildcard)

    def test_downloader_should_pass_gracefully_when_url_not_downloadable(self):
        start_url = 'https://xkcd.com/###'
        ranges = [
            {'start_from': '0', 'end_at': '2'},
        ]
        try:
            self.dl_handler.download(start_url, ranges)
            downloaded_files = utils.get_all_file_names_from_directory(self.dl_handler.download_path)
            # convert to set because order should not matter for equality at assert
            downloaded_files = set(downloaded_files)
            expected_files = {'1-xkcd.com.html', '2-xkcd.com.html'}
            self.assertEqual(expected_files, downloaded_files)
        except HTTPError:
            self.fail("Download raised HTTPError unexpectedly!")


if __name__ == '__main__':
    unittest.main()
