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

from src.cpu import CPU
from src.keyboards import KeyBoard
from src.memory import Memory
import time, threading

if __name__ == "__main__":
    memory = Memory(16)  # 16MB
    keyboard = KeyBoard()
    cpu = CPU()

    cpu.attach_memory(memory)
    cpu.attach_keyboard(keyboard)
    t = threading.Thread(target=keyboard.run, name='LoopThread')
    t.start()
    cpu.run()
    t.join()



