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

data = [
    {
        'id': 'wizpock_2',
        'wrap_mode': 'stitched',
        'stitches': {
            'up': 'wizpock_1',
            'down': 'wizpock_1',
            'left': 'wizpock_1',
            'right': 'wizpock_1',
        },
        'data': [
            '#########',
            '#~~_____#',
            '#_~~~___#',
            '#___~~~~#',
            '#___@__~#',
            '#_____~~#',
            '#_~~~~~_#',
            '#~~_____#',
            '#########',
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
            's': {'id': 'start'},
            '!': {'sprite': 'golden_wall'},
            '#': {'sprite': 'stone'},
            '_': {'sprite': 'cobble'},
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
