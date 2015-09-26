import uuid


def killer():
    base_id = uuid.uuid4().hex
    return {
        'id': base_id,
        'sprite': 'lava',
        'also': [
            {
                'sprite': 'feather',
                'stitches': {
                    'right': 'player/',
                    'left': '%s/' % base_id,
                    'down': 'hell/'
                },
                'song': 'ibi rowo go tut rowo po'
            }
        ]
    }


def gravity():
    base_id = uuid.uuid4().hex
    return {
        'id': base_id,
        'sprite': 'cobble',
        'also': [
            {
                'sprite': 'feather',
                'stitches': {
                    'right': 'player/',
                    'left': '%s/' % base_id
                },
                'song': 'ibi rowo go tut rowo gopo'
            }
        ]
    }


def celebrant_copier(direction, base_id, celebrant_id):
    return {
        'sprite': 'glove',
        'song': 'ibi goro ro tut po%s bo' % direction,
        'stitches': {
            'left': 'player/',
            'right': 'sword/',
            'down': '%s/%s/' % (base_id, {'po': 'u', 'bo': 'd', 'ro': 'l', 'go': 'r'}[direction]),
            'up': '%s/' % celebrant_id
        }
    }


def celebrant(celebrant_info, default_sprite='grass'):
    base_id = uuid.uuid4().hex
    celebrant_id = celebrant_info.get('id', None) or uuid.uuid4().hex
    celebrant_info['id'] = celebrant_id
    stitches = {
        'left': '%s/l/' % base_id,
        'right': '%s/r/' % base_id,
        'down': '%s/d/' % base_id,
        'up': '%s/u/' % base_id,
    }
    if 'stitches' not in celebrant_info:
        celebrant_info['stitches'] = {}
    for direction in stitches.keys():
        if direction not in celebrant_info.get('stitches', {}).keys():
            celebrant_info['stitches'][direction] = '%s/%s/' % (base_id, direction[0])

    return {  # celebrant
        'id': base_id,
        'sprite': default_sprite,
        'also': [
            celebrant_copier('po', base_id, celebrant_id),
            celebrant_copier('bo', base_id, celebrant_id),
            celebrant_copier('ro', base_id, celebrant_id),
            celebrant_copier('go', base_id, celebrant_id),
            celebrant_info
        ]
    }


def dialog(text, id=None):
    longest_line = max(len(l) for l in text)
    data = [
        line + '_' * (longest_line - len(line)) for line in text
    ]
    outer_id = id or uuid.uuid4().hex
    return {
        'id': outer_id,
        'sprite': 'dialog',
        'innie': True,
        'entrances': 'u',
        'dimension': {
            'data': data,
            'legend': {
                '_': {'sprite': 'darkness'},
            }
        }
    }


data = [
    {
        'data': [
            '@@@@@@@@@@@@@@@@@@@@@@@@',
            '@_________+_+3+_+__@@@@@',
            '@__________+cpc+___@@@@@',
            '@_######__+c_s_c+__@@@@@',
            '@_#w##w#___+c_c+___@@@4@',
            '@_##d###__+_+_+_+__...p@',
            '@___~~~~~~~~~~~~~~~....>',
            '@________~_2######_....@',
            '@________~_p##ww##_@@@@@',
            '@__1_____~__####h#_@@@@@',
            '@__p_____~~~~~~~~__@@@@@',
            '@____e___~_________@@@@@',
            '@@@@@@@@@@@@@@@@@@@@@@@@',
        ],
        'legend': {
            '_': {'sprite': 'grass'},
            '@': {'sprite': 'stone'},
            '~': {'sprite': 'dirt_path'},
            '#': {'sprite': 'stucco'},
            '+': {'sprite': 'stone'},
            '.': {'sprite': 'cobble'},
            's': {'id': 'sword', 'sprite': 'sword'},
            'd': {  # domicile
                'sprite': 'door',
                'stitches': {
                    'up': 'home_1_entrance//r'
                }
            },
            'h': {  # home
                'sprite': 'door',
                'stitches': {
                    'up': 'home_2_entrance//r'
                }
            },
            'w': {'sprite': 'window'},
            '1': dialog(["HELLO", "FRIEND"]),
            '2': dialog(["PLEASE", "SLAY", "WIZARD"]),
            '3': dialog(["DRAG", "SWORD", "RIGHT", "HAND"]),
            '4': dialog(["CANT", "LEAVE", "WITHOUT", "SWORD"]),
            'p': {'sprite': 'rando'},
            'e': {
                'id': 'town_entrance'
            },
            'c': lambda: celebrant({
                'sprite': 'celebrant',
            }),
            '>': lambda: celebrant({
                'sprite': 'gate',
                'stitches': {
                    # 'right': 'tree_entrance//r'
                    'right': 'flower_entrance//r'
                }
            }, 'gate')
        }
    },
    {
        'data': [
            '########',
            '#1s___s#',
            '#p___l_#',
            '#______#',
            '###v####',
        ],
        'legend': {
            '#': {'sprite': 'stucco'},
            '_': {'sprite': 'cobble'},
            'w': {'sprite': 'window'},
            's': {'sprite': 'stool'},
            'l': {'sprite': 'lamp'},
            'p': {'sprite': 'rando'},
            '1': dialog(["MAKE", "URSELF", "AT", "HOME"]),
            'v': {'sprite': 'cobble', 'id': 'home_1_entrance'}
        }
    },
    {
        'data': [
            '########',
            '#h___1_#',
            '#____p_#',
            '#______#',
            '###v####',
        ],
        'legend': {
            '#': {'sprite': 'stucco'},
            '_': {'sprite': 'cobble'},
            'p': {'sprite': 'rando'},
            '1': dialog(["DONT", "GO IN", "HOLE"]),
            'h': {
                'sprite': 'hole',
                'type': 'alta',
                'to_id': 'into_hole'
            },
            'v': {'sprite': 'cobble', 'id': 'home_2_entrance'}
        }
    },
    {
        'data': [
            '<_____>'
        ],
        'legend': {
            '<': {
                'id': 'into_hole',
                'sprite': 'darkness',
                'stitches': {
                    'left': 'sr',
                    'right': 'sr',
                    'up': 'sr',
                    'down': 'sr',
                }
            },
            '>': {
                'sprite': 'darkness',
                'stitches': {
                    'left': 'bottom_of_hole/',
                    'right': 'bottom_of_hole/',
                    'up': 'bottom_of_hole/',
                    'down': 'bottom_of_hole/',
                }
            },
            '_': {
                'sprite': 'darkness',
                'stitches': {
                    'left': 'sr',
                    'right': 'sr',
                    'up': 'sr',
                    'down': 'sr',
                }
            }
        }
    },
    {
        'data': [
            '~~~~~~~~~~~~~~~~~~~~',
            '~vvvvvvvvvvvvvvvvvo~',
            '~vvvvvvvvvvvvvvv___~',
            '~^___vv___vvv___vvv~',
            '~~~~~~~~~~~~~~~~~~~~',
        ],
        'legend': {
            '_': {'sprite': 'wood'},
            '^': {'sprite': 'wood', 'id': 'bottom_of_hole'},
            '~': killer,
            'v': gravity,
            'o': {
                'sprite': 'hole',
                'type': 'alta',
                'to_id': 'home_2_entrance'
            }
        },
    }
]
