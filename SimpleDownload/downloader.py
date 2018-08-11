import sys
from urllib.parse import urlsplit, urlunsplit

import validators

# examples:
# python3 simple_download.py http://xkcd.com/+++1***2300+++
# python3 simple_download.py https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/+++0001***0928+++


class Downloader:
    def __init__(self, arg):
        self.user_input = arg
        self.CONCAT_DELIMITER = '+++'
        self.RANGE_DELIMITER = '***'
        self.BASE_URL = self.extract_base_url()

    def validate_user_input(self):

        def validate_base_url():
            if validators.url(self.BASE_URL) is validators.utils.ValidationFailure:
                raise ValueError('Base URL is malformed, please keep to the following format: "http://www.example.com/" ')

        def validate_concat_sequences():
            pass

    def extract_base_url(self):
        split_url = urlsplit(self.user_input)
        base_url = urlunsplit((split_url.scheme, split_url.netloc, "", "", ""))
        return base_url


if __name__ == 'main':
    try:
        passed_argument = sys.argv[1]
    except IndexError:
        print('You did not pass an URL path to the script execution.')
    except:
        # TODO: when all errors are known, handle properly
        # 1. IndexError, when no argument passed
        print('Unexpected Error: ' + sys.exc_info()[0])

