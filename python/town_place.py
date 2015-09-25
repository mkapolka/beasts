import uuid


def dialog(text):
    longest_line = max(len(l) for l in text)
    data = [
        line + '_' * (longest_line - len(line)) for line in text
    ]
    outer_id = uuid.uuid4().hex
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
            '@@@@@@@@@@@@@@@@@@@@',
            '@__________________@',
            '@_######__######___@',
            '@_#w##w#__####w#___@',
            '@_##d###__##d###___@',
            '@___~~~~~~~~~______@',
            '@________~_2######_@',
            '@________~_p##ww##_@',
            '@__1_____~__####d#_@',
            '@__p_____~~~~~~~~__@',
            '@____e_____________@',
            '@@@@@@@@@@@@@@@@@@@@',
        ],
        'legend': {
            '_': {'sprite': 'grass'},
            '@': {'sprite': 'stone'},
            '~': {'sprite': 'dirt_path'},
            '#': {'sprite': 'stucco'},
            'd': {'sprite': 'door'},
            'w': {'sprite': 'window'},
            '1': dialog(["WELCOME", "TRAVELER"]),
            '2': dialog(["PLEASE", "SLAY", "WIZARD"]),
            'p': {'sprite': 'rando'},
            'e': {
                'id': 'town_entrance'
            }
        }
    }
]
