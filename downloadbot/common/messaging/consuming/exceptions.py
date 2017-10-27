# -*- coding: utf-8 -*-

from .. import exceptions


class DeleteError(Exception):
    pass


class ReceiveTimeout(exceptions.Timeout):
    pass
