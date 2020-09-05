# 综述

指令集和上一个版本没有多大区别，但是着重修改了系统指令集


|opcode(8)|源寄存器（5）|中间寄存器（5）|目的寄存器（5）|剩余9位|使用示例|说明|
|---------|:-----------:|:------------:|:------------:|:------:|:---:|---:|
| *算术运算指令* |||||||
|00000000|rs|rt|rd|保留|add rs,rt,rd|rd = rs + rt|
|00000001|rs|rt|imm | |add rs,rt,rd|rd = rs + rt|
|00000010|rs|rt|rd|保留|add rs,rt,rd|rd = rs + rt|
|00000011|rs|rt|rd|保留|add rs,rt,rd|rd = rs + rt|
|00000100|rs|rt|rd|保留|add rs,rt,rd|rd = rs + rt|
|00000101|rs|rt|rd|保留|add rs,rt,rd|rd = rs + rt|
|00000110|rs|rt|rd|保留|add rs,rt,rd|rd = rs + rt|
|00000000|rs|rt|rd|保留|add rs,rt,rd|rd = rs + rt|

