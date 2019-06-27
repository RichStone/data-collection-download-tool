import sys
from url_downloader import url_argument_parser, downloader


def main(user_input):
    parser = url_argument_parser.Parser()
    start_url, ranges = parser.get_ranges_and_clean_start_url(user_input)

    download_handler = downloader.Downloader(range_wildcard=parser.final_url_range_wildcard)
    download_handler.download(start_url, ranges)


if __name__ == '__main__':
    main(sys.argv[1])
