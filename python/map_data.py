import uuid


def lurker(sprite, watching_id, direction):
    return {
        'id': '%s_lurker' % watching_id,
        'sprite': sprite,
        'stitches': {
            'right': '%s//r' % watching_id,
        },
        'song': 'ibi wowo ema tut wowo wo, beh wo ro%s' % direction
    }


def color_changer():
    ground_id = uuid.uuid4().hex
    # inner_id = uuid.uuid4().hex

    return {
        'id': ground_id,
        'type': 'pocket',
        'dimension': {
            'data': [
                'S____w',
                'e_____',
            ],
            'legend': {
                'S': {
                    'stitches': {
                        'left': '%s/' % ground_id,
                    },
                    'song': 'tut gowo popo'
                },
                'w': {
                    'stitches': {
                        'down': '%s_eye/' % ground_id
                    },
                    'song': 'tut popo poporo, tut po poro'
                },
                '_': {
                    'sprite': 'void',
                    'stitches': {
                        'down': 's'
                    }
                },
                'e': {
                    'id': 'eye',
                    'stitches': {
                        'down': 'transmutation/',
                    }
                }
            },
            'exits': '',
            'wrap_mode': 'looped'
        },
        'sprite': 'grass',
        'entrances': '',
        'innie': False,
    }


def mushroom_pocket():
    ground_id = uuid.uuid4().hex
    inner_id = uuid.uuid4().hex
    return {
        'id': ground_id,
        'type': 'pocket',
        'dimension': {
            'data': [
                '#####',
                '#_d_#',
                '#___#',
                '#___#',
                '##_##',
                '##_##',
                '##_##',
                'vvevv',
            ],
            'legend': {
                '_': {'sprite': 'bog'},
                '#': {'sprite': 'slime'},
                'v': {
                    'sprite': 'slime',
                    'stitches': {
                        'down': '%s/' % inner_id
                    }
                },
                'e': {
                    'id': 'entrance',
                    'sprite': 'bog',
                    'stitches': {
                        'down': '%s/' % inner_id
                    }
                },
                'd': {
                    'id': 'start',
                    'sprite': 'bog',
                    'also': [{
                        'id': 'beetle',
                        'sprite': 'necromancy',
                        'song': 'ibi popo po tut po bo, tut po popo',
                        'stitches': {
                            'down': '%s_start/' % (ground_id),
                            'up': '%s_start/' % ground_id
                        }},
                        lurker('beetle', '%s_beetle' % ground_id, 'po')
                    ],
                    'stitches': {
                        'up': '%s_beetle/' % ground_id
                    }
                }
            },
            'exits': 'd'
        },
        'sprite': 'grass',
        'entrances': 'u',
        'innie': True,
        'also': [{
            'id': inner_id,
            'sprite': 'mushroom_pink',
            'stitches': {
                'down': '%s/' % ground_id,
                'up': '%s_entrance/' % (ground_id),
            }},
            lurker('mushroom_pink', inner_id, 'po')
        ],
        'stitches': {
            'up': '%s//c' % inner_id,
            'inner': '%s/' % inner_id
        }
    }


def tree():
    ground_id = uuid.uuid4().hex
    tree_id = uuid.uuid4().hex
    return {
        'id': ground_id,
        'sprite': 'grass',
        'also': [{
            'id': tree_id,
            'sprite': 'tree',
            'stitches': {
                'inner': '%s/' % ground_id
            }
        }],
        'stitches': {
            'inner': '%s/' % tree_id
        }
    }


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

maps = [
    {
        'data': ['pl'],
        'legend': {
            'p': {
                'id': 'player',
                'sprite': 'ophan',
                'stitches': {
                    'inner': 'start/',
                    'right': 'start/'
                }
            },
            'l': lurker('spriggan_m', 'player', 'wo')
        }
    },
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
            "####_c_c_c_c____########",
            "####c___q___c_____v#####",
            "####_c_c_c_c____########",
            "####____________########",
            "########__##############",
            "########__##############",
            "########__##############",
            "########__f#############",
            "########__##############",
            "########__##############",
            "########__##############",
            "###_T_______T_##########",
            "###_____X_____#####___##",
            "##b_________T_______p_##",
            "###___________#####___##",
            "###_T_T___T___##########",
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
            'f': teleporter('to_flower', 'flower_entrance'),
            'T': tree,
            'c': color_changer,
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
            '<___w>',
            '<____>',
        ],
        'legend': {
            'b': teleporter('zoomie', 'boob'),
            '>': {
                'sprite': 'brick',
                'stitches': {
                    'right': 'ruu'
                },
                'song': 'tut ro robo'
            },
            '<': {
                'sprite': 'cobble',
                'stitches': {
                    'left': 'ldd'
                },
                'song': 'tut go gopo'
            },
            'c': {
                'sprite': 'brick',
                'stitches': {
                    'left': 'ldd'
                },
                'song': 'tut go gopo'
            },
            'w': {
                'id': 'wanderer',
                'sprite': 'cobble'
            }
        },
        'wrap_mode': 'wrap',
        'sprites': {
            '_': 'cobble',
            '#': 'brick',
            'default': 'cobble'
        }
    },
    {  # Sinuous rills
        'data': [
            '~~~~o~~~~~~~~o~~',
            '~___r____f___r_~',
            '~e__r________r_~',
            '~___rrrrr_rrrr_~',
            '~_______r_r____~',
            '~__rrrr_r_rrrr_~',
            '~__r__rrr____r_~',
            '~_rr_____rrrrr_~',
            '~_r_rrrr_r_____~',
            '~_rrr__r_r_rrr_~',
            '~______r_r_r_r_~',
            'rrrrrrrr_rrr_r_~',
            '~~~~~~~~~~~~~r~~',
        ],
        'legend': {
            '~': {'sprite': 'water_light'},
            'r': {'sprite': 'water_light', 'type': 'rill'},
            'o': {'sprite': 'water_light', 'type': 'rill_origin'},
            '_': {'sprite': 'grass'},
            'f': mushroom_pocket,
            'e': {'id': 'flower_entrance', 'sprite': 'grass'}
        }
    },
    {
        'data': [
            'vvvvvvvvvv',
            'vcvv_____v',
            'v_vv_vv_vv',
            'v_vv_vvrvv',
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
                'stitches': {
                    'right': 's'
                }
            },
            '^': {
                'sprite': 'brick',
                'stitches': {
                    'up': 's'
                }
            },
            'o': teleporter('maze_exit', 'start'),
            'v': {
                'type': 'alta',
                'to_id': 'void',
            },
            'r': teleporter('to_colors', 'transmutation')
        }
    }, {
        'data': [
            '___',
            '_@_',
            '___',
        ],
        'legend': {
            '@': {
                'sprite': 'hungry_ghost',
                'stitches': {
                    'inner': 'wanderer/'
                },
                'song': 'tut wowo wo, beh wo woro'
            },
            '_': {
                'sprite': 'water_dark'
            }
        }
    },
    {  # Where the colors live
        'data': [
            '1234567890ab'
        ],
        'legend': {
            k: {'id': v, 'sprite': v, 'stitches': {'up': 'ur', 'down': 'dl'}} for (k, v) in zip('1234567890ab', ['transmutation', 'translocation', 'summoning', 'poison', 'necromancy', 'ice', 'fire', 'enchantment', 'earth', 'conjuration', 'divination', 'air'])
        },
        'wrap_mode': 'looped'
    },
]
