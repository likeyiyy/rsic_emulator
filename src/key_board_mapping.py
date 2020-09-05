#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# code is far away from bugs with the god animal protect
# I love animals. They taste delicious.
#         ┌─┐       ┌─┐
#      ┌──┘ ┴───────┘ ┴──┐
#      │                 │
#      │       ───       │
#      │  ─┬┘       └┬─  │
#      │                 │
#      │       ─┴─       │
#      │                 │
#      └───┐         ┌───┘
#          │         │
#          │         │
#          │         │
#          │         └──────────────┐
#          │                        │
#          │      Gods Bless        ├─┐
#          │      Never Bugs        ┌─┘
#          │                        │
#          └─┐  ┐  ┌───────┬──┐  ┌──┘
#            │ ─┤ ─┤       │ ─┤ ─┤
#            └──┴──┘       └──┴──┘

from __future__ import absolute_import, annotations, print_function
from typing import Dict, List, Tuple, Type, Union, Callable, Optional

class KeyBoardMapping(object):
    LBUTTON = 1
    RBUTTON = 2
    CANCEL = 3
    MBUTTON = 4
    XBUTTON1 = 5
    XBUTTON2 = 6
    BACK = 8
    TAB = 9
    CLEAR = 12
    RETURN = 13
    SHIFT = 16
    CONTROL = 17
    MENU = 18
    PAUSE = 19
    CAPITAL = 20
    KANA = 21
    HANGEUL = 21
    HANGUL = 21
    JUNJA = 23
    FINAL = 24
    HANJA = 25
    KANJI = 25
    ESCAPE = 27
    CONVERT = 28
    NONCONVERT = 29
    ACCEPT = 30
    MODECHANGE = 31
    SPACE = 32
    PRIOR = 33
    NEXT = 34
    END = 35
    HOME = 36
    LEFT = 37
    UP = 38
    RIGHT = 39
    DOWN = 40
    SELECT = 41
    PRINT = 42
    EXECUTE = 43
    SNAPSHOT = 44
    INSERT = 45
    DELETE = 46
    HELP = 47
    LWIN = 91
    RWIN = 92
    APPS = 93
    SLEEP = 95
    NUMPAD0 = 96
    NUMPAD1 = 97
    NUMPAD2 = 98
    NUMPAD3 = 99
    NUMPAD4 = 100
    NUMPAD5 = 101
    NUMPAD6 = 102
    NUMPAD7 = 103
    NUMPAD8 = 104
    NUMPAD9 = 105
    MULTIPLY = 106
    ADD = 107
    SEPARATOR = 108
    SUBTRACT = 109
    DECIMAL = 110
    DIVIDE = 111
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    F13 = 124
    F14 = 125
    F15 = 126
    F16 = 127
    F17 = 128
    F18 = 129
    F19 = 130
    F20 = 131
    F21 = 132
    F22 = 133
    F23 = 134
    F24 = 135
    NUMLOCK = 144
    SCROLL = 145
    OEM_NEC_EQUAL = 146
    OEM_FJ_JISHO = 146
    OEM_FJ_MASSHOU = 147
    OEM_FJ_TOUROKU = 148
    OEM_FJ_LOYA = 149
    OEM_FJ_ROYA = 150
    LSHIFT = 160
    RSHIFT = 161
    LCONTROL = 162
    RCONTROL = 163
    LMENU = 164
    RMENU = 165
    BROWSER_BACK = 166
    BROWSER_FORWARD = 167
    BROWSER_REFRESH = 168
    BROWSER_STOP = 169
    BROWSER_SEARCH = 170
    BROWSER_FAVORITES = 171
    BROWSER_HOME = 172
    VOLUME_MUTE = 173
    VOLUME_DOWN = 174
    VOLUME_UP = 175
    MEDIA_NEXT_TRACK = 176
    MEDIA_PREV_TRACK = 177
    MEDIA_STOP = 178
    MEDIA_PLAY_PAUSE = 179
    LAUNCH_MAIL = 180
    LAUNCH_MEDIA_SELECT = 181
    LAUNCH_APP1 = 182
    LAUNCH_APP2 = 183
    OEM_1 = 186
    OEM_PLUS = 187
    OEM_COMMA = 188
    OEM_MINUS = 189
    OEM_PERIOD = 190
    OEM_2 = 191
    OEM_3 = 192
    OEM_4 = 219
    OEM_5 = 220
    OEM_6 = 221
    OEM_7 = 222
    OEM_8 = 223
    OEM_AX = 225
    OEM_102 = 226
    ICO_HELP = 227
    ICO_00 = 228
    PROCESSKEY = 229
    ICO_CLEAR = 230
    PACKET = 231
    OEM_RESET = 233
    OEM_JUMP = 234
    OEM_PA1 = 235
    OEM_PA2 = 236
    OEM_PA3 = 237
    OEM_WSCTRL = 238
    OEM_CUSEL = 239
    OEM_ATTN = 240
    OEM_FINISH = 241
    OEM_COPY = 242
    OEM_AUTO = 243
    OEM_ENLW = 244
    OEM_BACKTAB = 245
    ATTN = 246
    CRSEL = 247
    EXSEL = 248
    EREOF = 249
    PLAY = 250
    ZOOM = 251
    NONAME = 252
    PA1 = 253
    OEM_CLEAR = 254
