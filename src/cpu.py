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

from src.constants import KEY_MMAP_ADDR, KEY_BOARD_INT_NUM, SCREEN_MMAP_ADDR
from src.keyboards import KeyBoard
from src.memory import Memory
from src.opcode import OPCode
from src.screen import Screen
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class CPU(object):

    def __init__(self):
        self.PC = 0x7C00
        self.BP = 0x0
        self.SP = 0x0
        self.PSW = 0
        self.IDTR = 0x0
        self.CR3 = 0x0
        self.CR2 = 0x0
        self.CR0 = 0x0
        self.regs = [0] * 32
        self.f_regs = [0.0] * 4
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

    def read_keyboard(self):
        return self.memory.read8(KEY_MMAP_ADDR)

    def get_screen_memory(self):
        result = []
        for y in range(0, SCREEN_HEIGHT):
            for x in range(0, SCREEN_WIDTH):
                result.append(self.memory.read8(SCREEN_MMAP_ADDR + (y * SCREEN_WIDTH) + x))
        return result

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
        self.screen.init_get_memory_handler(self.get_screen_memory)
        return self.screen

    def cli(self):
        low_2_bit = self.PSW & 0b11
        self.PSW = ((self.PSW >> 3) << 3) | low_2_bit

    @property
    def is_enable_protection(self):
        return self.CR0 & 0b1

    def fetch(self):
        if self.is_enable_protection:
            # 保护模式待实现
            ...
        else:
            instruction = self.memory.read32(self.PC)
            self.PC += 4
            return instruction

    def run(self):
        y = 0
        x = 0
        while True:
            instruction = self.fetch()
            op_code = instruction >> 24
            RS_INDEX = (instruction & 0x0fffffff) >> 19
            RT_INDEX = (instruction & 0x07ffffff) >> 14
            RD_INDEX = (instruction & 0x003fffff) >> 9
            if op_code == OPCode.ADD:
                self.regs[RD_INDEX] = self.regs[RS_INDEX] + self.regs[RT_INDEX]
            elif op_code == OPCode.SUB:
                self.regs[RD_INDEX] = self.regs[RS_INDEX] - self.regs[RT_INDEX]
            elif op_code == OPCode.MUL:
                self.regs[RD_INDEX] = self.regs[RS_INDEX] * self.regs[RT_INDEX]
            elif op_code == OPCode.DIV:
                self.regs[RD_INDEX] = int(self.regs[RS_INDEX] / self.regs[RT_INDEX])
            elif op_code == OPCode.DIV:
                _, self.regs[RD_INDEX] = divmod(self.regs[RS_INDEX], self.regs[RT_INDEX])

            intrrupt_flag = (self.PSW & 0b100) >> 2
            if intrrupt_flag:
                ascii_code = self.read_keyboard()
                self.memory.write8(SCREEN_MMAP_ADDR + (y * SCREEN_WIDTH) + x, ascii_code)
                x += 1
                if x >= SCREEN_WIDTH:
                    x = 0
                    y += 1
                    if y >= SCREEN_HEIGHT:
                        y = 0
                self.cli()
