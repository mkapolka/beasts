import inspect
import collections
import random
import uuid


from beast import Beast

from map_data import maps


class BeastGrid(object):
    def __init__(self, width, height, wrap_mode='bounded'):
        self.beasts = [[None for _ in range(0, height)] for _ in range(0, width)]
        self.width = width
        self.height = height
        self.wrap_mode = wrap_mode
        self.extra_beasts = []

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
        for beast in self.extra_beasts:
            yield beast


def init_beast(custom_data, all_beasts, id_prepend=''):
    beast = Beast(custom_data.get('symbol', '?'))
    beast.id = uuid.uuid4().hex

    for key, value in custom_data.items():
        if isinstance(value, dict):
            setattr(beast, key, dict(value.items()))
        else:
            setattr(beast, key, value)
    if id_prepend and not beast.absolute_id:
        beast.id = '%s_%s' % (id_prepend, beast.id)
    beast.type = custom_data.get('type', None)
    beast.sprite = custom_data['sprite']
    for beast_data in custom_data.get('also', []):
        if inspect.isfunction(beast_data):
            beast_data = beast_data()
        also_beast = init_beast(beast_data, all_beasts, id_prepend)
        all_beasts.append(also_beast)
        beast.also_beasts.append(also_beast)
    return beast


def initialize_grid(map_data, id_prepend=''):
    md = map_data['data']
    legend = map_data.get('legend', {})

    height = len(md)
    width = len(md[0])
    beast_map = BeastGrid(width, height, map_data.get('wrap_mode', 'bounded'))
    for y, line in enumerate(md):
        for x, char in enumerate(line):
            symbol = md[y][x]
            if symbol in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                default_data = {
                    'sprite': 'letter_%s' % symbol.lower()
                }
            else:
                default_data = {'sprite': 'void'}
            custom_data = legend.get(symbol, default_data)
            if inspect.isfunction(custom_data):
                custom_data = custom_data()
            default_data.update(custom_data)
            beast = init_beast(default_data, beast_map.extra_beasts, id_prepend)
            beast.x = x
            beast.y = y
            beast_map.set(x, y, beast)
    for (x, y) in beast_map.all_points():
            beast = beast_map.get(x, y)
            beast.left = beast.orig_left = beast_map.get(x - 1, y)
            beast.right = beast.orig_right = beast_map.get(x + 1, y)
            beast.up = beast.orig_up = beast_map.get(x, y - 1)
            beast.down = beast.orig_down = beast_map.get(x, y + 1)
    return beast_map


def do_pocket(pocket, all_beasts, customs):
    pocket.innie = getattr(pocket, 'innie', False)
    pocket_map = initialize_grid(pocket.dimension, pocket.id)
    pocket.map = pocket_map
    for beast in pocket_map.all_beasts():
        all_beasts[beast.id] = beast
        if beast.type:
            customs[beast.type].append(beast)
        if beast.stitches:
            customs['stitched'].append(beast)
        if beast.dimension:
            customs['pocket'].append(beast)
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
    dirs = 's'
    flags = ''
    if len(parts) == 1:
        dirs = string
    elif len(parts) == 2:
        current = all_beasts[parts[0]] if parts[0] else current
        dirs = parts[1]
    elif len(parts) == 3:
        current = all_beasts[parts[0]] if parts[0] else current
        dirs = parts[1]
        flags = parts[2]

    for direction in dirs:
        current = {
            'u': current.orig_up,
            'd': current.orig_down,
            'r': current.orig_right,
            'l': current.orig_left,
            'i': current.inner,
            's': current
        }[direction]
    return current, flags


def stitch(beast, all_beasts, up_string='', down_string='', left_string='', right_string='', inner_string=''):
    up, ur = calc_stitch_string(beast, up_string, all_beasts) if up_string else (beast.up, False)
    down, dr = calc_stitch_string(beast, down_string, all_beasts) if down_string else (beast.down, False)
    left, lr = calc_stitch_string(beast, left_string, all_beasts) if left_string else (beast.left, False)
    right, rr = calc_stitch_string(beast, right_string, all_beasts) if right_string else (beast.right, False)
    inner, ir = calc_stitch_string(beast, inner_string, all_beasts) if inner_string else (beast.inner, False)
    beast.up = up
    beast.down = down
    beast.left = left
    beast.right = right
    beast.inner = inner
    if ur == 'r':
        beast.up.down = beast
    elif ur == 'c':
        beast.orig_up.down = beast.orig_up

    if dr == 'r':
        beast.down.up = beast
    elif dr == 'c':
        beast.orig_down.up = beast.orig_down

    if lr == 'r':
        beast.left.right = beast
    elif lr == 'c':
        beast.orig_left.right = beast.orig_left

    if rr == 'r':
        beast.right.left = beast
    elif rr == 'c':
        beast.orig_right.left = beast.orig_right

    if ir == 'r':
        beast.inner.inner = beast
    elif ir == 'c':
        beast.orig_inner.inner = beast.orig_inner


