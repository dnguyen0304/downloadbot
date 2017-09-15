# -*- coding: utf-8 -*-

import Queue
import os
import threading
import uuid

from . import applications
from . import download_bot
from . import room_list_watcher


class Application(object):

    def __init__(self, infrastructure, properties):

        """
        Parameters
        ----------
        infrastructure : clare.infrastructure.infrastructures.ApplicationInfrastructure
        properties : collections.Mapping
        """

        self._infrastructure = infrastructure
        self._properties = properties

    def create(self):

        """
        Returns
        -------
        clare.application.applications.Application
        """

        queue = Queue.Queue()

        # Construct the room list watcher.
        room_list_watcher_factory = room_list_watcher.factories.Producer(
            infrastructure=self._infrastructure.room_list_watcher,
            properties=self._properties['room_list_watcher'])
        room_list_watcher_ = room_list_watcher_factory.create()

        # Include threading.
        kwargs = {
            'interval': self._properties['room_list_watcher']['interval']
        }
        room_list_watcher_ = threading.Thread(name='room_list_watcher',
                                              target=room_list_watcher_.produce,
                                              kwargs=kwargs)
        room_list_watcher_.daemon = True

        # Construct the download bot.
        download_bot_factory = download_bot.factories.Factory(
            queue=queue,
            properties=self._properties['download_bot'])
        directory_path = os.path.join(
            self._properties['download_bot']['factory']['root_directory_path'],
            str(uuid.uuid4()))
        download_bot_ = download_bot_factory.create(
            download_directory_path=directory_path)

        # Include threading.
        kwargs = {
            'interval': self._properties['download_bot']['interval'],
            'timeout': self._properties['download_bot']['timeout']
        }
        download_bot_ = threading.Thread(name='download_bot',
                                         target=download_bot_.consume,
                                         kwargs=kwargs)
        download_bot_.daemon = True

        # Construct the application.
        application = applications.Application(
            room_list_watcher=room_list_watcher_,
            download_bot=download_bot_)

        return application

    def __repr__(self):
        repr_ = '{}(infrastructure={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._infrastructure,
                            self._properties)
