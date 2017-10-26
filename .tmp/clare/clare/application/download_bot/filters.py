# -*- coding: utf-8 -*-


class ExceptGenerationSevenMetagameFilter(BaseFilter):

    def _should_filter(self, record):
        _, metagame_name, _ = record.value.split('-')
        if metagame_name.startswith('gen7'):
            return False
        else:
            return True

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class ExceptOverusedMetagameFilter(BaseFilter):

    def _should_filter(self, record):
        _, metagame_name, _ = record.value.split('-')
        if metagame_name.endswith('ou'):
            return False
        else:
            return True

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
