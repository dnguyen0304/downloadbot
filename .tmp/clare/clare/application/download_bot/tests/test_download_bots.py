# -*- coding: utf-8 -*-

from nose.tools import assert_equal

from .. import download_bots


class TestUrlRunPathDownloadBot(object):

    def __init__(self):
        self.root_url = None
        self.path = None
        self.url = None

    def setup(self):
        self.root_url = 'http://www.foo.com'
        self.path = 'battle-bar-0'
        self.url = self.root_url + '/' + self.path

    def test_root_url_with_trailing_slash_and_path_with_leading_slash(self):
        self.root_url = self.root_url + '/'
        self.path = '/' + self.path
        self.do()

    def test_root_url_with_trailing_slash_and_path_without_leading_slash(self):
        self.root_url = self.root_url + '/'
        self.path = self.path
        self.do()

    def test_root_url_without_trailing_slash_and_path_with_leading_slash(self):
        self.root_url = self.root_url
        self.path = '/' + self.path
        self.do()

    def test_root_url_without_trailing_slash_and_path_without_leading_slash(self):
        self.root_url = self.root_url
        self.path = self.path
        self.do()

    def do(self):
        download_bot = download_bots.DownloadBot(replay_downloader=None,
                                                 download_validator=None)
        download_bot = download_bots.UrlPathDownloadBot(
            download_bot=download_bot,
            root_url=self.root_url)
        url = download_bot._url_join(root_url=self.root_url, path=self.path)
        assert_equal(url, self.url)