def generate(maps):
    customs = collections.defaultdict(list)
    all_beasts = {}
    for map_data in maps:
        beast_map = initialize_grid(map_data)
        for beast in beast_map.all_beasts():
            all_beasts[beast.id] = beast
            if beast.type:
                customs[beast.type].append(beast)
            if beast.stitches:
                customs['stitched'].append(beast)
            if beast.dimension:
                customs['pocket'].append(beast)

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
        corners = '%s%s%s%s' % (
            'F' if wall.left.up.type != 'wall' else '',
            'J' if wall.right.down.type != 'wall' else '',
            '7' if wall.right.up.type != 'wall' else '',
            'L' if wall.left.down.type != 'wall' else '',
        )
        if adjacent == 'l':
            wall.right = wall
        if adjacent == 'r':
            wall.left = wall
        if adjacent == 'u':
            wall.down = wall
        if adjacent == 'd':
            wall.up = wall

        if not adjacent and corners == 'F':
            wall.right = wall
            wall.down = wall
        if not adjacent and corners == 'J':
            wall.left = wall
            wall.up = wall
        if not adjacent and corners == '7':
            wall.left = wall
            wall.down = wall
        if not adjacent and corners == 'L':
            wall.right = wall
            wall.up = wall

    for extender in customs['portal_extender']:
        base = all_beasts.get(extender.base_id)
        reciprocal = getattr(extender, 'reciprocal', False)
        offset_x = base.x - extender.x
        offset_y = base.y - extender.y
        rel_string = ''
        if offset_x > 0:
            rel_string += 'l' * offset_x
        if offset_x < 0:
            rel_string += 'r' * (offset_x * -1)
        if offset_y > 0:
            rel_string += 'u' * offset_y
        if offset_y < 0:
            rel_string += 'd' * (offset_y * -1)
        for key in base.stitches.keys():
            extender.stitches[key] = base.stitches[key] + rel_string + '/r' if reciprocal else ''

    for stitched in all_beasts.values():
        stitches = stitched.stitches
        if stitches:
            stitch(stitched, all_beasts, stitches.get('up', ''), stitches.get('down', ''), stitches.get('left', ''), stitches.get('right', ''), stitches.get('inner', ''))
    for origin in customs['rill_origin']:
        rills = customs['rill']
        rill_path = [origin]
        n = origin
        while n is not None:
            c = n
            n = None
            for adjacent in c.all_orig:
                if adjacent in rills and adjacent not in rill_path:
                    rill_path.append(adjacent)
                    rills.remove(adjacent)
                    n = adjacent
        watchers = [Beast('r') for b in rill_path]
        for n, watcher in enumerate(watchers):
            watcher.sprite = 'rill'
            watcher.left = watchers[n - 1]
            watcher.right = watchers[n + 1] if n < len(watchers) - 1 else watchers[0]
            watcher.up = rill_path[n]
            watcher.down = rill_path[n]
            all_beasts[watcher.id] = watcher
        # Rill rider
        rill_rider = next(b for b in origin.also_beasts if b.type == 'rill_rider')
        rill_rider.up = watchers[0]
        all_beasts[rill_rider.id] = rill_rider

    for n, lurkroom in enumerate(customs['lurkroom']):
        previous = customs['lurkroom'][n - 1]
        lurkmap = lurkroom.map
        previous_lurkmap = previous.map
        for (x, y) in lurkmap.right_wall_points():
            lurkmap.get(x, y).right = previous_lurkmap.get(0, y)
            previous_lurkmap.get(0, y).left = lurkmap.get(x, y)

    # THE GOLDEN RILL
    golden_rill = []
    shuffled_beasts = all_beasts.values()
    random.shuffle(shuffled_beasts)
    for beast in shuffled_beasts:
        rill_segment = Beast('golden_rill')
        rill_segment.sprite = 'golden_rill'
        rill_segment.up = beast
        rill_segment.down = beast
        golden_rill.append(rill_segment)
    for n, beast in enumerate(golden_rill):
        left = golden_rill[n - 1]
        beast.left = left
        beast.left.right = beast

    for rider in customs['golden_rill_rider']:
        rider.up = random.choice(golden_rill)

    all_beasts['golden_rill_origin'].down = golden_rill[0]

    for rill in golden_rill:
        all_beasts[rill.id] = rill

    return all_beasts.values()

# bb = next(b for b in generate(maps) if b.id == 'start')

if __name__ == "__main__":
    outfile = open('output.txt', 'w')
    beasts = generate(maps)
    for beast in beasts:
        outfile.write(','.join([beast.id,
                                beast.sprite,
                                beast.right.id,
                                beast.up.id,
                                beast.left.id,
                                beast.down.id,
                                beast.inner.id,
                                beast.song.replace(',', '/'),
                                str(beast.tick_speed)]))
        outfile.write('\n')
    outfile.flush()
