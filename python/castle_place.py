import uuid


def nogo(sprite):
    base_id = uuid.uuid4().hex
    inner_id = uuid.uuid4().hex
    return {
        'id': base_id,
        'absolute_id': True,
        'sprite': sprite,
        'also': [
            {
                'id': inner_id,
                'absolute_id': True,
                'sprite': 'glove',
                'stitches': {
                    'left': 'player_position_memory/',
                    'right': '%s/' % base_id,
                    'down': 'player/'
                },
                'song': 'ibi powo ro tut powo gobo'
            }
        ]
    }


def left_moat():
    return moat_entrance('')


def right_moat():
    return moat_entrance('r')


def moat_entrance(side):
    entrance_id = uuid.uuid4().hex
    return {
        'id': entrance_id,
        'sprite': 'wood',
        'entrances': '',
        'also': [
            {
                'id': '%s_cloner' % entrance_id,
                'sprite': 'glove',
                'stitches': {
                    'up': '%s/' % entrance_id,
                    'right': '%s_walker//r' % (entrance_id),
                    'down': 'castle_secret//r'
                },
                'song': 'tut bobo robobo'
            },
            {
                'id': '%s_walker' % entrance_id,
                'sprite': 'foot',
                'stitches': {
                    'up': '%s_rill/' % entrance_id
                },
                'song': 'tut bo boro'
            }
        ],
        'dimension': {
            'data': [
                'o~~1~~~~2~',
            ],
            'wrap_mode': 'looped',
            'exits': '',
            'legend': {
                'o': {
                    'id': 'rill',
                    'sprite': 'rill',
                    'stitches': {
                        'up': 'over_moat/%s' % side
                    }
                },
                '~': {
                    'sprite': 'rill',
                    'stitches': {
                        'up': 'over_moat/%s' % side
                    }
                },
                '1': {
                    'sprite': 'rill',
                    'stitches': {
                        'up': 'fake_bridge/%s' % side
                    }
                },
                '2': {
                    'sprite': 'rill',
                    'stitches': {
                        'up': 'inside_castle/%s' % side
                    }
                }
            }
        }
    }


data = [
    {  # Courtyard
        'data': [
            '___________s',
            '_~#~#~~#~#~_',
            '_~########~_',
            '_~#w####w#~_',
            '_~###DD###~_',
            '_~~~~o~~~~~_',
            '____#^>#____',
            '____________',
            '____________',
            '_____e______',
        ],
        'legend': {
            '_': {'sprite': 'grass'},
            '#': {'sprite': 'stone'},
            '~': {'sprite': 'water_light'},
            'D': {'sprite': 'door'},
            'w': {'sprite': 'window'},
            'o': {
                'sprite': 'water_light',
                'id': 'over_moat',
            },
            'e': {'sprite': 'grass', 'id': 'castle_courtyard_entrance'},
            '^': left_moat,
            '>': right_moat,
            's': {'id': 'castle_secret'}
        }
    },
    {  # Moat
        'data': [
            '**#2-#**',
            '**#__#**',
            '**#__#**',
            '**#1_#**',
        ],
        'wrap_mode': 'looped',
        'legend': {
            '*': lambda: dict(nogo('lava'), **{
                'type': 'wall',
            }),
            '#': {'sprite': 'stone'},
            '_': {'sprite': 'wood'},
            '1': {
                'id': 'fake_bridge',
                'sprite': 'wood'
            },
            '2': {
                'id': 'fake_bridge_end',
                'sprite': 'wood',
                'stitches': {
                    'up': 'fake_bridge//r'
                }
            },
            '-': {
                'stitches': {
                    'up': 'fake_bridge/r/r'
                },
                'sprite': 'wood'
            },
        }
    },
    {  # Inside the castle
        'data': [
            '################',
            '#______________#',
            '#______________#',
            '#______________#',
            '#______________#',
            '#######__#######',
            '#e___#____#____#',
            '#______________#',
            '#____#____#____#',
            '#######__#######',
            '~~~~~~#ww#~~~~~~',
            '~~~~~~#ww#~~~~~~',
            '~~~~~~#ww#~~~~~~',
            '~~~~~~#c2#~~~~~~',
        ],
        'legend': {
            'c': {
                'sprite': 'wood',
                'id': 'inside_castle',
                'stitches': {
                    'down': 'over_moat/dd'
                }
            },
            '2': {
                'sprite': 'wood',
                'stitches': {
                    'down': 'over_moat/ddr'
                }
            },
            'e': {
                'id': 'castle_tower_entrance',
                'sprite': 'cobble'
            },
            'w': {'sprite': 'wood'},
            '~': {'sprite': 'water_light'},
            '#': {'sprite': 'stone'},
            '_': {'sprite': 'cobble'},
        }
    },
    {  # Tower
        'data': [
            '*******',
            '*#*#*#*',
            '*#####*',
            '*#_o_#*',
            '*#__##*',
            '*##o_#*',
            '*#__##*',
            '*##o_#*',
            '*#__##*',
            '*#-v-#*',
        ],
        'legend': {
            '#': {'sprite': 'stone'},
            '_': {'sprite': 'cobble'},
            '*': {'sprite': 'sky'},
            'o': {'sprite': 'window'},
            'v': {
                'sprite': 'cobble',
                'id': 'tower_to_castle',
                'stitches': {
                    'down': 'castle_tower_entrance//r'
                }
            },
            '-': {
                'type': 'portal_extender',
                'base_id': 'tower_to_castle',
                'sprite': 'cobble',
                'reciprocal': True
            }
        }
    }
]
