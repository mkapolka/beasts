import uuid


class Beast(object):
    def __init__(self, symbol):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.inner = self
        self.orig_left = self
        self.orig_right = self
        self.orig_up = self
        self.orig_down = self
        self.orig_inner = self
        self.symbol = symbol
        self.id = uuid.uuid4().hex
        self.tick_speed = 1
        self.type = ''
        self.song = ''
        self.stitches = {}
        self.also_beasts = []
        self.absolute_id = False
        self.dimension = None
        self.x = 0
        self.y = 0

    @property
    def all(self):
        return [self.up, self.down, self.right, self.left, self.inner]

    @all.setter
    def all(self, value):
        self.left = value
        self.right = value
        self.up = value
        self.down = value

    @property
    def all_orig(self):
        return [self.orig_up, self.orig_down, self.orig_left, self.orig_right, self.orig_inner]

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
