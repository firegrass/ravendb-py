import bunch


class buncher(object):

    def __init__(self, value):
        self._value = value

    def bunch(self):
        bunched = bunch.Bunch()
        bunched.update(self._value)
        return bunched
