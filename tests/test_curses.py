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

import curses
from curses.textpad import Textbox, rectangle


def main():
    import curses
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.addstr(0, 0, "CPU, 键盘，显示缓存，都初始化好了")
    rectangle(stdscr, uly=1, ulx=0, lry=1 + 25 + 1, lrx=1 + 80 + 1)
    stdscr.refresh()
    y = 2
    x = 1
    while True:
        key_code = stdscr.getch()
        stdscr.addch(y, x, key_code)
        x += 1
        if x > 80:
            x = x % 80
            y += 1


if __name__ == "__main__":

    main()