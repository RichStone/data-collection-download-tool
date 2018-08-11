import sys
# python3 simple_download.py http://xkcd.com/+++1***2300+++

# python3 simple_download.py https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/+++0001***0928+++


class Downloader:
    def __init__(self, arg):
        self.user_input = arg


if __name__ == 'main':
    try:
        passed_argument = sys.argv[1]
    except IndexError:
        print('You did not pass an URL path to the script execution.')
    except:
        # TODO: when all errors are known, handle properly
        # 1. IndexError, when no argument passed
        print('Unexpected Error: ' + sys.exc_info()[0])


