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

import time
from curses.textpad import rectangle
from typing import Dict, List, Tuple, Type, Union, Callable, Optional

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_REFRESH_FREQ


class Screen(object):

    def __init__(self, stdscr):
        self.stdscr = stdscr
        rectangle(stdscr, uly=1, ulx=0, lry=1 + SCREEN_HEIGHT + 1, lrx=1 + SCREEN_WIDTH + 1)
        stdscr.refresh()
        self.init_y = 2
        self.init_x = 1
        self.get_memory = None

    def init_get_memory_handler(self, get_memory: Callable):
        self.get_memory = get_memory

    def run(self):
        self.stdscr.addstr(1, 0, "显示器始化好了！")
        assert self.get_memory is not None
        while True:
            time.sleep(1.0 / SCREEN_REFRESH_FREQ)
            buffers = self.get_memory()
            for y in range(0, SCREEN_HEIGHT):
                for x in range(0, SCREEN_WIDTH):
                    ascii_code = buffers[(y * SCREEN_WIDTH) + x]
                    if ascii_code == 0:
                        ascii_code = 32
                    self.stdscr.addch(self.init_y + y, self.init_x + x, chr(ascii_code))