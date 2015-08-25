import collections
import uuid


from beast import Beast

from map_data import maps


class BeastGrid(object):
    def __init__(self, width, height, wrap_mode='bounded'):
        self.beasts = [[None for _ in range(0, height)] for _ in range(0, width)]
        self.width = width
        self.height = height
        self.wrap_mode = wrap_mode

    def get(self, x, y):
        if x < 0 or x >= self.width:
            if self.wrap_mode == 'bounded':
                x = 0 if x < 0 else self.width - 1
            else:  # wrap
                x %= self.width
        if y < 0 or y >= self.height:
            if self.wrap_mode == 'bounded':
                y = 0 if y < 0 else self.height - 1
            else:
                y %= self.height
        return self.beasts[x][y]

    def set(self, x, y, beast):
        self.beasts[x][y] = beast

    def all_points(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield (x, y)

    def left_wall_points(self):
        for y in range(0, self.height):
            yield (0, y)

    def right_wall_points(self):
        for y in range(0, self.height):
            yield (self.width - 1, y)

    def up_wall_points(self):
        for x in range(0, self.width):
            yield (x, 0)

    def down_wall_points(self):
        for x in range(0, self.width):
            yield (x, self.height - 1)

    def edge_points(self):
        for x in range(0, self.width):
            for y in [0, self.height - 1]:
                yield (x, y)
        for x in [1, self.width - 1]:
            for y in range(0, self.height - 1):
                yield (x, y)

    def all_beasts(self):
        for point in self.all_points():
            yield self.get(*point)


def initialize_grid(map_data):
    md = map_data['data']
    legend = map_data.get('legend', {})

    height = len(md)
    width = len(md[0])
    beast_map = BeastGrid(width, height, map_data.get('wrap_mode', 'bounded'))
    sprites = map_data.get('sprites', {
        '_': 'grass',
        '#': 'stone',
        'default': 'bog'
    })
    for y, line in enumerate(md):
        for x, char in enumerate(line):
            symbol = md[y][x]
            beast = Beast(symbol)
            beast.id = uuid.uuid4().hex
            beast.sprite = sprites.get(symbol, sprites['default'])
            if symbol in legend.keys():
                entry = legend[symbol]
                for key, value in entry.items():
                    setattr(beast, key, value)
                beast.type = entry.get('type', None)
                beast.sprite = entry.get('sprite', sprites.get(symbol, sprites['default']))
            beast_map.set(x, y, beast)
    for (x, y) in beast_map.all_points():
            beast = beast_map.get(x, y)
            beast.left = beast.orig_left = beast_map.get(x - 1, y)
            beast.right = beast.orig_right = beast_map.get(x + 1, y)
            beast.up = beast.orig_up = beast_map.get(x, y - 1)
            beast.down = beast.orig_down = beast_map.get(x, y + 1)
    return beast_map


def do_pocket(pocket, all_beasts, customs):
    pocket.innie = pocket.innie if getattr(pocket, 'innie', False) else False
    pocket_map = initialize_grid(pocket.dimension)
    for beast in pocket_map.all_beasts():
        all_beasts[beast.id] = beast
        if beast.type:
            customs[beast.type].append(beast)
    exits = pocket.dimension.get('exits', 'lrud')
    if 'l' in exits:
        for point in pocket_map.left_wall_points():
            pocket_map.get(*point).left = pocket.left
    if 'r' in exits:
        for point in pocket_map.right_wall_points():
            pocket_map.get(*point).right = pocket.right
    if 'u' in exits:
        for point in pocket_map.up_wall_points():
            pocket_map.get(*point).up = pocket.up
    if 'd' in exits:
        for point in pocket_map.down_wall_points():
            pocket_map.get(*point).down = pocket.down
    entrances = getattr(pocket, 'entrances', 'lrud')
    if 'l' in entrances:
        v = pocket_map.get(pocket_map.width - 1, pocket_map.height / 2)
        if pocket.innie:
            pocket.left = v
        else:
            pocket.right.left = v
    if 'r' in entrances:
        v = pocket_map.get(0, pocket_map.height / 2)
        if pocket.innie:
            pocket.right = v
        else:
            pocket.left.right = v
    if 'u' in entrances:
        v = pocket_map.get(pocket_map.width / 2, pocket_map.height - 1)
        if pocket.innie:
            pocket.up = v
        else:
            pocket.down.up = v
    if 'd' in entrances:
        v = pocket_map.get(pocket_map.width / 2, 0)
        if pocket.innie:
            pocket.down = v
        else:
            pocket.up.down = v


def do_teleporter(teleporter, all_beasts, customs):
    other = all_beasts[teleporter.to_id]
    lt = teleporter.clone('_left')
    lt.left = other.orig_left
    lt.up = other.orig_up
    lt.down = other.orig_down
    teleporter.right.left = lt

    rt = teleporter.clone('_right')
    rt.right = other.orig_right
    rt.up = other.orig_up
    rt.down = other.orig_down
    teleporter.left.right = rt

    ut = teleporter.clone('_up')
    ut.up = other.orig_up
    ut.left = other.orig_left
    ut.right = other.orig_right
    teleporter.down.up = ut

    dt = teleporter.clone('_down')
    dt.down = other.orig_down
    dt.left = other.orig_left
    dt.right = other.orig_right
    teleporter.up.down = dt

    all_beasts[lt.id] = lt
    all_beasts[rt.id] = rt
    all_beasts[ut.id] = ut
    all_beasts[dt.id] = dt


def calc_stitch_string(beast, string, all_beasts):
    """ id/udlr """
    parts = string.split('/')
    current = beast
    if len(parts) > 1:
        current = all_beasts[parts[0]]
    for direction in parts[-1]:
        current = {
            'u': current.orig_up,
            'd': current.orig_down,
            'r': current.orig_right,
            'l': current.orig_left,
            'i': current.inner,
            's': current
        }[direction]
    return current


def stitch(beast, all_beasts, up_string='', down_string='', left_string='', right_string='', inner_string=''):
    up = calc_stitch_string(beast, up_string, all_beasts) if up_string else beast.up
    down = calc_stitch_string(beast, down_string, all_beasts) if down_string else beast.down
    left = calc_stitch_string(beast, left_string, all_beasts) if left_string else beast.left
    right = calc_stitch_string(beast, right_string, all_beasts) if right_string else beast.right
    inner = calc_stitch_string(beast, inner_string, all_beasts) if inner_string else beast.inner
    beast.up = up
    beast.down = down
    beast.left = left
    beast.right = right
    beast.inner = inner


def generate(maps):
    customs = collections.defaultdict(list)
    all_beasts = {}
    for map_data in maps:
        beast_map = initialize_grid(map_data)
        for beast in beast_map.all_beasts():
            all_beasts[beast.id] = beast
            if beast.type:
                customs[beast.type].append(beast)
    for pocket in customs['pocket']:
        do_pocket(pocket, all_beasts, customs)

    for alta in customs['alta']:
        alta.all = all_beasts[alta.to_id]

    for teleporter in customs['teleporter']:
        do_teleporter(teleporter, all_beasts, customs)

    for wall in customs['wall']:
        adjacent = '%s%s%s%s' % (
            'l' if wall.left.type != 'wall' else '',
            'r' if wall.right.type != 'wall' else '',
            'u' if wall.up.type != 'wall' else '',
            'd' if wall.down.type != 'wall' else '',
        )
        if adjacent == 'l':
            wall.right = wall
        if adjacent == 'r':
            wall.left = wall
        if adjacent == 'u':
            wall.down = wall
        if adjacent == 'd':
            wall.up = wall
    for stitched in customs['stitched']:
        stitches = stitched.stitches
        stitch(stitched, all_beasts, stitches.get('up', ''), stitches.get('down', ''), stitches.get('left', ''), stitches.get('right', ''), stitches.get('inner', ''))

    return all_beasts.values()

bb = next(b for b in generate(maps) if b.id == 'start')

if __name__ == "__main__":
    outfile = open('output.txt', 'w')
    beasts = generate(maps)
    for beast in beasts:
        outfile.write(','.join([beast.id, beast.sprite, beast.right.id, beast.up.id, beast.left.id, beast.down.id, beast.inner.id, beast.song.replace(',', '/')]))
        outfile.write('\n')
    outfile.flush()
