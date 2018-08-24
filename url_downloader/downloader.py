class Downloader:
    def __init__(self, ranges_delimiter):
        self.ranges_delimiter = ranges_delimiter

    def build_download_url(self, start_url, ranges):
        """
        Replaces the wildcard delimiter with the current range number to be downloaded.

        :param start_url: string - custom url with wildcard to be dissected
        :param ranges: dict of ints - ranges to download
        :return: string - URL ready for download
        """
        split_url = start_url.split(self.ranges_delimiter)
        insert_index = 1
        for loop_index, r in enumerate(ranges):
            split_url.insert(insert_index, ranges[loop_index]['start_from'])
            insert_index += 2
        download_url = ''.join(split_url)
        return download_url
