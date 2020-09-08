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

from src.opcode import OPCode, three_reg_opcodes, two_reg_with_reversed, two_reg_with_label, single_reg_with_reversed, \
    no_reg_with_reversed, no_reg_with_label


class InsDumper(object):

    @classmethod
    def dis_assembly(cls, instruction: int):
        instruction &= 0xffff_ffff
        RS_INDEX = (instruction & 0x00ff_ffff) >> 19
        RT_INDEX = (instruction & 0x007f_ffff) >> 14
        RD_INDEX = (instruction & 0x0003_ffff) >> 9
        JUMP_LABEL = instruction & 0b11_1111_1111_1111
        opcode = instruction >> 24
        if opcode in three_reg_opcodes:
            return f"{OPCode(opcode).name} R{RS_INDEX}, R{RT_INDEX}, R{RD_INDEX}"
        elif opcode in two_reg_with_reversed:
            return f"{OPCode(opcode).name} R{RS_INDEX}, R{RT_INDEX}"
        elif opcode in two_reg_with_label:
            label = "0x%08x" % JUMP_LABEL
            return f"{OPCode(opcode).name} R{RS_INDEX}, R{RT_INDEX}, {label}"
        elif opcode in single_reg_with_reversed:
            return f"{OPCode(opcode).name} R{RS_INDEX}"
        elif opcode in no_reg_with_reversed:
            return f"{OPCode(opcode).name}"
        elif opcode in no_reg_with_label:
            NO_REG_LABEL = instruction & 0x00ff_ffff
            label = "0x%08x" % NO_REG_LABEL
            return f"{OPCode(opcode).name} {label}"
        elif opcode == OPCode.LUI:
            LUI_LABEL = instruction & 0xffff
            label = "0x%04x" % LUI_LABEL
            return f"{OPCode(opcode).name} R{RS_INDEX}, {label}"
        elif opcode == OPCode.INT:
            INT_NUM = instruction & 0xff
            return f"{OPCode(opcode).name} {INT_NUM}"
        elif opcode == OPCode.LCR:
            return f"{OPCode(opcode).name} R{RS_INDEX}, CR{RT_INDEX}"
        else:
            raise NotImplementedError

