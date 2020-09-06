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

from src.asm.objdump import ObjDumper
from src.constants import REG_SCREEN_HEIGHT, REG_SCREEN_WIDTH, REG_SCREEN_START_Y, REG_SCREEN_START_X, \
    SCREEN_REFRESH_FREQ, STACK_SCREEN_START_Y, STACK_SCREEN_START_X, STACK_SCREEN_HEIGHT, STACK_SCREEN_WIDTH, \
    CODE_SCREEN_START_Y, CODE_SCREEN_START_X, CODE_SCREEN_HEIGHT, CODE_SCREEN_WIDTH


class DebugDisplay(object):
    """
    EmmDisplay不同于Screen，Screen是显示器，而EmmDisplay是显示寄存器，栈，全局变量的地方
    """

    def __init__(self, stdscr, cpu_ins):
        self.stdscr = stdscr
        self.cpu_ins = cpu_ins
        rectangle(stdscr, uly=REG_SCREEN_START_Y, ulx=REG_SCREEN_START_X, lry=REG_SCREEN_START_Y + REG_SCREEN_HEIGHT + 1, lrx=REG_SCREEN_START_X + REG_SCREEN_WIDTH + 2)
        rectangle(stdscr, uly=STACK_SCREEN_START_Y, ulx=STACK_SCREEN_START_X, lry=STACK_SCREEN_START_Y + STACK_SCREEN_HEIGHT + 1, lrx=STACK_SCREEN_START_X + STACK_SCREEN_WIDTH + 2)
        rectangle(stdscr, uly=CODE_SCREEN_START_Y, ulx=CODE_SCREEN_START_X, lry=CODE_SCREEN_START_Y + CODE_SCREEN_HEIGHT + 1, lrx=CODE_SCREEN_START_X + CODE_SCREEN_WIDTH + 2)

    def display_regs(self):
        for i in range(32):
            if i > 22:
                self.stdscr.addstr(REG_SCREEN_START_Y + i + 1 - 9, REG_SCREEN_START_X + 17, "R%02d: 0x%08x" % (i, self.cpu_ins.regs[i]))
            else:
                self.stdscr.addstr(REG_SCREEN_START_Y + i + 1, REG_SCREEN_START_X + 1, "R%02d: 0x%08x" % (i, self.cpu_ins.regs[i]))

        self.stdscr.addstr(REG_SCREEN_START_Y + 1, REG_SCREEN_START_X + 17, "PC:  0x%08x" % self.cpu_ins.PC)
        self.stdscr.addstr(REG_SCREEN_START_Y + 2, REG_SCREEN_START_X + 17, "BP:  0x%08x" % self.cpu_ins.BP)
        self.stdscr.addstr(REG_SCREEN_START_Y + 3, REG_SCREEN_START_X + 17, "SP:  0x%08x" % self.cpu_ins.SP)
        self.stdscr.addstr(REG_SCREEN_START_Y + 4, REG_SCREEN_START_X + 17, "PSW: 0x%08x" % self.cpu_ins.PSW)
        self.stdscr.addstr(REG_SCREEN_START_Y + 5, REG_SCREEN_START_X + 17, "DTR: 0x%08x" % self.cpu_ins.IDTR)
        self.stdscr.addstr(REG_SCREEN_START_Y + 6, REG_SCREEN_START_X + 17, "CR3: 0x%08x" % self.cpu_ins.CR3)
        self.stdscr.addstr(REG_SCREEN_START_Y + 7, REG_SCREEN_START_X + 17, "CR2: 0x%08x" % self.cpu_ins.CR2)
        self.stdscr.addstr(REG_SCREEN_START_Y + 8, REG_SCREEN_START_X + 17, "CR1: 0x%08x" % self.cpu_ins.CR1)
        self.stdscr.addstr(REG_SCREEN_START_Y + 9, REG_SCREEN_START_X + 17, "CR0: 0x%08x" % self.cpu_ins.CR0)

        for i in range(0, 4):
            self.stdscr.addstr(REG_SCREEN_START_Y + i + 10, REG_SCREEN_START_X + 17, "FR%d: 0x%08x" % (i, self.cpu_ins.regs[i]))

    def display_stack(self):
        sp = self.cpu_ins.SP
        for i in range(-7, 8):
            addr = sp - 4 * i
            if addr >= self.cpu_ins.memory.size:
                continue
            if addr == sp:
                prefix = '*'
            else:
                prefix = ' '
            self.stdscr.addstr(STACK_SCREEN_START_Y + i + 7 + 1, STACK_SCREEN_START_X + 1, "%s 0x%08x:  0x%08x" % (prefix, sp - 4 * i, self.cpu_ins.memory.read32(addr)))

    def display_code(self):
        pc = self.cpu_ins.PC
        for i in range(-7, 8):
            addr = pc - 4 * i
            if addr >= self.cpu_ins.memory.size:
                continue
            if addr == pc:
                prefix = '*'
            else:
                prefix = ' '
            self.stdscr.addstr(CODE_SCREEN_START_Y + i + 7 + 1, CODE_SCREEN_START_X + 1, "%s 0x%08x:  %s" % (prefix, pc - 4 * i, ObjDumper.dis_assembly(self.cpu_ins.memory.read32(addr))))

    def run(self):
        self.stdscr.addstr(0, 30, "调试显示器始化好了！")
        while True:
            time.sleep(1.0 / SCREEN_REFRESH_FREQ)
            self.display_regs()
            self.display_stack()
            self.display_code()
            self.stdscr.refresh()

