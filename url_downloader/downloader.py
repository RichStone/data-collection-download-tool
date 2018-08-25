import os
import urllib.request
from urllib.parse import urlsplit


class Downloader:
    def __init__(self, range_wildcard):
        self.range_wildcard = range_wildcard
        downloader_directory = os.path.dirname(__file__)
        self.download_path = os.path.join(downloader_directory, '../downloads/')
        # place longer suffixes at the beginning, order matters!
        self.important_suffixes = ('.tar.gz', '.xml.gz', '.zip', '.tar', '.html')

    def download(self, start_url, ranges):
        start_from_indices = self.get_start_indices_from_ranges(ranges)
        end_at_indices = self.get_end_at_indices_from_ranges(ranges)
        current_ranges = start_from_indices
        zfill_amount = self.get_zfill_amount(ranges)
        # current_ranges[0] yields the currently needed index for the download
        print('########## Starting Download ##########')
        while current_ranges[0] <= end_at_indices[0]:
            url = self.build_download_url(start_url, current_ranges, zfill_amount)
            file_name = self.get_target_file_name(url, current_ranges[0])
            target_path = self.download_path + file_name
            print('Downloading from ' + url + ' to ' + target_path)
            urllib.request.urlretrieve(url, target_path)
            current_ranges[0] += 1
        print('########## Download Finished ##########')

    @staticmethod
    def get_start_indices_from_ranges(ranges):
        start_from = []
        for index, r in enumerate(ranges):
            start_from.append(int(r['start_from']))
        return start_from

    @staticmethod
    def get_end_at_indices_from_ranges(ranges):
        end_at = []
        for index, r in enumerate(ranges):
            end_at.append(int(r['end_at']))
        return end_at

    def get_target_file_name(self, url, index):
        split_url = urlsplit(url)
        # get the domain/top level domain part of url
        file_name = split_url.netloc
        # get rid of '/' for *nix filesystem compatibility
        file_name = file_name.replace('/', '-')
        # join with currently downloaded index
        file_name = str(index) + '-' + file_name

        if url.endswith(self.important_suffixes):
            important_suffix = self.get_important_suffix(url)
            file_name += important_suffix
        return file_name

    def get_important_suffix(self, url):
        for suffix in self.important_suffixes:
            if suffix in url:
                return suffix

    @staticmethod
    def get_zfill_amount(ranges):
        """
        If the range string starts with a '0', all chars must be counted in order to get a zfill value.

        :param ranges: dict - contains the different ranges
        :return: int - number of zeros to be filled in the target string
        """
        download_range = ranges[0]['start_from']
        zfill_amount = 0
        if download_range.startswith('0'):
            for number in download_range:
                zfill_amount += 1
        return zfill_amount

    def build_download_url(self, start_url, current_range, zfill_amount):
        """
        Replaces the wildcard delimiter with the current range number to be downloaded.

        :param leading_zeros_in_range: int - amount of zeros to be prefixed to range
        :param start_url: string - custom url with wildcard to be dissected
        :param current_range: dict of ints - ranges to download
        :return: string - URL ready for download
        """
        split_url = start_url.split(self.range_wildcard)
        insert_index = 1
        for loop_index, r in enumerate(current_range):
            split_url.insert(insert_index, str(current_range[loop_index]).zfill(zfill_amount))
            insert_index += 2
        download_url = ''.join(split_url)
        return download_url
