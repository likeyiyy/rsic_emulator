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

from src.sign_extend import SignExtend


class TestSignExtend(unittest.TestCase):

    def assert16bitValueEqual(self, value: int):
        bit16_value = eval(bin(value & 0xffff))
        self.assertEqual(value, SignExtend.extend_16bit(bit16_value))

    def assert26bitValueEqual(self, value: int):
        bit26_value = eval(bin(value & 0b000000_11111_11111_11111_1111_1111_111))
        self.assertEqual(value, SignExtend.extend_26bit(bit26_value))

    def test_extend_16bit(self):
        self.assert16bitValueEqual(-7)
        self.assert16bitValueEqual(7)
        self.assert16bitValueEqual(0)
        self.assert16bitValueEqual(1)
        self.assert16bitValueEqual(-1)
        self.assert16bitValueEqual(int(65536 / 2) - 1)
        self.assert16bitValueEqual(- int(65536 / 2))

    def test_extend_26bit(self):
        self.assert26bitValueEqual(-7)
        self.assert26bitValueEqual(7)
        self.assert26bitValueEqual(0)
        self.assert26bitValueEqual(1)
        self.assert26bitValueEqual(-1)
        self.assert26bitValueEqual(int(65536 / 2) - 1)
        self.assert26bitValueEqual(- int(65536 / 2))
