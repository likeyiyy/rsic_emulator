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

if typing.TYPE_CHECKING:
    pass

UINT8 = typing.NewType("UINT8", int)
UINT16 = typing.NewType("UINT16", int)
UINT32 = typing.NewType("UINT32", int)


class Memory(object):

    def __init__(self, size_in_mb: int):
        self.size = size_in_mb * 1024 * 1024
        self._memory = [0 & 0xff] * self.size

    def read8(self, addr: UINT32):
        if addr > self.size:
            raise Exception(f"不存在的地址{addr}")
        return self._memory[addr]

    def write8(self, addr: UINT32, value: UINT8):
        if addr > self.size:
            raise Exception(f"不存在的地址{addr}")
        value = value & 0xff
        self._memory[addr] = value

    def read32(self, addr: UINT32):
        if addr > self.size:
            raise Exception(f"不存在的地址{addr}")
        addr = addr & ~0b11
        value = (self._memory[addr + 3] << 24) \
                + (self._memory[addr + 2] << 16) \
                + (self._memory[addr + 1] << 8) \
                + self._memory[addr]
        return value

    def write32(self, addr: UINT32, value: UINT32):
        if addr > self.size:
            raise Exception(f"不存在的地址{addr}")
        addr = addr & ~0b11
        self._memory[addr] = value & 0xff
        self._memory[addr + 1] = value >> 8 & 0xff
        self._memory[addr + 2] = value >> 16 & 0xff
        self._memory[addr + 3] = value >> 24 & 0xff