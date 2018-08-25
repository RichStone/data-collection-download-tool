class Downloader:
    def __init__(self, range_wildcard):
        self.range_wildcard = range_wildcard

    def download(self, ranges):
        start_from_indices = self.get_start_indices_from_ranges(ranges)
        end_at_indices = self.get_end_at_indices_from_ranges(ranges)
        current_ranges = start_from_indices

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
            split_url.insert(insert_index, current_range[loop_index])
            insert_index += 2
        download_url = ''.join(split_url)
        return download_url
