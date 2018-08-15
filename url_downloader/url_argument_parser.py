from urllib.parse import urlsplit, urlunsplit
import urllib.request
from urllib.error import URLError
import re

import validators


class Parser:
    def __init__(self):
        self.concat_delimiter = '++'
        self.range_delimiter = '**'
        # regex needs delimiters to be escaped
        self.concat_delimiter_escaped = '\+\+'
        self.range_delimiter_escaped = '\*\*'

        self.ranges = dict()
        self.clean_url = ''

    def get_ranges_and_clean_start_url(self, user_input):
        if user_input == '' or user_input is None or not isinstance(user_input, str):
            raise ValueError('Error: you have to pass a valid String to the parser.')
        base_url = self.extract_base_url(user_input)
        self.validate_base_url_connection(base_url)

        custom_url_part = self.extract_custom_url_part(user_input)
        self.ranges = self.extract_ranges(custom_url_part)
        self.clean_url = self.build_clean_url(self.ranges, user_input)

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
        if not extracted_ranges:
            raise ValueError('You did not provide the accepted syntax for the URL path.')
        else:
            for extracted_range in extracted_ranges:
                if self.range_delimiter in extracted_range:
                    range_obj = dict()
                    split_range = extracted_range.split(self.range_delimiter)
                    # TODO: check on split every range value to be numeric
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

    def build_clean_url(self, ranges, user_input):
        split_url = user_input.split(self.concat_delimiter)
        # TODO: comment this crazy stuff
        split_index = 1
        for loop_index, r in enumerate(ranges):
            split_url[split_index] = ranges[loop_index]['start_from']
            split_index += 2
        clean_url = ''.join(s for s in split_url)
        return clean_url
