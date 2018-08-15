import sys
from urllib.parse import urlsplit, urlunsplit
import urllib.request
from urllib.error import URLError
import re

import validators

# examples:
# python3 simple_download.py http://xkcd.com/+++1***2300+++
# python3 simple_download.py https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed+++0001***0928+++.xml.gz


class Parser:
    def __init__(self):
        self.concat_delimiter = '++'
        self.range_delimiter = '**'
        # regex needs delimiters to be escaped
        self.concat_delimiter_escaped = '\+\+'
        self.range_delimiter_escaped = '\*\*'

    def build_clean_url(self, user_input):
        if user_input == '' or user_input is None or not isinstance(user_input, str):
            raise ValueError('Error: you have to pass a valid String to the parser.')
        base_url = self.extract_base_url(user_input)
        self.validate_base_url_connection(base_url)
        custom_url_part = self.extract_custom_url_part(user_input)
        ranges = self.extract_ranges(custom_url_part)

    def validate_user_input(self, user_input):
        def validate_concat_sequences():
            pass

    def extract_base_url(self, user_input):
        split_url = urlsplit(user_input)
        base_url = urlunsplit((split_url.scheme, split_url.netloc, '', '', ''))
        if validators.url(base_url) is validators.utils.ValidationFailure:
            raise ValueError('Base URL is malformed, please keep to the following format: '
                             '"http://www.example.com/" ')
        return base_url

    def extract_custom_url_part(self, user_input):
        split_url = urlsplit(user_input)
        custom_part = urlunsplit(('', '', split_url.path, '', ''))
        return custom_part

    def extract_ranges(self, custom_url_part):
        ranges = []
        extracted_ranges = re.findall(r'(?<=' + self.concat_delimiter_escaped + ').+?(?=' + self.concat_delimiter_escaped + ')',
                                      custom_url_part)
        if extracted_ranges is not []:
            for extracted_range in extracted_ranges:
                if self.range_delimiter in extracted_range:
                    range_obj = dict()
                    split_range = extracted_range.split(self.range_delimiter)
                    range_obj['start_from'] = split_range[0]
                    range_obj['end_at'] = split_range[1]
                    ranges.append(range_obj)
            return ranges

    def validate_base_url_connection(self, base_url):
        try:
            return urllib.request.urlopen(base_url).getcode()
        except URLError:
            raise URLError('Terminate program because connection could not be established with the given base URL '
                           + base_url)


if __name__ == 'main':
    try:
        passed_argument = sys.argv[1]
    except IndexError:
        print('You did not pass an URL path to the script execution.')
    except:
        # TODO: when all errors are known, handle properly
        # 1. IndexError, when no argument passed
        print('Unexpected Error: ' + sys.exc_info()[0])

