import uuid


def rill_origin():
    rider_id = uuid.uuid4().hex
    return {
        'sprite': 'rill_origin',
        'type': 'rill_origin',
        'also': [
            {
                'id': rider_id,
                'sprite': 'rider_onto',
                'type': 'rill_rider',
                'song': 'tut bo boro'
            },
            lambda: lurker('rill_rider', rider_id, 'bobo')],
        'innie': True,
        'dimension': {
            'data': [
                'vvvvv',
                'v###v',
                'v#>#v',
                'v###v',
                'vvvvv',
            ],
            'wrap_mode': 'bounded',
            'exits': '',
            'legend': {
                '#': {'sprite': 'stone'},
                '_': {'sprite': 'water_dark'},
                '>': {
                    'sprite': 'water_dark',
                    'stitches': {
                        'right': '%s//r' % rider_id,
                        'left': '%s//r' % rider_id,
                        'up': '%s//r' % rider_id,
                        'down': '%s//r' % rider_id,
                    }
                },
                'v': {'sprite': 'darkness'}
            }
        },
    }


def lurker(sprite, watching_id, direction, reciprocate=True, absolute_lurker_id=False):
    return {
        'id': 'lurkroom_%s' % (watching_id if watching_id else uuid.uuid4().hex),
        'type': 'lurkroom',
        'sprite': 'void',
        'entrances': '',
        'dimension': {
            'data': [
                '###',
                '#lh',
                '#_#',
                '___',
            ],
            'exits': '',
            'wrap_mode': 'bounded',
            'legend': {
                '#': {'sprite': 'stone'},
                '_': {'sprite': 'cobble'},
                'l': {
                    'id': ('%s_lurker' % watching_id) if watching_id else uuid.uuid4().hex,
                    'absolute_id': absolute_lurker_id,
                    'type': 'lurker',
                    'sprite': sprite,
                    'song': 'ibi wowo ema tut wowo wo, ibi rorowo roro beh wo roro',
                    'tick_speed': 1.0 / 4,
                },
                'h': {
                    'sprite': 'glove',
                    'song': 'tut ro bo%s' % direction,
                    'stitches': {
                        'up': ('%s//%s' % (watching_id, 'r' if reciprocate else '')) if watching_id else '',
                    },
                    'tick_speed': 1.0 / 4,
                }
            }
        }
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
                '##_##',
                '##_##',
                '__d__',
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
                    'also': [
                        {
                            'id': 'beetle',  # Head
                            'sprite': 'head',
                            'song': 'tut po ropo',
                            'stitches': {
                                # 'right': '%s_resetter//r' % ground_id
                                'right': '%s_body//r' % ground_id
                            }
                        },
                        {
                            'id': 'body',  # Body
                            'sprite': 'foot',
                            'song': 'tut po popo',
                            'stitches': {
                                'right': '%s_resetter//r' % ground_id,
                                'up': '%s_butt//r' % ground_id,
                            }
                        },
                        {
                            'id': 'butt',
                            'sprite': 'butt',
                            'song': 'tut bo popo',
                            'stitches': {
                                'left': '%s_resetter//r' % ground_id
                            }
                        },
                        {
                            'id': 'resetter',
                            'sprite': 'glove',
                            'song': 'ibi gopo robo tut gopo bo',
                            'tick_speed': 2,
                            'stitches': {
                                'up': '%s_start/' % ground_id,
                            }
                        },
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
            lurker('mushroom_pink', inner_id, 'po', False)
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
        'data': [
            '_h_^',
            'apal',
            '_f__',
        ],
        'legend': {
            'p': {
                'id': 'player',
                'sprite': 'ophan',
                'stitches': {
                    'inner': 'start/',
                    # 'right': 'start/'
                }
            },
            'l': lurker('you', 'player', 'wo', reciprocate=False, absolute_lurker_id=True),
            '^': {
                'stitches': {
                    'up': 'start/',
                    'right': 'start/'
                }
            },
            'h': {'sprite': 'head'},
            'a': {'sprite': 'glove'},
            'f': {'sprite': 'foot'}
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
            "########__t#############",
            "########__##############",
            "###CT_______Tw##########",
            "###___HELLO___#####___##",
            "##b_________T_______p_##",
            "###_____X_____#####___##",
            "###_T_T___T__m##########",
            "########d###############",
            "########################",
        ],
        'legend': {
            '_': {'sprite': 'grass'},
            '#': {'type': 'wall', 'sprite': 'stone'},
            'b': {
                'type': 'teleporter',
                'id': 'boogie',
                'to_id': 'apple'
            },
            # '#': {'type': 'wall'},
            'C': {'type': 'teleporter', 'to_id': 'castle_courtyard_entrance'},
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
            't': teleporter(None, 'tree_entrance'),
            'w': teleporter(None, 'town_entrance'),
            'm': {'id': 'golden_rill_origin'}
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
            '_': {'sprite': 'cobble'},
            '#': {'sprite': 'brick'},
            'o': {'sprite': 'altar'},
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
                'sprite': 'void',
                'type': 'teleporter',
                'id': 'rubbie',
                'to_id': '1'
            },
        },
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
            'ABCDEFGHIJ',
        ],
        'legend': {
            'A': alta('2', '1'),
            'B': alta('3', '2'),
            'C': alta('4', '3'),
            'D': alta('5', '4'),
            'E': alta('6', '5'),
            'F': alta('7', '6'),
            'G': alta('8', '7'),
            'H': alta('9', '8'),
            'I': alta('0', '9'),
            'J': alta('rubbie', '0'),
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
            '#######################################',
            '#~~~~~~~~~o~~~~~o~~~~~~~~o~r~~~~~~~~~~#',
            '#~__THE___r_____r____f___r_r_________~#',
            '#~_rrrrrrrr_____r________r_r_rrrrrr__~#',
            '#~erSINUOUS_____rrrrr_rrrr_rrr____r__~#',
            '#~_rrrrrrr__________r_r______#=P=#r__~#',
            '#~__RILLSr_____rrrr_r_rrrr___|###/r__~#',
            '#~__rrrrrr_____r__rrr____r___1###Gr__~#',
            '#~__r_____rrr_rr_____rrrrr___|###/rr_~#',
            '#~__rrrrrrr_r_r_rrrr_r_______#-2-#_r_~#',
            '#~__________r_rrr__r_r_rrr_rrr____rr_~#',
            '#~__rrr_rrr_r______r_r_r_r_r_r___rr__~#',
            '#~__r_rrr_rrr_rrrrrr_rrr_r_r_r__rr___~#',
            '#~~~r~~~~~~~~~r~~~~~~~~~~r~r~o~~o~~~~~#',
            '#######################################',
        ],
        'wrap_mode': 'looped',
        'legend': {
            '#': {'sprite': 'grass'},
            '~': {'sprite': 'grass'},
            'r': {'sprite': 'water_light', 'type': 'rill'},
            'o': rill_origin,
            '_': {'sprite': 'grass'},
            'f': mushroom_pocket,
            'e': {'id': 'flower_entrance', 'sprite': 'grass'},
            '1': {
                'id': 'rill_red',
                'sprite': 'fire',
                'stitches': {
                    'right': 'red_room_entrance/'
                }
            },
            '|': {
                'sprite': 'fire',
                'type': 'portal_extender',
                'base_id': 'rill_red'
            },
            'G': {
                'id': 'rill_green',
                'sprite': 'poison',
                'stitches': {
                    'left': 'green_room_entrance/'
                }
            },
            '/': {
                'sprite': 'poison',
                'type': 'portal_extender',
                'base_id': 'rill_green',
            },
            '2': {
                'id': 'rill_blue',
                'sprite': 'ice',
                'stitches': {
                    'up': 'blue_room_entrance/'
                }
            },
            '-': {
                'sprite': 'ice',
                'type': 'portal_extender',
                'base_id': 'rill_blue'
            },
            'P': {
                'id': 'rill_purple',
                'sprite': 'purple',
                'stitches': {
                    'down': 'purple_room_entrance/'
                }
            },
            '=': {
                'sprite': 'purple',
                'type': 'portal_extender',
                'base_id': 'rill_purple'
            },
        }
    },
    {  # Within the rillstone
        'data': [
            '######################',
            '#########=P=##########',
            '#########ppp##########',
            '#########ppp##########',
            '##########p###########',
            '##########p###########',
            '##########p###########',
            '##########p###########',
            '##########_###########',
            '|rr######____######gg/',
            'Rrrrrrrr__t___gggggggG',
            '|rr#######___######gg/',
            '###########_##########',
            '###########b##########',
            '###########b##########',
            '###########b##########',
            '##########bbb#########',
            '##########bbb#########',
            '##########-B-#########',
        ],
        'legend': {
            '_': {
                'sprite': 'cobble'
            },
            '#': {
                'sprite': 'darkness',
                'type': 'wall'
            },
            'r': {'sprite': 'fire'},
            'R': {
                'id': 'red_room_entrance',
                'sprite': 'fire',
                'stitches': {
                    'left': 'rill_red/'
                }
            },
            '|': {
                'sprite': 'fire',
                'type': 'portal_extender',
                'base_id': 'red_room_entrance',
            },
            'g': {'sprite': 'poison'},
            'G': {
                'id': 'green_room_entrance',
                'sprite': 'poison',
                'stitches': {
                    'right': 'rill_green/'
                }
            },
            '/': {
                'sprite': 'poison',
                'type': 'portal_extender',
                'base_id': 'green_room_entrance',
            },
            'b': {'sprite': 'ice'},
            'B': {
                'id': 'blue_room_entrance',
                'sprite': 'ice',
                'stitches': {
                    'down': 'rill_blue/',
                }
            },
            '-': {
                'sprite': 'ice',
                'type': 'portal_extender',
                'base_id': 'blue_room_entrance'
            },
            'p': {'sprite': 'purple'},
            'P': {
                'id': 'purple_room_entrance',
                'sprite': 'purple',
                'stitches': {
                    'up': 'rill_purple/',
                }
            },
            '=': {
                'sprite': 'purple',
                'type': 'portal_extender',
                'base_id': 'purple_room_entrance'
            },
            't': {
                'sprite': 'boulder',
                'type': 'teleporter',
                'to_id': 'tree_entrance'
            },
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
    {
        'data': [
            '^^^^1',
            'e##2_',
            '##3__',
            '#4___',
            '5____',
        ],
        'wrap_mode': 'looped',
        'legend': {
            'e': {
                'id': 'triangle',
                'sprite': 'cobble'
            },
            '#': {
                'sprite': 'cobble'
            },
            '1': {'sprite': 'stone', 'stitches': {'down': '/ld/', 'up': 'triangle_bottom//r'}},
            '2': {'sprite': 'stone', 'stitches': {'right': '/lll/r', 'down': '/ld/'}},
            '3': {'sprite': 'stone', 'stitches': {'right': '/ll/r', 'down': '/ld/'}},
            '4': {'sprite': 'stone', 'stitches': {'right': '/l/r', 'down': '/ld/'}},
            '5': {'id': 'triangle_bottom', 'sprite': 'stone', 'stitches': {'right': '/s/r', 'down': '/ld/'}},
            '^': {
                'sprite': 'cobble',
                'stitches': {
                    'up': 'triangle_bottom/'
                }
            }
        }
    },
    {  # Player location memory place
        'data': [
            '>--|'
        ],
        'legend': {
            '>': {
                'stitches': {
                    'left': 'player/'
                },
                'song': 'bib gowo bo tut bo gowo'
            },
            '-': {
                'song': 'tut bo gobo'
            },
            '|': {
                'id': 'player_position_memory',
                'song': 'tut bo gobo'
            }
        }
    },
    {
        'data': [
            '_________',
            '_YOU_ARE_',
            '__@DEAD__',
            '_________',
        ],
        'legend': {
            '_': {'sprite': 'darkness'},
            '@': {'id': 'hell', 'sprite': 'darkness'}
        }
    }
]

from tree_place import data as tree_data
from gold_place import data as gold_data
from castle_place import data as castle_data
from town_place import data as town_data

maps.extend(tree_data)
maps.extend(gold_data)
maps.extend(castle_data)
maps.extend(town_data)
