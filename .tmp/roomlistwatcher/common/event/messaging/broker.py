# -*- coding: utf-8 -*-


class Broker(object):

    def __init__(self, observable_class):

        """
        Parameters
        ----------
        observable_class : clare.common.event_driven.Observable
        """

        self._observable_class = observable_class
        self._topics_index = dict()

    def create_topic(self, name):

        """
        A new topic is created only if one by the same name does not
        already exist.

        Parameters
        ----------
        name : str
        """

        if name not in self._topics_index:
            self._topics_index[name] = self._observable_class()

    def list_topics(self):

        """
        Returns
        -------
        collections.Sequence
        """

        return self._topics_index.keys()

    def publish(self, event, topic_name):

        """
        Parameters
        ----------
        event : str
        topic_name : str
        """

        observable = self._topics_index[topic_name]
        observable.notify(event=event)

    def subscribe(self, subscriber, topic_name):

        """
        Parameters
        ----------
        subscriber : clare.common.event_driven.interfaces.INotifyable
        topic_name : str
        """

        observable = self._topics_index[topic_name]
        observable.register(observer=subscriber)

    def __repr__(self):
        repr_ = '{}(observable_class={})'
        return repr_.format(self.__class__.__name__, self._observable_class)
