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

from pynput.keyboard import Listener, Key


from src.key_board_mapping import KeyBoardMapping

if typing.TYPE_CHECKING:
    pass

MAPPING = {
    "BackSpace": "Back",
    "Shift_L": "LSHIFT",
    "Shift_R": "RSHIFT",
    "Control_L": "LCONTROL",
    "Control_R": "RCONTROL",
}


class KeyBoard(object):

    def __init__(self):
        self.set_memory = None
        self.set_cpu_interrupt_flag = None

    def init_set_memory_handler(self, set_memory: typing.Callable):
        self.set_memory = set_memory

    def init_set_cpu_interrupt_flag(self, set_cpu_interrupt_flag: typing.Callable):
        self.set_cpu_interrupt_flag = set_cpu_interrupt_flag

    def on_press(self, key):
        assert self.set_memory is not None, "Memory 没有初始化"
        assert self.set_cpu_interrupt_flag is not None, "CPU没有初始化"
        if isinstance(key, Key):
            symbol = MAPPING.get(key.value._symbol) or key.value._symbol
            symbol = symbol.upper()
            key = getattr(KeyBoardMapping, symbol, None)
        else:
            key = ord(key.char)
        if key:
            self.set_memory(key)
            self.set_cpu_interrupt_flag()

    def on_release(self, key):
        pass

    def run(self):
        print("KEYBOARD RUNING")
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    keyboard_ins = KeyBoard()
    keyboard_ins.run()
