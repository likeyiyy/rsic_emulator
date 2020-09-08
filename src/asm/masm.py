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

import copy
import os
import sys
from typing import Dict, List, Tuple, Type, Union, Callable, Optional

from src.opcode import OPCode, three_reg_opcodes, two_reg_with_reversed, two_reg_with_label, single_reg_with_reversed, \
    no_reg_with_reversed, no_reg_with_label

VERSION = "0.0.1"

resolved_map = set()


class PreProcessor(object):

    def __init__(self, dependency: List = None):
        if not dependency:
            self.dependency = []
        else:
            self.dependency = dependency

    def process(self, file_path: str):
        if not os.path.exists(file_path):
            raise Exception("不存在的文件路径！")
        relative_root, file_name = os.path.split(file_path)
        source_file_abs_path = os.path.abspath(file_path)
        self.dependency.append(source_file_abs_path)
        with open(file_path, "r") as f:
            content = f.read()
            iter_content = copy.deepcopy(content)
            for line_content in iter_content.split("\n"):
                if line_content.startswith(".include"):
                    depend_file = line_content.replace(".include", "").strip().replace('"', "")
                    depend_file = os.path.join(relative_root, depend_file)
                    depend_file_abs_path = os.path.abspath(depend_file)
                    global resolved_map
                    if depend_file_abs_path not in resolved_map:
                        if depend_file_abs_path in self.dependency:
                            raise Exception(f"出现了循环依赖： {file_path}依赖{depend_file_abs_path}，但是{depend_file_abs_path}已经出现在{self.dependency}中"
                                            f", 或者是文件头依赖了多次")
                        else:
                            self.dependency.append(depend_file_abs_path)
                        depend_content = PreProcessor(copy.deepcopy(self.dependency)).process(depend_file)
                        content = content.replace(line_content, depend_content)
                        resolved_map.add(depend_file_abs_path)
                    else:
                        content = content.replace(line_content, "")
        return content


class PassOne(object):

    def __init__(self):
        self.label_maps = {}
        self.import_labels = []
        self.public_labels = []

    def process(self, file_content: str):
        ipc = 0
        for idx, line in enumerate(file_content.split("\n")):
            line = line.strip()
            if line.startswith(";") or not line:
                continue
            elif line.startswith("."):
                
                if line.startswith(".align"):
                    align_num = int(line.replace(".align", "").replace('"', '').strip())
                    while ipc % align_num != 0:
                        ipc += 1
                elif line.startswith(".ascii"):
                    strings = line.replace(".ascii", "").replace('"', '').strip()
                    if not strings:
                        raise Exception(f"第{idx + 1}行： .ascii后面没有跟着字符串")
                    ipc += len(strings)
                elif line.startswith(".byte"):
                    num_str = line.replace(".byte", "").strip()
                    if not num_str.isdigit():
                        raise Exception(f"第{idx + 1}行： .byte后面跟的不是数字")
                    ipc += 1
                elif line.startswith(".word"):
                    num_str = line.replace(".word", "").strip()
                    if not num_str.isdigit():
                        raise Exception(f"第{idx + 1}行： .word后面跟的不是数字")
                    ipc += 4
                elif line.startswith(".import"):
                    labels = [_.strip() for _ in line.replace(".import", "").split(",")]
                    for label in labels:
                        if label in self.label_maps.keys():
                            raise Exception(f"第{idx + 1}行： .import 导入的label和本文件中的label重名了: {label}。")
                        else:
                            self.import_labels.append(label)
                elif line.startswith(".public"):
                    labels = [_.strip() for _ in line.replace(".public", "").split(",")]
                    self.public_labels.extend(labels)
                continue
            elif ":" in line:
                label = line.split(":")[0]
                if label in label_maps:
                    raise Exception(f"第{idx + 1}行： 重复定义的Label:  {label}")
                else:
                    if label.upper() in OPCode._member_names_:
                        raise Exception(f"第{idx + 1}行： Label名称和opcode相同，： {label}")
                    label_maps[label] = ipc
            else:
                ipc += 1

        for label in self.public_labels:
            if label not in self.label_maps.keys():
                raise Exception(f"Error: 想要public的label{label}， 在本文件中没有定义")
        return label_maps

# object file format simple defined here
# 0-3字节：  magic num
# 4-7字节：  .public区域 文件偏移位置
# 8-11字节： .public区域大小
# 12-15字节： .import区域 文件偏移位置
# 16-19字节： .import区域大小
# 20-23字节： .text 文件偏移位置
# 24-27字节： .text 大小
# 28-31字节： .data 文件偏移位置
# 32-35字节： .data 大小
# 36-39字节： .strtab 文件偏移位置，以0为终止符
# 40-43字节： .strtab 大小


# .entry
# .entry每8个字节一组，前四个字节代表符号表的位置，后四个字节代表入口地址，所以我们支持大概2^32个符号
# .import
# .import每8个字节一组，前四个字节代表指令地址，后面四个字节代表符号表中的偏移
MAGIC_NUMBER = 0x7f454c4602010100

