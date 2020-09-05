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

from src.memory import Memory


class TestMemory(unittest.TestCase):

    def test_memory(self):
        memory = Memory(1) # 1m大小

        memory.write32(17, 1)
        result = memory.read32(17)
        self.assertEqual(result, 1)

        memory.write32(1897, 2123123313)
        result = memory.read32(1897)
        self.assertEqual(result, 2123123313)

        # 一个字节只能写八位
        memory.write8(323432, 0xabee)
        self.assertEqual(memory.read8(323432), 0xee)