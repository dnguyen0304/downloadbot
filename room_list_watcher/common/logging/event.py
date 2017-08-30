# -*- coding: utf-8 -*-

import collections
import datetime
import json
import uuid

import clare.common
from . import interfaces


class Event(interfaces.IEvent, interfaces.IJsonSerializable):

    def __init__(self, topic, arguments):

        """
        Parameters
        ----------
        topic : Topic
        arguments : collections.Mapping
        """

        self.correlation_id = str(uuid.uuid4())

        self.topic = topic
        self.arguments = arguments

        time_zone = clare.common.utilities.TimeZone.from_name('UTC')
        self.created_at = datetime.datetime.utcnow().replace(tzinfo=time_zone)

    @property
    def INTERFACE_VERSION(self):
        return '1.0.0'

    def to_json(self):
        data = collections.OrderedDict()
        data['interface_version'] = self.INTERFACE_VERSION
        data['correlation_id'] = self.correlation_id
        data['topic_name'] = self.topic.name
        data['arguments'] = self.arguments
        data['created_at'] = self.created_at.isoformat()

        return json.dumps(data)

    def __repr__(self):
        repr_ = '{}(topic={}, arguments={})'
        return repr_.format(self.__class__.__name__,
                            self.topic,
                            self.arguments)
