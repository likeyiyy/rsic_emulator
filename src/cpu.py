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
        self.CR1 = 0x0
        self.CR0 = 0x0
        self.regs = [0] * 32
        self.f_regs = [0.0] * 4
        self.memory = None
        self.keyboard = None
        self.screen = None

    def attach_memory(self, memory: Memory):
        self.memory = memory
        self.SP = self.memory.size - 4
        self.BP = self.SP

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

    def enter_interrupt(self, int_num: int):
        # push PWS
        self.SP -= 4
        self.memory.write32(self.SP, self.PSW)
        # push pc
        self.SP -= 4
        self.memory.write32(self.SP, self.PC)
        self.PC = self.IDTR + int_num * 4

    def run(self):
        while True:
            instruction = self.fetch()
            op_code = instruction >> 24
            RS_INDEX = (instruction & 0x0fffffff) >> 19
            RT_INDEX = (instruction & 0x07ffffff) >> 14
            RD_INDEX = (instruction & 0x003fffff) >> 9
            JUMP_LABEL = instruction & 0b11_1111_1111_1111

            if op_code in (OPCode.ADD, ):
                self.regs[RD_INDEX] = self.regs[RS_INDEX] + self.regs[RT_INDEX]
            elif op_code in (OPCode.SUB, ):
                self.regs[RD_INDEX] = self.regs[RS_INDEX] - self.regs[RT_INDEX]
            elif op_code in (OPCode.MUL, ):
                self.regs[RD_INDEX] = self.regs[RS_INDEX] * self.regs[RT_INDEX]
            elif op_code in (OPCode.DIV, ):
                self.regs[RD_INDEX] = int(self.regs[RS_INDEX] / self.regs[RT_INDEX])
            elif op_code == OPCode.MOD:
                _, self.regs[RD_INDEX] = divmod(self.regs[RS_INDEX], self.regs[RT_INDEX])
            elif op_code in (OPCode.ADD, OPCode.FADD):
                self.f_regs[RD_INDEX] = self.f_regs[RS_INDEX] + self.f_regs[RT_INDEX]
            elif op_code in (OPCode.SUB, OPCode.FSUB):
                self.f_regs[RD_INDEX] = self.f_regs[RS_INDEX] - self.f_regs[RT_INDEX]
            elif op_code in (OPCode.MUL, OPCode.FMUL):
                self.f_regs[RD_INDEX] = self.f_regs[RS_INDEX] * self.f_regs[RT_INDEX]
            elif op_code in (OPCode.DIV, OPCode.FDIV):
                self.f_regs[RD_INDEX] = int(self.f_regs[RS_INDEX] / self.f_regs[RT_INDEX])

            elif op_code == OPCode.AND:
                self.regs[RD_INDEX] = self.regs[RS_INDEX] & self.regs[RT_INDEX]
            elif op_code == OPCode.OR:
                self.regs[RD_INDEX] = self.regs[RS_INDEX] | self.regs[RT_INDEX]
            elif op_code == OPCode.NOT:
                self.regs[RT_INDEX] = ~self.regs[RS_INDEX]
            elif op_code == OPCode.SLL:
                self.regs[RD_INDEX] = self.regs[RS_INDEX] << self.regs[RT_INDEX]
            elif op_code == OPCode.SLR:
                self.regs[RD_INDEX] = self.regs[RS_INDEX] >> self.regs[RT_INDEX]

            elif op_code == OPCode.LT:
                if self.regs[RS_INDEX] < self.regs[RT_INDEX]:
                    self.PC = JUMP_LABEL
            elif op_code == OPCode.GT:
                if self.regs[RS_INDEX] > self.regs[RT_INDEX]:
                    self.PC = JUMP_LABEL
            elif op_code == OPCode.LTE:
                if self.regs[RS_INDEX] <= self.regs[RT_INDEX]:
                    self.PC = JUMP_LABEL

            elif op_code == OPCode.GTE:
                if self.regs[RS_INDEX] >= self.regs[RT_INDEX]:
                    self.PC = JUMP_LABEL

            elif op_code == OPCode.EQ:
                if self.regs[RS_INDEX] == self.regs[RT_INDEX]:
                    self.PC = JUMP_LABEL

            elif op_code == OPCode.NEQ:
                if self.regs[RS_INDEX] != self.regs[RT_INDEX]:
                    self.PC = JUMP_LABEL

            elif op_code == OPCode.JMP:
                self.PC = self.regs[RS_INDEX]

            elif op_code == OPCode.JMPI:
                JMPI_LABEL = instruction & 0x0fffffff
                self.PC = JMPI_LABEL

            elif op_code == OPCode.MOV:
                self.regs[RT_INDEX] = self.regs[RS_INDEX]
            elif op_code == OPCode.LOAD:
                self.regs[RT_INDEX] = self.memory.read8(self.regs[RS_INDEX])
            elif op_code == OPCode.STORE:
                self.memory.write8(self.regs[RT_INDEX], self.regs[RS_INDEX])
            elif op_code == OPCode.LUI:
                imm_num = instruction & 0xffff
                self.regs[RS_INDEX] = imm_num

            elif op_code == OPCode.CALL:
                self.SP -= 4
                self.memory.write32(self.SP, self.PC)
                self.PC = self.regs[RS_INDEX]

            elif op_code == OPCode.CALLI:
                CALL_LABEL = instruction & 0x0fffffff
                self.SP -= 4
                self.memory.write32(self.SP, self.PC)
                self.PC = CALL_LABEL

            elif op_code == OPCode.RET:
                self.PC = self.memory.read32(self.SP)
                self.SP += 4

            elif op_code == OPCode.PUSH:
                self.SP -= 4
                self.memory.write32(self.SP, self.regs[RS_INDEX])

            elif op_code == OPCode.PUSH:
                self.regs[RS_INDEX] = self.memory.read32(self.SP)
                self.SP += 4

            elif op_code == OPCode.INT:
                int_num = instruction & 0xff
                self.enter_interrupt(int_num=int_num)
                self.PSW &= ~0b00  # 不再允许中断和单步调试

            elif op_code == OPCode.IRET:
                self.PC = self.memory.read32(self.SP)
                self.SP += 4
                self.PSW = self.memory.read32(self.SP)
                self.SP += 4

            elif op_code == OPCode.LIDT:
                IDT_LABEL = instruction & 0x0fffffff
                self.IDTR = IDT_LABEL

            elif op_code == OPCode.LCR:
                cr_num = RT_INDEX
                if cr_num == 0:
                    self.CR0 = self.regs[RS_INDEX]
                elif cr_num == 1:
                    self.CR1 = self.regs[RS_INDEX]
                elif cr_num == 2:
                    self.CR2 = self.regs[RS_INDEX]
                elif cr_num == 3:
                    self.CR3 = self.regs[RS_INDEX]
                else:
                    # 触发中断
                    pass

            elif op_code == OPCode.STI:
                self.PSW |= 0b10
            elif op_code == OPCode.CLI:
                self.PSW &= 0xfffffffd

            enable_interrupt = self.PSW & 0b10 >> 1
            if enable_interrupt:
                interrupt_flag = (self.PSW & 0b100) >> 2
                if interrupt_flag:
                    int_num = (self.PSW >> 16) & 0xff
                    self.enter_interrupt(int_num=int_num)