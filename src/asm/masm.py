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
    no_reg_with_reversed, no_reg_with_label, two_reg_with_imm

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

    def __init__(self, file_content: str):
        self.file_content = file_content
        self.label_maps = {}
        self.import_labels = []
        self.public_labels = []

    def process(self) -> "PassOne":
        ipc = 0
        for idx, line in enumerate(self.file_content.split("\n")):
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
                if label in self.label_maps:
                    raise Exception(f"第{idx + 1}行： 重复定义的Label:  {label}")
                else:
                    if label.upper() in OPCode._member_names_:
                        raise Exception(f"第{idx + 1}行： Label名称和opcode相同，： {label}")
                    self.label_maps[label] = ipc
            else:
                ipc += 4

        for label in self.public_labels:
            if label not in self.label_maps.keys():
                raise Exception(f"Error: 想要public的label{label}， 在本文件中没有定义")

        return self

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

    def __init__(self, pass_one_assembly: PassOne):
        # 继承pass one
        self.file_content = pass_one_assembly.file_content
        self.symbol_map = pass_one_assembly.label_maps
        self.import_labels = pass_one_assembly.import_labels
        self.public_labels = pass_one_assembly.public_labels

        # 状态
        self.in_text_section = False
        self.in_data_section = False
        self.code = []
        self.data = []
        self.public_labels_tab = {}
        self.import_labels_tab = {}
        self.str_tab = []

    def clear_in_status(self):
        self.in_text_section = False
        self.in_data_section = False

    def process(self):
        ipc = 0
        for idx, line in enumerate(self.file_content.split("\n")):
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
                    opcode = OPCode.__members__[opcode.upper()]
                except:
                    raise Exception(f"第{idx + 1}行： 不支持的opcode： {opcode}")
                if opcode in three_reg_opcodes:
                    rs, rt, rd = [_.strip() for _ in registers.split(",")]
                    rs_idx = int(rs.replace("r", ""))
                    rt_idx = int(rt.replace("r", ""))
                    rd_idx = int(rd.replace("r", ""))
                    instruction = opcode << 26 | rs_idx << 21 | rt_idx << 17 | rd_idx << 11 & ~0b111_1111_1111
                    self.code.append(instruction)
                elif opcode in two_reg_with_reversed:
                    rs, rt = [_.strip() for _ in registers.split(",")]
                    rs_idx = int(rs.lower().replace("r", ""))
                    rt_idx = int(rt.replace("r", ""))
                    instruction = opcode << 26 | rs_idx << 21 | rt_idx << 16 & ~0b11111_111_1111_1111
                    self.code.append(instruction)
                elif opcode in two_reg_with_label:
                    rs, rt, label = [_.strip() for _ in registers.split(",")]
                    rs_idx = int(rs.replace("r", ""))
                    rt_idx = int(rt.replace("r", ""))
                    if label in self.symbol_map.keys():
                        # 若是本系统内定义的
                        label_ipc = self.symbol_map.get(label)
                        instruction = opcode << 26 | rs_idx << 21 | rt_idx << 16 | (((label_ipc - ipc) // 4) & 0xffff)
                        self.code.append(instruction)
                    elif label in self.import_labels:
                        # 若是外部定义的
                        label_idx = self.get_strt_able_index(label)
                        if ipc in self.import_labels_tab:
                            raise Exception(f"第{idx + 1}行： {ipc}已经占用了一个label位置")
                        else:
                            # 第ipc行指令引用了字符串表中label_idx位置的字符
                            self.import_labels_tab[ipc] = label_idx
                            # 低的位置暂时清零
                            instruction = opcode << 26 | rs_idx << 21 | rt_idx << 16 & ~0b11111_111_1111_1111
                            self.code.append(instruction)
                    else:
                        raise Exception(f"第{idx + 1}行： {label}没有在文件中定义，也没有在import中定义")
                elif opcode in two_reg_with_imm:
                    rs, rt, imm = [_.strip() for _ in registers.split(",")]
                    rs_idx = int(rs.replace("r", ""))
                    rt_idx = int(rt.replace("r", ""))
                    imm = int(eval(imm))
                    instruction = opcode << 26 | rs_idx << 21 | rt_idx << 16 | imm
                    self.code.append(instruction)
                elif opcode in single_reg_with_reversed:
                    rs = registers.strip()
                    try:
                        rs_idx = int(rs.replace("r", ""))
                    except:
                        raise Exception(f"第{idx + 1}行： {rs}不是一个有效的寄存器")
                    instruction = opcode << 26 | rs_idx << 21
                    self.code.append(instruction)
                elif opcode in no_reg_with_reversed:
                    instruction = opcode << 26
                    self.code.append(instruction)
                elif opcode in no_reg_with_label:
                    label = registers.strip()
                    if label in self.symbol_map.keys():
                        # 若是本系统内定义的
                        label_ipc = self.symbol_map.get(label)
                        instruction = opcode << 26 | (((label_ipc - ipc) // 4) & 0b11111_11111_11111_111_1111_1111)
                        self.code.append(instruction)
                    elif label in self.import_labels:
                        # 若是外部定义的
                        label_idx = self.get_strt_able_index(label)
                        if ipc in self.import_labels_tab:
                            raise Exception(f"第{idx + 1}行： {ipc}已经占用了一个label位置")
                        else:
                            # 第ipc行指令引用了字符串表中label_idx位置的字符
                            self.import_labels_tab[ipc] = label_idx
                            # 低的位置暂时清零
                            instruction = opcode << 26
                            self.code.append(instruction)
                    else:
                        raise Exception(f"第{idx + 1}行： {label}没有在文件中定义，也没有在import中定义")
                elif opcode == OPCode.LUI:
                    LUI_LABEL = eval(registers.strip()) & 0xffff
                    instruction = opcode << 26 | LUI_LABEL
                    self.code.append(instruction)
                elif opcode == OPCode.INT:
                    INT_NUM = eval(registers.strip()) & 0xff
                    instruction = opcode << 26 | INT_NUM
                    self.code.append(instruction)
                elif opcode == OPCode.LCR:
                    int_num, value = [_.strip() for _ in registers.split(",")]
                    value = eval(value) & 0b11111_11111_111_1111_1111
                    instruction = opcode << 26 | int_num << 21 | value
                    self.code.append(instruction)
                else:
                    print(opcode)
                    raise NotImplementedError
                print(ipc, opcode, registers)
                ipc += 4
        return self

    def print_code(self):
        print(f"code start: size: {len(self.code) * 4}".center(80, "*"))
        for code in self.code:
            print(bin(code)[2:].zfill(32))
        print("code end".center(80, "*"))

    def print_data(self):
        print(f"data start: size: {len(self.data) * 4}".center(80, "*"))
        for data in self.data:
            print(bin(data)[2:].zfill(32))
        print("data end".center(80, "*"))

    def print_str_tab(self):
        print(f"str_tab start: size: {sum([len(_) for _ in self.str_tab])}".center(80, "*"))
        for string in self.str_tab:
            print(string)
        print("str_tab end".center(80, "*"))

    def print_format(self):
        self.print_code()
        self.print_data()
        self.print_str_tab()

    def get_strt_able_index(self, label: str):
        # 在字符串表中，则返回符号表的位置，不在符号表中，则插入，再返回位置
        if label in self.str_tab:
            label_idx = self.str_tab.index(label)
        else:
            self.str_tab.append(label)
            label_idx = len(self.str_tab) - 1
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
            pass_two = PassTwo(PassOne(content).process()).process()
            pass_two.print_format()