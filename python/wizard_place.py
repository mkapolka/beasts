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
