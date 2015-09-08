import uuid


def rill_origin():
    rider_id = uuid.uuid4().hex
    return {
        'sprite': 'water_light',
        'type': 'rill_origin',
        'also': [
            {
                'id': rider_id,
                'sprite': 'fire',
                'type': 'rill_rider',
                'song': 'tut bo boro'
            },
            lambda: lurker('alligator', rider_id, 'bobo')]
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
                            'sprite': 'necromancy',
                            'song': 'tut po ropo',
                            'stitches': {
                                # 'right': '%s_resetter//r' % ground_id
                                'right': '%s_body//r' % ground_id
                            }
                        },
                        {
                            'id': 'body',  # Body
                            'sprite': 'fire',
                            'song': 'tut po popo',
                            'stitches': {
                                'right': '%s_resetter//r' % ground_id,
                                'up': '%s_butt//r' % ground_id,
                            }
                        },
                        # {
                            # 'id': 'body2',
                            # 'sprite': 'transmutation',
                            # 'song': 'tut ro popo',
                            # 'tick_speed': .5,
                            # 'stitches': {
                                # 'down': '%s_body//r' % ground_id,
                                # 'up': '%s_butt//r' % ground_id
                            # }
                        # },
                        {
                            'id': 'butt',
                            'sprite': 'purple',
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
            'l': lurker('spriggan_m', 'player', 'wo', absolute_lurker_id=True)
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
            '#': {'type': 'wall', 'sprite': 'stone'},
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
            '~~~~o~~~~~~~~o~r~~~~~~~~~~',
            '~___r____f___r_r_________~',
            '~e__r________r_r_rrrrrr__~',
            '~___rrrrr_rrrr_rrr____r__~',
            '~_______r_r______#=P=#r__~',
            '~__rrrr_r_rrrr___|###/r__~',
            '~__r__rrr____r___R###Gr__~',
            '~_rr_____rrrrr___|###/rr_~',
            '~_r_rrrr_r_______#-B-#_r_~',
            '~_rrr__r_r_rrr_rrr____rr_~',
            '~______r_r_r_r_r_r___rr__~',
            'rrrrrrrr_rrr_r_r_r__rr___~',
            '~~~~~~~~~~~~~r~r~o~~o~~~~~',
        ],
        'legend': {
            '~': {'sprite': 'water_light'},
            'r': {'sprite': 'water_light', 'type': 'rill'},
            'o': rill_origin,
            '_': {'sprite': 'grass'},
            'f': mushroom_pocket,
            'e': {'id': 'flower_entrance', 'sprite': 'grass'},
            'R': {
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
            'B': {
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
            '########______########',
            '|rr#####______#####gg/',
            'Rrrrrrrr__t___gggggggG',
            '|rr#####______#####gg/',
            '########______########',
            '###########bbbbbbbb###',
            '###########b######bbb#',
            '###########b##bbbb##b#',
            '##########bbb#b#####b#',
            '##########bbb#bbbbbbb#',
            '##########-B-#########',
        ],
        'legend': {
            '_': {
                'sprite': 'cobble'
            },
            '#': {
                'sprite': 'void',
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
                'sprite': 'cobble',
                'type': 'teleporter',
                'to_id': 'triangle'
            }
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
    }
]
