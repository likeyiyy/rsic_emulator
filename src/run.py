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

from src.constants import DEFAULT_MEMORY_SIZE
from src.cpu import CPU
from src.keyboards import KeyBoard
from src.memory import Memory
import time, threading

from src.screen import Screen

if __name__ == "__main__":
    import curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # 内存初始化
    memory = Memory(DEFAULT_MEMORY_SIZE)  # 16MB

    # 键盘初始化
    keyboard = KeyBoard(stdscr)

    # 显示器初始化
    screen = Screen(stdscr)

    cpu = CPU()

    cpu.attach_memory(memory)
    cpu.attach_keyboard(keyboard)
    cpu.attach_screen(screen)

    keyboard_thread = threading.Thread(target=keyboard.run, name='KeyBoard-LoopThread')
    screen_thread = threading.Thread(target=screen.run, name='Screen-LoopThread')
    keyboard_thread.start()
    screen_thread.start()
    cpu.run()
    screen_thread.join()
    keyboard_thread.join()



