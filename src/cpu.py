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

from src.keyboards import KeyBoard
from src.memory import Memory
from src.screen import Screen

KEY_BOARD_INT_NUM = 16
KEY_MMAP_ADDR = 0xb8d70


class CPU(object):

    def __init__(self):
        self.PSW = 0
        self.memory = None
        self.keyboard = None
        self.screen = None

    def attach_memory(self, memory: Memory):
        self.memory = memory

    def set_keyboard_memory(self, key_code: int):
        """
        暂时不设置缓冲区深度了。
        :param key_code: key的ascii码
        :return:
        """
        self.memory.write8(KEY_MMAP_ADDR, key_code)

    def set_keyboard_interrupt_flag(self):
        self.PSW |= 0b100 # 设置中断标志
        low_16_bit = self.PSW & 0xffff  # 设置中断号
        high_8_bit = self.PSW & 0xff000000
        self.PSW = high_8_bit << 24 | KEY_BOARD_INT_NUM << 16 | low_16_bit

    def attach_keyboard(self, keyboard: KeyBoard) -> KeyBoard:
        self.keyboard = keyboard
        self.keyboard.init_set_memory_handler(self.set_keyboard_memory)
        self.keyboard.init_set_cpu_interrupt_flag(self.set_keyboard_interrupt_flag)
        return self.keyboard

    def attach_screen(self, screen: Screen):
        self.screen = screen

    def run(self):
        print("CPU RUNNING")
        while True:
            intrrupt_flag = (self.PSW & 0b100) >> 2
            if intrrupt_flag:
                print(self.memory.read8(KEY_MMAP_ADDR))
                low_2_bit = self.PSW & 0b11
                self.PSW = ((self.PSW >> 3) << 3) | low_2_bit