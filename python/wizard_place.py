import uuid
from map_data import lurker


def fireball_spawner():
    base_id = uuid.uuid4().hex
    id = uuid.uuid4().hex
    return {
        'sprite': 'cobble',
        'id': base_id,
        'stitches': {
            'right': '%s/' % id
        },
        'also': [{
            'id': id,
            'absolute_id': True,
            'sprite': 'fireball',
            'song': 'tut po popo',
            'stitches': {
                'down': '%s/' % base_id
            }},
            lurker('fireball', id, 'po'),
            {
                'sprite': 'sword',
                'stitches': {
                    'right': '%s//r' % id,
                    'left': 'player/',
                    'down': 'hell/'
                },
                'tick_speed': 1.0 / 5,
                'song': 'ibi gowo ropo tut gowo po'}
        ]
    }

to_orb_stitches = {
    'left': 'orb_pedestal/l',
    'right': 'orb_pedestal/r',
    'up': 'orb_pedestal/u',
    'down': 'orb_pedestal/d',
}

data = [
    {
        'id': 'orb_room',
        'data': [
            '       ',
            ' ##v## ',
            ' ##### ',
            ' ##o## ',
            ' ##### ',
            ' ##### ',
            '       ',
        ],
        'legend': {
            '#': {'sprite': 'cobble'},
            ' ': {'sprite': 'void'},
            'o': {
                'id': 'orb_pedestal',
                'sprite': 'orb_red'
            },
            'v': {
                'sprite': 'head',
                'stitches': {
                    'down': 'orb_mechanics/'
                }
            }
        }
    },
    {
        'data': [
            '****_s',
            '<>^v__',
            '~~~~~~',
            'roygbp',
        ],
        'wrap_mode': 'wrapped',
        'legend': {
            's': {'id': 'orb_mechanics'},
            '~': {'sprite': 'rill'},
            'r': {'sprite': 'orb_red', 'stitches': to_orb_stitches},
            'o': {'sprite': 'orb_orange', 'stitches': to_orb_stitches},
            'y': {'sprite': 'orb_yellow', 'stitches': to_orb_stitches},
            'g': {'sprite': 'orb_green', 'stitches': to_orb_stitches},
            'b': {'sprite': 'orb_blue', 'stitches': to_orb_stitches},
            'p': {'sprite': 'orb_purple', 'stitches': to_orb_stitches},
            '*': {
                'sprite': 'foot',
                'song': 'tut popo poporo'
            },
            '>': {
                'sprite': 'glove',
                'song': 'tut roro popo',
                'stitches': {'right': 'orb_pedestal/l', 'down': 'dl'}
            },
            '<': {
                'sprite': 'glove',
                'song': 'tut rogo popo',
                'stitches': {'right': 'orb_pedestal/r', 'down': 'd'}
            },
            '^': {
                'sprite': 'glove',
                'song': 'tut robo popo',
                'stitches': {'right': 'orb_pedestal/d', 'down': 'dll'}
            },
            'v': {
                'sprite': 'glove',
                'song': 'tut ropo popo',
                'stitches': {'right': 'orb_pedestal/u', 'down': 'dlll'}
            }
        }
    },
    {
        'id': 'wizpock_2',
        'wrap_mode': 'stitched',
        'stitches': {
            'up': 'orb_room',
            'down': 'wizpock_1',
            'left': 'wizpock_1',
            'right': 'wizpock_1',
        },
        'data': [
            '#####',
            '#___#',
            '#_@_#',
            '#___#',
            '#####',
        ],
        'legend': {
            '#': {'sprite': 'wood'},
            '_': {'sprite': 'grass'},
            '~': {'sprite': 'water_light'},
            '@': {
                'id': 'wizpock_2_center',
                'sprite': 'tree',
                'stitches': {
                    'left': 'wizpock_center/rrrr/o',
                    'right': 'wizpock_center/llll/o',
                    'down': 'wizpock_center/uuuu/o',
                    'up': 'wizpock_center/dddd/o',
                }
            },
        }
    },
    {
        'id': 'wizpock_1',
        'wrap_mode': 'stitched',
        'stitches': {
            'up': 'wizpock_2',
            'down': 'wizpock_2',
            'left': 'wizpock_2',
            'right': 'wizpock_2',
        },
        'data': [
            '#########',
            '#___s___#',
            '#_!___!_#',
            '#__!!!__#',
            '#__!@!__#',
            '#__!!!__#',
            '#_!___!_#',
            '#_______#',
            '#########'
        ],
        'legend': {
            # 's': {'id': 'start'},
            '!': {'sprite': 'golden_wall'},
            '#': {'sprite': 'ice_brick'},
            '_': {'sprite': 'tile'},
            '@': {
                'id': 'wizpock_center',
                'sprite': 'cobble',
                'stitches': {
                    'left': 'wizpock_2_center/rrr/o',
                    'right': 'wizpock_2_center/lll/o',
                    'down': 'wizpock_2_center/uuu/o',
                    'up': 'wizpock_2_center/ddd/o',
                }
            },
        }
    },
    {
        'data': [
            '##########',
            '#________#',
            '#________#',
            '<________#',
            '#__THE___#',
            '#__WIZARD#',
            '#__TOWER_#',
            '##&#######',
        ],
        'legend': {
            '#': {'sprite': 'stone'},
            '_': {'sprite': 'cobble'},
            '&': {
                'id': 'wizard_inside',
                'sprite': 'stone'
            },
            '<': {
                'sprite': 'door',
                'type': 'teleporter',
                'to_id': 'wizard_hallway'
            }
        }
    },
    {
        'data': [
            '#_#_#f##',
            '___f___<',
            '#f#_#_##',
        ],
        'wrap_mode': 'looped',
        'legend': {
            '#': {'sprite': 'stone'},
            '_': {'sprite': 'cobble'},
            'f': fireball_spawner,
            '<': {'id': 'wizard_hallway', 'sprite': 'cobble'}
        }
    }
]
