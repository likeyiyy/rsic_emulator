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

import unittest
from typing import Dict, List, Tuple, Type, Union, Callable, Optional

from src.asm.objdump import ObjDumper


class TestObjDump(unittest.TestCase):

    def test_dis_assembly(self):
        ins = [
            0b00000000_00000_00000_00000_000000000,  # add
            0b00000001_00000_00000_00000_000000000,  # sub
            0b00001011_00000_00000_00000_000000000,  # not
            0b00001110_00000_00000_00000_000000000,  # lt
            0b00010100_00000_00000_00000_000000000,  # jmp
            0b00011100_00000_00000_00000_000000000,  # ret
            0b00011011_00000_00000_00000_000000000,  # calli
            0b00011001_00000_00000_00000_000000000,  # lui
            0b00011111_00000_00000_00000_000000000,  # int 31
            0b00100011_00000_00000_00000_000000000,  # lcr 35
        ]
        self.assertEqual(ObjDumper.dis_assembly(ins[0]), "ADD R0, R0, R0")
        self.assertEqual(ObjDumper.dis_assembly(ins[1]), "SUB R0, R0, R0")
        self.assertEqual(ObjDumper.dis_assembly(ins[2]), "NOT R0, R0")
        self.assertEqual(ObjDumper.dis_assembly(ins[3]), "LT R0, R0, 0x00000000")
        self.assertEqual(ObjDumper.dis_assembly(ins[4]), "JMP R0")
        self.assertEqual(ObjDumper.dis_assembly(ins[5]), "RET")
        self.assertEqual(ObjDumper.dis_assembly(ins[6]), "CALLI 0x00000000")
        self.assertEqual(ObjDumper.dis_assembly(ins[7]), "LUI R0, 0x0000")
        self.assertEqual(ObjDumper.dis_assembly(ins[8]), "INT 0")
        self.assertEqual(ObjDumper.dis_assembly(ins[9]), "LCR R0, CR0")