# 设计思路
结合x86和mips两种指令集的综合，分为特殊寄存器，和普通寄存器，寄存器都是32位

# 特殊寄存器

PC程序计数器

BP( Base Pointer regilter)：基址指针寄存器。

SP( Stack Pointer Register)：堆栈指针寄存器。

PSW(Program Status Word): 标志寄存器

|位|名称|含义|
|---|---|---|
|00|TF|跟踪标志，为程序调试，若为1，则每执行一条指令，都会出发中断向量1|
|01|IF|中断许可标志位|
|02|IH|中断发生标志位|
|03..15|...|留空|
|16..23|...|中断向量|
|24..31|...|中断优先级|

IDTR 中断表基址寄存器
你可以将中断处理程序表的基地址指向IDTR

CR3：页目录基址寄存器

CR2：缺页寄存器

    CR1: 保留

CR0: 控制寄存器

|位|名称|含义|
|---|---|---|
|00|PE|Protection Enable|
|01..30|...|留空|
|31|PG|分页(Paging)标志|

# 通用寄存器
$0..$31
通用寄存器


$32..$35
浮点寄存器
