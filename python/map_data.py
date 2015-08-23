import uuid


def alta(to_id, id=None):
    return {
        'id': id or uuid.uuid4().hex,
        'type': 'alta',
        'to_id': to_id
    }


def teleporter(id, to_id, sprite='arch'):
    return {
        'id': id or uuid.uuid4().hex,
        'type': 'teleporter',
        'to_id': to_id,
        'sprite': sprite
    }

pocket_dimension = {
    'data': [
        '#___######',
        '_#_#_#___#',
        '__#__#___#',
        '_#_#_#___#',
        '#___######',
        '######___#',
        '#___#_#_#_',
        '#___#__#__',
        '#___#_#_#_',
        '######___#',
    ],
    'wrap_mode': 'pocket',
    'sprites': {
        '_': 'cobble',
        '#': 'brick',
        'default': 'altar'
    }
}

flower_dimension = {
    'data': [
        '#####',
        '#___#',
        '#___#',
        '#___#',
        '##_##',
        '##_##',
        '##_##',
        '##_##',
    ],
    'legend': {
        '_': {'sprite': 'bog'},
        '#': {'sprite': 'slime'},
    },
    'exits': 'd'
}


maps = [
    {
        'data': ['v'],
        'legend': {
            'v': {
                'id': 'void',
                'sprite': 'void'
            }
        },
        'wrap_mode': 'loop'
    },
    {
        'data': [
            "########################",
            "########################",
            "########################",
            "####____________########",
            "####____q_________v#####",
            "####____________########",
            "####____________########",
            "########__##############",
            "########__##############",
            "########__##############",
            "########__f#############",
            "########__##############",
            "########__##############",
            "########__##############",
            "###___________##########",
            "###_____X_____#####___##",
            "##b_________________p_##",
            "###___________#####___##",
            "###___________##########",
            "########d###############",
            "########################",
        ],
        'legend': {
            'b': {
                'type': 'teleporter',
                'id': 'boogie',
                'to_id': 'apple'
            },
            # '#': {'type': 'wall'},
            'X': {'id': 'start'},
            'd': teleporter('dookie', 'maze_entrance'),
            'q': teleporter('boob', 'zoomie'),
            'p': {
                'id': 'pocky',
                'type': 'pocket',
                'dimension': pocket_dimension
            },
            'v': teleporter('vovo', 'void'),
            'f': teleporter('to_flower', 'flower_entrance')
        }
    },
    {
        'data': [
            "##################",
            "###_o_oro_o_o_o###",
            "#b______________a#",
            "###_o_o_o_o_o_o###",
            "##################",
        ],
        'legend': {
            'a': {
                'type': 'teleporter',
                'id': 'apple',
                'to_id': 'boogie'
            },
            'b': {
                'type': 'teleporter',
                'id': 'aggie',
                'to_id': 'hallway_right'
            },
            'r': {
                'type': 'teleporter',
                'id': 'rubbie',
                'to_id': '1'
            }
        },
        'sprites': {
            '#': 'brick',
            '_': 'cobble',
            'o': 'altar',
            'default': 'bog'
        }
    },
    {
        'data': [
            "###################",
            "###o_o_o_o_o_o_o###",
            "#b_______________a#",
            "###o_o_o_o_o_o_o###",
            "###################",
        ],
        'legend': {
            'a': {
                'type': 'teleporter',
                'id': 'hallway_right',
                'to_id': 'aggie'
            },
            'b': {
                'type': 'teleporter',
                'id': 'hallway_left',
                'to_id': 'hallway_right'
            },
            'o': {
                'sprite': 'altar',
                'song': 'tut po pogo'
            }
        },
        'sprites': {
            '#': 'brick',
            '_': 'cobble',
            'default': 'bog'
        }
    },
    {
        'data': [
            '1234567890',
        ],
        'legend': {
            '1': alta('2', '1'),
            '2': alta('3', '2'),
            '3': alta('4', '3'),
            '4': alta('5', '4'),
            '5': alta('6', '5'),
            '6': alta('7', '6'),
            '7': alta('8', '7'),
            '8': alta('9', '8'),
            '9': alta('0', '9'),
            '0': alta('rubbie', '0'),
        }
    },
    {
        'data': [
            'c####>',
            '<____>',
            '<____>',
            '<_b__>',
            '<____>',
            '<____>',
        ],
        'legend': {
            'b': teleporter('zoomie', 'boob'),
            '>': {
                'sprite': 'brick',
                'type': 'stitched',
                'stitches': {
                    'right': 'ruu'
                },
                'song': 'tut ro robo'
            },
            '<': {
                'sprite': 'cobble',
                'type': 'stitched',
                'stitches': {
                    'left': 'ldd'
                },
                'song': 'tut go gopo'
            },
            'c': {
                'sprite': 'brick',
                'type': 'stitched',
                'stitches': {
                    'left': 'ldd'
                },
                'song': 'tut go gopo'
            }
        },
        'wrap_mode': 'wrap',
        'sprites': {
            '_': 'cobble',
            '#': 'brick',
            'default': 'cobble'
        }
    },
    {
        'data': [
            '~~~~~~~~~~~~~~~~',
            '~~~~~~~~~~~~~~~~',
            '~_f_f__f______f~',
            '~e_________f___~',
            '~______________~',
            '~~~~~~~~~~~~~~~~',
        ],
        'legend': {
            '~': {'sprite': 'water_light'},
            '_': {'sprite': 'grass'},
            'f': {
                'type': 'pocket',
                'dimension': flower_dimension,
                'entrances': 'u',
                'sprite': 'hungry_ghost',
                'innie': True
            },
            'e': {'id': 'flower_entrance', 'sprite': 'grass'}
        }
    },
    {
        'data': [
            'vvvvvvvvvv',
            'vcvv_____v',
            'v_vv_vv_vv',
            'v_vv_vv_vv',
            'v_vv_vvvvv',
            'v_vv_____v',
            'v_vvvovv_v',
            'v_vvvvvv_v',
            'v________v',
            'vvvvvvvvvv',
        ],
        'legend': {
            'c': {
                'id': 'maze_entrance',
                'sprite': 'cobble'
            },
            '_': {'sprite': 'cobble'},
            '#': {'sprite': 'brick', 'type': 'wall'},
            '>': {
                'sprite': 'brick',
                'type': 'stitched',
                'stitches': {
                    'right': 's'
                }
            },
            '^': {
                'sprite': 'brick',
                'type': 'stitched',
                'stitches': {
                    'up': 's'
                }
            },
            'o': teleporter('maze_exit', 'start'),
            'v': {
                'type': 'teleporter',
                'to_id': 'void',
                'sprite': 'void'
            }
        }
    }
]
