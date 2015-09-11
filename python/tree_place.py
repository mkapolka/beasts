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
            '_____',
            '_t___',
            'e___t',
            '_____',
            '_t___',
        ],
        'legend': {
            '_': {
                'sprite': 'leafs'
            },
            't': tree,
            'e': {'id': 'tree_entrance', 'sprite': 'leafs'}
        },
        'wrap_mode': 'looped'
    },
    {
        'data': [
            'vvvvvvv',
            'v_____v',
            'v_c___v',
            'v____cv',
            'v_____v',
            'v_c___v',
            'vvvvvvv',
        ],
        'legend': {
            '_': {
                'sprite': 'slime'
            },
            'c': canopy_entrance,
            'v': {'sprite': 'void'}
        }
    }
]
