# -*- coding: utf-8 -*-

from .. import exceptions


class EmitFailed(Exception):
    pass


class SendTimeout(exceptions.Timeout):
    pass
