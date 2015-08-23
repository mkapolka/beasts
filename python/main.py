from collections import deque

from curses import wrapper

from maps import bb


render_pattern = [
    "^^^^^^^^^<<<<<<<<<<^>>>>>>>>>>^^^^^^^^^^",
    "^^^^^^^^^^<<<<<<<<<^>>>>>>>>>^^^^^^^^^^^",
    "^^^^^^^^^^^<<<<<<<<^>>>>>>>>^^^^^^^^^^^^",
    "^^^^^^^^^^^^<<<<<<<^>>>>>>>^^^^^^^^^^^^^",
    "^^^^^^^^^^^^^<<<<<<^>>>>>>^^^^^^^^^^^^^^",
    "^^^^^^^^^^^^^^<<<<<^>>>>>^^^^^^^^^^^^^^^",
    "^^^^^^^^^^^^^^^<<<<^>>>>^^^^^^^^^^^^^^^^",
    "^^^^^^^^^^^^^^^^<<<^>>>^^^^^^^^^^^^^^^^^",
    "^^^^^^^^^^^^^^^^^<<^>>^^^^^^^^^^^^^^^^^^",
    "^^^^^^^^^^^^^^^^^^<^>^^^^^^^^^^^^^^^^^^^",
    "<<<<<<<<<<<<<<<<<<<o>>>>>>>>>>>>>>>>>>>>",
    "vvvvvvvvvvvvvvvvvv<v>vvvvvvvvvvvvvvvvvvv",
    "vvvvvvvvvvvvvvvvv<<v>>vvvvvvvvvvvvvvvvvv",
    "vvvvvvvvvvvvvvvv<<<v>>>vvvvvvvvvvvvvvvvv",
    "vvvvvvvvvvvvvvv<<<<v>>>>vvvvvvvvvvvvvvvv",
    "vvvvvvvvvvvvvv<<<<<v>>>>>vvvvvvvvvvvvvvv",
    "vvvvvvvvvvvvv<<<<<<v>>>>>>vvvvvvvvvvvvvv",
    "vvvvvvvvvvvv<<<<<<<v>>>>>>>vvvvvvvvvvvvv",
    "vvvvvvvvvvv<<<<<<<<v>>>>>>>>vvvvvvvvvvvv",
    "vvvvvvvvvv<<<<<<<<<v>>>>>>>>>vvvvvvvvvvv",
    "vvvvvvvvv<<<<<<<<<<v>>>>>>>>>>vvvvvvvvvv",
]


render_pattern_2 = [
    "<^<^<^<^<^<^<^<^<^<^^>^>^>^>^>^>^>^>^>^>",
    "^<^<^<^<^<^<^<^<^<^^>^>^>^>^>^>^>^>^>^>^",
    "<^<^<^<^<^<^<^<^<^<^^>^>^>^>^>^>^>^>^>^>",
    "^<^<^<^<^<^<^<^<^<^^>^>^>^>^>^>^>^>^>^>^",
    "<^<^<^<^<^<^<^<^<^<^^>^>^>^>^>^>^>^>^>^>",
    "^<^<^<^<^<^<^<^<^<^^>^>^>^>^>^>^>^>^>^>^",
    "<^<^<^<^<^<^<^<^<^<^^>^>^>^>^>^>^>^>^>^>",
    "^<^<^<^<^<^<^<^<^<^^>^>^>^>^>^>^>^>^>^>^",
    "<^<^<^<^<^<^<^<^<^<^^>^>^>^>^>^>^>^>^>^>",
    "^<^<^<^<^<^<^<^<^<^^>^>^>^>^>^>^>^>^>^>^",
    "<<<<<<<<<<<<<<<<<<<o>>>>>>>>>>>>>>>>>>>>",
    "<v<v<v<v<v<v<v<v<v<v>v>v>v>v>v>v>v>v>v>v",
    "v<v<v<v<v<v<v<v<v<vvv>v>v>v>v>v>v>v>v>v>",
    "<v<v<v<v<v<v<v<v<v<v>v>v>v>v>v>v>v>v>v>v",
    "v<v<v<v<v<v<v<v<v<vvv>v>v>v>v>v>v>v>v>v>",
    "<v<v<v<v<v<v<v<v<v<v>v>v>v>v>v>v>v>v>v>v",
    "v<v<v<v<v<v<v<v<v<vvv>v>v>v>v>v>v>v>v>v>",
    "<v<v<v<v<v<v<v<v<v<v>v>v>v>v>v>v>v>v>v>v",
    "v<v<v<v<v<v<v<v<v<vvv>v>v>v>v>v>v>v>v>v>",
    "<v<v<v<v<v<v<v<v<v<v>v>v>v>v>v>v>v>v>v>v",
    "v<v<v<v<v<v<v<v<v<vvv>v>v>v>v>v>v>v>v>v>",
]


def render(beast, render_pattern):
    height = len(render_pattern)
    width = len(render_pattern[0])
    output = [[None for _ in range(0, height)] for _ in range(0, width)]
    # Find the 'o'
    center_y, line = next((y, line) for (y, line) in enumerate(render_pattern) if 'o' in line)
    center_x = line.index('o')
    queue = deque([(center_x, center_y, 'o')])
    output[center_x][center_y] = beast
    done = []
    while len(queue) > 0:
        x, y, command = queue.pop()

        done.append((x, y))

        if command == 'o':
            pass
        elif command == '^':
            output[x][y] = output[x][y + 1].up
        elif command == 'v':
            output[x][y] = output[x][y - 1].down
        elif command == '<':
            output[x][y] = output[x + 1][y].left
        elif command == '>':
            output[x][y] = output[x - 1][y].right

        for x2, y2 in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            in_bounds = (0 <= x2 < width and 0 <= y2 < height)
            if (x2, y2) not in done and in_bounds:
                command = (x2, y2, render_pattern[y2][x2])
                if command not in queue:
                    queue.appendleft(command)

    outline = ''
    for y in range(0, height):
        line = ''.join(output[x][y].symbol if (x, y) != (center_x, center_y) else 'X' for x in range(0, width))
        outline = '%s%s\n' % (outline, line)
    return outline


def loop(stdscr, beast):
    done = False
    while not done:
        for line in render(beast, render_pattern_2):
            stdscr.addstr(line)
        stdscr.move(0, 0)
        stdscr.refresh()
        com = stdscr.getkey()
        if com == 'h':
            beast = beast.left
        if com == 'l':
            beast = beast.right
        if com == 'k':
            beast = beast.up
        if com == 'j':
            beast = beast.down
        if com == 'q':
            done = True


if __name__ == "__main__":
    beast = bb
    wrapper(loop, beast)