pre_code = [
    ".align",
    ".text",
    ".data",
    ".byte",
    ".word",
    ".import",
    ".public",
    ".ascii",
    ".asciz",
]

NOP = 0b0010_1000_0000_0000_0000_0000_0000_0000


class PassTwo(object):

    def __init__(self):
        # 状态
        self.in_text_section = False
        self.in_data_section = False
        self.code = []
        self.data = []
        self.public_labels = {}
        self.import_labels = {}
        self.strtab = []
        self.reloc_table = []

    def clear_in_status(self):
        self.in_text_section = False
        self.in_data_section = False

    def process(self, file_content: str, symbol_map: Dict, import_labels: List, public_labels: List):
        ipc = 0
        for idx, line in enumerate(file_content.split("\n")):
            line = line.strip()
            if line.startswith(";") or not line:
                continue
            elif line.startswith("."):
                if not any(code in line for code in pre_code):
                    raise Exception(f"第{idx + 1}行： 未识别的伪指令{line}")
                if line.startswith(".align"):
                    align_num = int(line.replace(".align", "").replace('"', '').strip())
                    while ipc % align_num != 0:
                        self.code.append(NOP)
                        ipc += 1
                    self.clear_in_status()
                elif line.startswith(".text"):
                    self.in_text_section = True
                elif line.startswith(".data"):
                    self.in_data_section = True
                elif line.startswith(".byte"):
                    if not self.in_data_section:
                        raise Exception(f"第{idx + 1}行： .byte应该在data section")
                elif line.startswith(".word"):
                    pass
                elif line.startswith(".import"):
                    pass
                elif line.startswith(".public"):
                    pass
                elif line.startswith(".ascii"):
                    pass
                elif line.startswith(".asciz"):
                    pass
            elif ":" in line:
                continue
            else:
                registers = None
                opcode_and_registers = line.split(' ', 1)
                if len(opcode_and_registers) == 2:
                    opcode, registers = opcode_and_registers
                else:
                    opcode = line
                try:
                    opcode = OPCode(opcode.upper())
                except:
                    raise Exception(f"第{idx + 1}行： 不支持的opcode： {opcode}")
                if opcode in three_reg_opcodes:
                    rs, rt, rd = [_.strip() for _ in registers.split(",")]
                    rs_idx = int(rs.replace("R", ""))
                    rt_idx = int(rt.replace("R", ""))
                    rd_idx = int(rd.replace("R", ""))
                    instruction = opcode << 24 | rs_idx << 19 | rt_idx << 14 | rd_idx << 9 & ~0b1_1111_1111
                    self.code.append(instruction)
                elif opcode in two_reg_with_reversed:
                    rs, rt = [_.strip() for _ in registers.split(",")]
                    rs_idx = int(rs.replace("R", ""))
                    rt_idx = int(rt.replace("R", ""))
                    instruction = opcode << 24 | rs_idx << 19 | rt_idx << 14 & ~0b11111_1_1111_1111
                    self.code.append(instruction)
                elif opcode in two_reg_with_label:
                    rs, rt, label = [_.strip() for _ in registers.split(",")]
                    rs_idx = int(rs.replace("R", ""))
                    rt_idx = int(rt.replace("R", ""))
                    if label in symbol_map.keys():
                        # 若是本系统内定义的
                        label_idx = symbol_map.get(label)
                        instruction = opcode << 24 | rs_idx << 19 | rt_idx << 14 & ~0b11111_1_1111_1111
                        self.code.append(instruction)
                        self.reloc_table.append(ipc)
                    elif label in import_labels:
                        # 若是外部定义的
                        label_idx = self.get_strt_able_index(label)
                        if ipc in self.import_labels:
                            raise Exception(f"第{idx + 1}行： {ipc}已经占用了一个label位置")
                        else:
                            # 第ipc行指令引用了字符串表中label_idx位置的字符
                            self.import_labels[ipc] = label_idx

                    else:
                        raise Exception(f"第{idx + 1}行： {label}没有在文件中定义，也没有在import中定义")


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
                print(ipc, opcode, registers)
                ipc += 1

    def get_strt_able_index(self, label: str):
        # 在字符串表中，则返回符号表的位置，不在符号表中，则插入，再返回位置
        if label in self.strtab:
            label_idx = self.strtab.index(label)
        else:
            self.strtab.append(label)
            label_idx = len(self.strtab) - 1
        return label_idx


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', nargs='?', help='源文件')
    parser.add_argument('--version', '-v', action='store_true', help='版本信息')
    parser.add_argument('--object_file', '-o', help='生成目标文件的文件名')
    args = parser.parse_args()
    object_file = ""
    if not (args.version or args.object_file or args.source_file):
        parser.print_help()
    else:
        source_file = None
        if args.version:
            print(VERSION)
        else:
            if args.object_file:
                object_file = args.object_file
            elif args.source_file:
                object_file = args.source_file.replace(".s", ".o")
            if args.source_file:
                source_file = args.source_file
            if not source_file:
                print("您必须提供源码文件!")
                sys.exit(-1)
            content = PreProcessor().process(source_file)
            label_maps = PassOne().process(content)
            PassTwo().process(content, label_maps)
            print(label_maps)

