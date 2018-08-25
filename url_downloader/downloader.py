import os
import urllib.request
from urllib.parse import urlsplit


class Downloader:
    def __init__(self, range_wildcard):
        self.range_wildcard = range_wildcard
        downloader_directory = os.path.dirname(__file__)
        self.download_path = os.path.join(downloader_directory, '../downloads/')

    def download(self, start_url, ranges):
        start_from_indices = self.get_start_indices_from_ranges(ranges)
        end_at_indices = self.get_end_at_indices_from_ranges(ranges)
        current_ranges = start_from_indices
        # current_ranges[0] yields the currently needed index for the download
        print('########## Starting Download ##########')
        while current_ranges[0] <= end_at_indices[0]:
            url = self.build_download_url(start_url, current_ranges)
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

    @staticmethod
    def get_target_file_name(url, index):
        split_url = urlsplit(url)
        file_name = str(index) + '-' + split_url.netloc
        return file_name

    def build_download_url(self, start_url, current_range):
        """
        Replaces the wildcard delimiter with the current range number to be downloaded.

        :param start_url: string - custom url with wildcard to be dissected
        :param current_range: dict of ints - ranges to download
        :return: string - URL ready for download
        """
        split_url = start_url.split(self.range_wildcard)
        insert_index = 1
        for loop_index, r in enumerate(current_range):
            split_url.insert(insert_index, str(current_range[loop_index]))
            insert_index += 2
        download_url = ''.join(split_url)
        return download_url
