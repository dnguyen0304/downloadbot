# -*- coding: utf-8 -*-


class AutomationFailed(Exception):
    pass


class ConnectionLost(AutomationFailed):
    pass


class ValidationFailed(AutomationFailed):
    pass


# TODO (duy): This could be evaluated for being migrated to a separate library.
class NoResultFound(Exception):
    pass
