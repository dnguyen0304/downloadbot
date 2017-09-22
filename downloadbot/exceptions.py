# -*- coding: utf-8 -*-

from .common import automation


class BattleNotCompleted(automation.exceptions.AutomationFailed):
    pass


class RoomExpired(automation.exceptions.AutomationFailed):
    pass
