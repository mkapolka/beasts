import uuid

from map_data import lurker


def fairy(fairy_id=None):
    fairy_id = fairy_id if fairy_id else uuid.uuid4().hex
    return {
        'id': fairy_id,
        'sprite': 'golden_rill_rider',
        'type': 'golden_rill_rider',
        'song': 'tut bo boro',
        'also': [
            lurker('golden_rill_rider', fairy_id, 'bobo')
        ]
    }


data = [
    {
        'data': [
            '#########',
            '#_2_f_f_#',
            '#f_____f#',
            '#_______#',
            '#f_____f#',
            '#_______#',
            '#f_____f#',
            '#_f___f_#',
            '####r####',
        ],
        'legend': {
            '#': {'sprite': 'golden_wall'},
            '_': {'sprite': 'golden_floor'},
            'v': {
                'sprite': 'pillar'
                # 'type': 'alta',
                # 'to_id': 'void'
            },
            'f': fairy,
            '2': fairy('daisychain'),
            'r': {
                'sprite': 'golden_floor',
                'stitches': {
                    'down': 'golden_rill_origin//r'
                }
            }
        }
    }
]
