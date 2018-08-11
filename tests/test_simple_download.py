import unittest
from SimpleDownload import downloader


class TestSimpleDownload(unittest.TestCase):
    def setUp(self):
        self.dl = downloader.Downloader()

    def test_argument_received(self):
        self.assertIsNotNone(self.dl.argument)


if __name__ == '__main__':
    unittest.main()