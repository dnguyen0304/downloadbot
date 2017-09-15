# -*- coding: utf-8 -*-

import time


class Application(object):

    def __init__(self, room_list_watcher, download_bot):
        self._room_list_watcher = room_list_watcher
        self._download_bot = download_bot

    def start(self):
        ONE_DAY_IN_SECONDS = 60 * 60 * 24

        self._room_list_watcher.start()
        self._download_bot.start()

        # Block the main thread indefinitely.
        try:
            while True:
                time.sleep(ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            pass

    def __repr__(self):
        repr_ = '{}(room_list_watcher={}, download_bot={})'
        return repr_.format(self.__class__.__name__,
                            self._room_list_watcher,
                            self._download_bot)
