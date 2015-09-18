import random
import uuid


total_trees = 0
total_canopies = 0


def timer(time, from_link, sprite, head_data, tail_data):
    base_id = uuid.uuid4().hex
    alsos = [
        {
            'id': uuid.uuid4().hex,
            'sprite': sprite,
            'song': 'tut bo gobo',
            'absolute_id': True
        } for n in range(time)
    ]

    for n, also in enumerate(alsos[1:]):
        also['stitches'] = {
            'left': '%s//r' % alsos[n - 1]['id']
        }

    alsos[0]['stitches'] = {
        'left': '%s//r' % base_id
    }

    if 'stitches' in tail_data:
        alsos[-1]['stitches'].update(tail_data['stitches'])
        del tail_data['stitches']

    alsos[-1].update(tail_data)

    return dict({
        'id': base_id,
        'sprite': 'wood',
        'song': 'tut bo %s' % from_link,
        'also': alsos,
        'absolute_id': True
    }, **head_data)


def resetter(id, sprite, a_check, b_check, from_link, to_link):
    return {
        'id': id,
        'sprite': sprite,
        'song': 'ibi %s %s tut %s %s' % (a_check, b_check, to_link, from_link),
    }


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
            '#s#',
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
                },
                'also': [
                    timer(3, 'gobo', 'bog', head_data={
                        'stitches': {
                            'left': 'eagle_head//r'
                        }
                    },
                        tail_data={
                            'stitches': {
                                'up': 'eagle_resetter//r'
                            },
                            'song': 'tut ro gobo'
                    })
                ]
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
                'song': 'tut gogo robogo',
                'stitches': {
                    'right': 'eagle_head/',
                    'left': 'eagle_out/'
                }
            },
            'r': {
                'id': 'eagle_right_syncer',
                'sprite': 'glove',
                'song': 'tut roro goboro',
                'stitches': {
                    'right': 'eagle_out/',
                    'left': 'eagle_head/'
                }
            },
            'u': {
                'id': 'eagle_up_syncer',
                'sprite': 'glove',
                'song': 'tut bobo pobobo',
                'stitches': {
                    'up': 'eagle_out/',
                    'down': 'eagle_head/'
                }
            },
            'd': {
                'id': 'eagle_down_syncer',
                'sprite': 'glove',
                'song': 'tut popo bobopo',
                'stitches': {
                    'up': 'eagle_head//',
                    'down': 'eagle_out//'
                }
            },
            's': dict(resetter('eagle_resetter', 'tree', 'bobo', 'poro', 'robobo', 'bobo'), **{
                'stitches': {
                    'up': 'eagle_head/',
                    'right': 'daisychain/'
                }
            })
        },
    }
]
