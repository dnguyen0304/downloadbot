# -*- coding: utf-8 -*-

from .. import exceptions


class EmitTimeout(exceptions.Timeout):
    pass


class SendTimeout(exceptions.Timeout):
    pass
