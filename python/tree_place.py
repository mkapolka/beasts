import random


total_trees = 0
total_canopies = 0


def canopy_entrance():
    global total_canopies
    id = 'canopy_entrance_%d' % total_canopies
    total_canopies += 1
    return {
        'id': id,
        'sprite': 'hole'
    }


def tree():
    global total_trees
    tree_number = total_trees
    id = 'tree_%d' % tree_number
    total_trees += 1
    return {
        'id': id,
        'sprite': 'tree',
        'dimension': {
            'data': [
                '#^#',
                '#_#',
                '#_#',
                '#_#',
                '#_#',
            ],
            'legend': {
                '_': {'sprite': 'cobble'},
                '#': {'sprite': 'wood'},
                '^': {
                    'sprite': 'cobble',
                    'stitches': {
                        'up': 'canopy_entrance_%d//r' % tree_number
                    }
                }
            },
            'exits': 'd'
        },
        'innie': True,
        'entrances': 'u'
    }


data = [
    {
        'data': [
            '^^^^^^^^^^^^^^^^^^^^^^^',
            '_______t_______________',
            'e_____________________t',
            '______________t________',
            'vvvvvvvvvvvvvvvvvvvvvvv',
        ],
        'legend': {
            '_': lambda: {'sprite': 'leafs' if random.random() < .5 else 'bog'},
            't': tree,
            'e': {'id': 'tree_entrance', 'sprite': 'leafs'},
            '^': {
                'sprite': 'leafs',
                'stitches': {
                    'up': '/ur/r',
                }
            },
            'v': {
                'sprite': 'leafs',
                'stitches': {
                    'down': '/dl/r',
                }
            }
        },
        'wrap_mode': 'looped'
    },
    {
        'data': [
            'vvvvvvv',
            'v__b__v',
            'v_____v',
            'v_____v',
            'v_c___v',
            'v_____v',
            'v_____v',
            'v_____v',
            'v____cv',
            'v_____v',
            'v___e_v',
            'v_____v',
            'v____}v',
            'v_c__>v',
            'vvvvvvv',
        ],
        'legend': {
            '_': {
                'sprite': 'slime'
            },
            'c': canopy_entrance,
            'v': {'sprite': 'void'},
            'b': {
                'sprite': 'boulder',
                'type': 'teleporter',
                'to_id': 'flower_entrance',
            },
            'e': {
                'id': 'eagle_start',
                'sprite': 'slime',
            },
            '>': {
                'type': 'teleporter',
                'to_id': 'eagle_head'
            },
            "}": {
                'type': 'teleporter',
                'to_id': 'eagle_inside_entrance'
            }
        }
    },
    {  # The Eagle
        'data': [
            '<^>',
            '<_>',
            '<v>',
            '###',
            'lhu',
            'rod',
        ],
        'legend': {
            'h': {
                'id': 'eagle_head',
                'sprite': 'head',
                'song': 'tut bo bobo',
                'stitches': {
                    'up': 'eagle_start/'
                }
            },
            'o': {
                'id': 'eagle_out',
                'sprite': 'foot',
                'type': 'alta',
                'to_id': 'eagle_start',
                'innie': True,
                'dimension': {
                    'data': [
                        '___',
                        '_e_',
                        '___',
                    ],
                    'exits': 'lrud',
                    'legend': {
                        'e': {
                            'id': 'eagle_inside_entrance',
                            'absolute_id': True
                        }
                    }
                }
            },
            'l': {
                'id': 'eagle_left_syncer',
                'sprite': 'glove',
                'song': 'tut gogo robo',
                'stitches': {
                    'right': 'eagle_head/',
                    'left': 'eagle_out/'
                }
            },
            'r': {
                'id': 'eagle_right_syncer',
                'sprite': 'glove',
                'song': 'tut roro gobo',
                'stitches': {
                    'right': 'eagle_out/',
                    'left': 'eagle_head/'
                }
            },
            'u': {
                'id': 'eagle_up_syncer',
                'sprite': 'glove',
                'song': 'tut bobo pobo',
                'stitches': {
                    'up': 'eagle_out/',
                    'down': 'eagle_head/'
                }
            },
            'd': {
                'id': 'eagle_down_syncer',
                'sprite': 'glove',
                'song': 'tut popo bobo',
                'stitches': {
                    'up': 'eagle_head//',
                    'down': 'eagle_out//'
                }
            },
        },
    }
]
