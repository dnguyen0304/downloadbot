# -*- coding: utf-8 -*-

from roomlistwatcher.common import event

from . import subscribers
from .. import policy


class Logging(object):

    def __init__(self, logger):

        """
        Parameters
        ----------
        logger : logging.Logger
        """

        self._logger = logger

    def create(self, event_name):

        """
        Parameters
        ----------
        event_name : str

        Returns
        -------
        common.event_driven.messaging.Broker
        """

        # Construct the attempt started subscriber.
        attempt_started_subscriber = subscribers.AttemptStarted(
            event_name=event_name)
        # Include logging.
        attempt_started_subscriber = subscribers.Logging(
            subscriber=attempt_started_subscriber,
            logger=self._logger)

        # Construct the attempt completed subscriber.
        attempt_completed_subscriber = subscribers.AttemptCompleted(
            event_name=event_name)
        # Include logging.
        attempt_completed_subscriber = subscribers.Logging(
            subscriber=attempt_completed_subscriber,
            logger=self._logger)

        # Construct the messaging broker.
        messaging_broker = event.messaging.Broker(
            observable_class=event.notifiables.Observable)
        # Initialize topics.
        messaging_broker.create_topic(name=policy.Topic.ATTEMPT_STARTED.name)
        messaging_broker.create_topic(name=policy.Topic.ATTEMPT_COMPLETED.name)
        # Initialize subscribers.
        messaging_broker.subscribe(
            subscriber=attempt_started_subscriber,
            topic_name=policy.Topic.ATTEMPT_STARTED.name)
        messaging_broker.subscribe(
            subscriber=attempt_completed_subscriber,
            topic_name=policy.Topic.ATTEMPT_COMPLETED.name)

        return messaging_broker

    def __repr__(self):
        repr_ = '{}(logger={})'
        return repr_.format(self.__class__.__name__, self._logger)
