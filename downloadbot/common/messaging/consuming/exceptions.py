# -*- coding: utf-8 -*-

from .. import exceptions


class DeleteError(Exception):
    pass


class HandleError(Exception):
    pass


class ReceiveTimeout(exceptions.Timeout):
    pass
