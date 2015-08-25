import uuid


class Beast(object):
    def __init__(self, symbol):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.inner = self
        self.symbol = symbol
        self.id = ''
        self.type = ''
        self.song = ''

    @property
    def all(self):
        return None

    @all.setter
    def all(self, value):
        self.left = value
        self.right = value
        self.up = value
        self.down = value

    @property
    def from_below(self):
        return self.down.up

    @property
    def from_above(self):
        return self.up.down

    @property
    def from_left(self):
        return self.left.right

    def clone(self, id_append=None):
        b = Beast(self.symbol)
        b.__dict__ = dict((k, v) if v != self else (k, b) for (k, v) in self.__dict__.items())
        b.id += id_append or uuid.uuid4().hex
        return b
