# -*- coding: utf-8 -*-


class AutomationFailed(Exception):
    pass


class ConnectionLost(AutomationFailed):
    pass


class WebDriverError(AutomationFailed):
    pass


class ValidationFailed(AutomationFailed):
    pass
