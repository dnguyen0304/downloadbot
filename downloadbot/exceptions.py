# -*- coding: utf-8 -*-

from . import automation


class BattleNotCompleted(automation.exceptions.AutomationFailed):
    pass


class RoomExpired(automation.exceptions.AutomationFailed):
    pass
