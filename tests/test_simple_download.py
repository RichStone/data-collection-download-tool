import unittest
from SimpleDownload import downloader


class TestSimpleDownload(unittest.TestCase):
    def setUp(self):
        pass

    def test_argument_received(self):
        arg = 'http://xkcd.com/+++1***2300+++'
        self.downloader = downloader.Downloader(arg)
        self.assertIsNotNone(self.downloader.user_input, '')


if __name__ == '__main__':
    unittest.main()