import enum


class OPCode(int, enum.Enum):
    # 算术运算指令
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4
    # 浮点数运算指令
    FADD = 5
    FSUB = 6
    FMUL = 7
    FDIV = 8
    # 逻辑运算指令
    AND = 9
    OR  = 10
    NOT = 11
    SLL = 12
    SLR = 13

    # 比较转移指令
    LT = 14
    GT = 15
    LTE = 16
    GTE = 17
    EQ = 18
    NEQ = 19
    JMP = 20
    JMPI = 21

    # 数据传输指令
    MOV = 22
    LOAD = 23
    STORE = 24
    LUI = 25

    # 系统指令
    CALL = 26
    CALLI = 27
    RET = 28
    PUSH = 29
    POP = 30
    INT = 31
    HALT = 32
    IRET = 33
    LIDT = 34
    LCR = 35
    STI = 36
    CLI = 37

    # 补充指令
    XOR = 38
    ADDI = 39
    NOP = 40


three_reg_opcodes = (
    OPCode.ADD,
    OPCode.SUB,
    OPCode.MUL,
    OPCode.DIV,
    OPCode.MOD,
    OPCode.FADD,
    OPCode.FSUB,
    OPCode.FMUL,
    OPCode.FDIV,
    OPCode.AND,
    OPCode.OR,
)
two_reg_with_reversed = (
    OPCode.NOT,
    OPCode.SLL,
    OPCode.SLR,
    OPCode.MOV,
    OPCode.LOAD,
    OPCode.STORE,
)
two_reg_with_label = (
    OPCode.LT,
    OPCode.GT,
    OPCode.LTE,
    OPCode.GTE,
    OPCode.EQ,
    OPCode.NEQ,
)
single_reg_with_reversed = (
    OPCode.JMP,
    OPCode.CALL,
    OPCode.PUSH,
    OPCode.POP,
)
no_reg_with_reversed = (
    OPCode.RET,
    OPCode.HALT,
    OPCode.NOP,
    OPCode.IRET,
    OPCode.STI,
    OPCode.CLI,
)
no_reg_with_label = (
    OPCode.JMPI,
    OPCode.CALLI,
    OPCode.LIDT,
)