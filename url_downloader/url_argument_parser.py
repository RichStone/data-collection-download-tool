from urllib.parse import urlsplit, urlunsplit
import urllib.request
from urllib.error import URLError
import re


class Parser:
    def __init__(self):
        self.concat_delimiter = '++'
        self.range_delimiter = '**'
        # regex needs delimiters to be escaped
        self.concat_delimiter_escaped = '\+\+'
        self.range_delimiter_escaped = '\*\*'
        self.final_url_range_wildcard = '###'

        self.ranges = dict()
        self.clean_url = ''

    def get_ranges_and_clean_start_url(self, user_input):
        if user_input == '' or user_input is None or not isinstance(user_input, str):
            raise ValueError('Error: you have to pass a valid String to the parser.')
        base_url = self.extract_base_url(user_input)
        self.validate_base_url_connection(base_url)

        custom_url_part = self.extract_custom_url_part(user_input)
        self.ranges = self.extract_ranges(custom_url_part)
        self.clean_url = self.build_final_url(self.ranges, user_input)
        return self.clean_url, self.ranges

    @staticmethod
    def extract_base_url(user_input):
        try:
            split_url = urlsplit(user_input)
        except ValueError:
            raise ValueError(
                'Splitting URL failed. Check you did something wrong here: '
                'https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit')
        base_url = urlunsplit((split_url.scheme, split_url.netloc, '', '', ''))
        return base_url

    @staticmethod
    def extract_custom_url_part(user_input):
        split_url = urlsplit(user_input)
        custom_part = urlunsplit(('', '', split_url.path, split_url.query, ''))
        return custom_part

    def extract_ranges(self, custom_url_part):
        ranges = []
        extracted_ranges = re.findall(
            r'(?<=' + self.concat_delimiter_escaped + ').+?(?=' + self.concat_delimiter_escaped + ')', custom_url_part)
        if not extracted_ranges:
            raise ValueError('You did not provide the accepted syntax for the URL path.')
        else:
            for extracted_range in extracted_ranges:
                if self.range_delimiter in extracted_range:
                    range_obj = dict()
                    split_range = extracted_range.split(self.range_delimiter)
                    range_obj['start_from'] = split_range[0]
                    range_obj['end_at'] = split_range[1]
                    ranges.append(range_obj)
            return ranges

    @staticmethod
    def validate_base_url_connection(base_url):
        try:
            return urllib.request.urlopen(base_url).getcode()
        except URLError:
            raise URLError('Terminate program because connection could not be established with the given base URL '
                           + base_url)
        except ValueError:
            raise ValueError('Base URL "' + base_url + '" is malformed, please keep to the following format: '
                             '"http://www.example.com/path/to/download++100**5000++"')

    def build_final_url(self, ranges, user_input):
        """
        Splits the custom url at the concat_delimiter. From this split always the range integer remains at every second
        position of the split list. In the loop this unnecessary remainder is replaced by a wildcard.

        :param ranges: dict of int - ranges to download
        :param user_input: string - custom url to be dissected
        :return: string - URL with wildcard values for ranges that can be finally used in downloader.py
        """
        split_url = user_input.split(self.concat_delimiter)
        split_index = 1
        for r in ranges:
            split_url[split_index] = self.final_url_range_wildcard
            split_index += 2
        clean_url = ''.join(s for s in split_url)
        return clean_url
