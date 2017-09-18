# -*- coding: utf-8 -*-

import functools

from . import exceptions
from . import interfaces
from clare import common


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


class Validating(interfaces.IReplayDownloader):

    def __init__(self, replay_downloader, validator):

        """
        Parameters
        ----------
        replay_downloader : clare.application.download_bot.interfaces.IReplayDownloader
        validator : clare.common.automation.validators.PokemonShowdown
        """

        self._replay_downloader = replay_downloader
        self._validator = validator

    def run(self, url):
        self._replay_downloader._initialize(url=url)
        self._do_run()

    def _do_run(self):

        """
        Raises
        ------
        clare.common.automation.exceptions.ConnectionLost
            If the connection with the target server was lost.
        clare.application.download_bot.exceptions.RoomExpired
            If the room has expired.
        """

        try:
            self._validator.check_room_was_entered()
        except common.automation.exceptions.ValidationFailed:
            try:
                self._validator.check_connection_exists()
            except common.automation.exceptions.ConnectionLost:
                raise
            else:
                message = 'The room has expired.'
                raise exceptions.RoomExpired(message)
        self._replay_downloader._do_run()

    def dispose(self):
        self._replay_downloader.dispose()

    def __repr__(self):
        repr_ = '{}(replay_downloader={}, validator={})'
        return repr_.format(self.__class__.__name__,
                            self._replay_downloader,
                            self._validator)
