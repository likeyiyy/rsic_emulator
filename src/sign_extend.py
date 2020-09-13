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


class SignExtend(object):

    @classmethod
    def extend_16bit(cls, value: int):
        """
        原来16位的数据，扩展到32位

        比如说假如value是：-7
        那么我们就假定value传递过来的int是：
        0b1111111111111001
        也就是65529

        由于我们总是假定传递过来的value是16位的，所以我们可以写更加快速的算法。

        In [1]: bin(-7 & 0xffff)
        Out[1]: '0b1111111111111001'
        :param value:
        :param bits:
        :return:
        """
        if (value & 0xffff) >> 15 == 0:
            return value
        return value - 0xffff - 1

    @classmethod
    def extend_26bit(cls, value: int):
        if (value & 0b000000_11111_11111_11111_1111_1111_111) >> 25 == 0:
            return value
        return value - 0b000000_11111_11111_11111_1111_1111_111 - 1