""" スキルデータを扱いやすくするためのクラス """

class SkillData():
    ID = 'id'
    BP = 'base_power'
    CP = 'coin_power'
    CC = 'coin_count'
    NM = 'name'
    PR = 'prisoner'

    def __init__(self,
                id         = None,
                base_power = 0,
                coin_power = 0,
                coin_count = 0,
                name       = "noname",
                prisoner   = None
            ) -> None:

        self._data = {
            self.ID: id,
            self.BP: base_power,
            self.CP: coin_power,
            self.CC: coin_count,
            self.NM: name,
            self.PR: prisoner
        }

    def get(self, key):
        return self._data[key]

    def set(self, key, value):
        self._data[key] = value