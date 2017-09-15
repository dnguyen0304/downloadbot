# -*- coding: utf-8 -*-

import selenium.common

from nose.tools import (assert_is_none,
                        assert_is_not_none,
                        assert_true,
                        raises)

from .. import exceptions
from .. import download_strategies


        pages_index = {'expired_room':
"""
<head>
  <title>Showdown!</title>
</head>
""",
                       'server_error':
"""
<head>
  <title>Showdown!</title>
</head>

<body>
  <div class="ps-overlay">
    <div>
      <form>
        <p>disconnected</p>
      </form>
    </div>
  </div>
</body>
""",
                       'battle_not_completed':
"""
<button class="" type="button"></button>
""",
                       'title_correct_content':
"""
<head>
  <title></title>
</head>
""",
                       'title_incorrect_content':
"""
<head>
  <title>Showdown!</title>
</head>""",
                       'server_error_correct_css_selector':
"""
<body>
  <div class="ps-overlay">
    <div>
      <form>
        <p></p>
      </form>
    </div>
  </div>
</body>
""",
                       'download_button_correct_class_name':
"""
<button class="replayDownloadButton" type="button"></button>
""",
                       'download_button_incorrect_class_name':
"""
<button class="" type="button"></button>
"""}


class NopDownloadStrategy(download_strategies.Base):

    def do_download(self):
        pass


class TestBase(MockServerUtilitiesMixin):

    def __init__(self):
        self.web_driver = None
        self.strategy = None

    def setup(self):
        self.web_driver = selenium.webdriver.Chrome()
        self.strategy = NopDownloadStrategy(web_driver=self.web_driver,
                                            timeout=None)

    @raises(exceptions.HttpError)
    def test_download_server_error_raises_http_error(self):
        url = self.construct_url(path='server_error')
        self.strategy.download(url=url)

    @raises(exceptions.DownloadFailed)
    def test_download_expired_room_raises_download_failed(self):
        url = self.construct_url(path='expired_room')
        self.strategy.download(url=url)

    def test_confirm_no_redirect_title_correct_content(self):
        self.set_web_driver_page(path='title_correct_content')
        self.strategy._confirm_no_redirect(timeout=None)

    @raises(selenium.common.exceptions.TimeoutException)
    def test_confirm_no_redirect_title_incorrect_content(self):
        self.set_web_driver_page(path='title_incorrect_content')
        self.strategy._confirm_no_redirect(timeout=None)

    def test_confirm_server_error_correct_css_selector_and_content(self):
        self.set_web_driver_page(path='server_error_correct_css_selector_and_content')
        encountered_server_error = self.strategy._confirm_server_error(
            timeout=None)
        assert_true(encountered_server_error)

    def teardown(self):
        self.strategy.dispose()


class TestReplay(MockServerUtilitiesMixin):

    def __init__(self):
        self.web_driver = None
        self.strategy = None

    def setup(self):
        self.web_driver = selenium.webdriver.Chrome()
        self.strategy = download_strategies.Replay(web_driver=self.web_driver,
                                                   timeout=None)

    @raises(exceptions.BattleNotCompleted)
    def test_do_download_battle_not_completed_raises_battle_not_completed(self):
        self.set_web_driver_page(path='battle_not_completed')
        self.strategy.do_download()

    def teardown(self):
        self.strategy.dispose()


class TestFindDownloadButton(MockServerUtilitiesMixin):

    def __init__(self):
        self.web_driver = None
        self.timeout = None

    def setup(self):
        self.web_driver = selenium.webdriver.Chrome()

    def test_correct_class_name(self):
        self.set_web_driver_page(path='download_button_correct_class_name')
        download_button = download_strategies.find_download_button(
            web_driver=self.web_driver,
            timeout=self.timeout)
        assert_is_not_none(download_button)

    def test_incorrect_class_name(self):
        self.set_web_driver_page(path='download_button_incorrect_class_name')
        download_button = download_strategies.find_download_button(
            web_driver=self.web_driver,
            timeout=self.timeout)
        assert_is_none(download_button)

    def teardown(self):
        self.web_driver.quit()
