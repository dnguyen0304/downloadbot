# -*- coding: utf-8 -*-

from .. import exceptions


class HandleError(Exception):
    pass


class ReceiveTimeout(exceptions.Timeout):
    pass
