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

import typing


class KeyBoard(object):

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.set_memory = None
        self.set_cpu_interrupt_flag = None

    def init_set_memory_handler(self, set_memory: typing.Callable):
        self.set_memory = set_memory

    def init_set_cpu_interrupt_flag(self, set_cpu_interrupt_flag: typing.Callable):
        self.set_cpu_interrupt_flag = set_cpu_interrupt_flag

    def on_press(self, key):
        assert self.set_memory is not None, "Memory 没有初始化"
        assert self.set_cpu_interrupt_flag is not None, "CPU没有初始化"
        self.set_memory(key)
        self.set_cpu_interrupt_flag()

    def run(self):
        self.stdscr.addstr(0, 0, "键盘初始化好了！")
        while True:
            key_code = self.stdscr.getch()
            self.on_press(key_code)


if __name__ == "__main__":
    import curses
    stdscr = curses.initscr()
    keyboard_ins = KeyBoard(stdscr)
    keyboard_ins.run()
