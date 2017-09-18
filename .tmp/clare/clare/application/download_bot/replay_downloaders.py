# -*- coding: utf-8 -*-

import functools

from . import interfaces


class Retrying(interfaces.IReplayDownloader):

    def __init__(self, replay_downloader, policy):

        """
        Parameters
        ----------
        replay_downloader : clare.application.download_bot.interfaces.IReplayDownloader
        policy : clare.common.retry.policy.Policy
        """

        self._replay_downloader = replay_downloader
        self._policy = policy

    def run(self, url):
        download = functools.partial(self._replay_downloader.run, url=url)
        self._policy.execute(download)

    def dispose(self):
        self._replay_downloader.dispose()

    def __repr__(self):
        repr_ = '{}(replay_downloader={}, policy={})'
        return repr_.format(self.__class__.__name__,
                            self._replay_downloader,
                            self._policy)
