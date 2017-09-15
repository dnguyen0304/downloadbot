# -*- coding: utf-8 -*-

from .. import exceptions


class DeleteFailed(Exception):
    pass


class FetchTimeout(exceptions.Timeout):
    pass


class ReceiveTimeout(exceptions.Timeout):
    pass
