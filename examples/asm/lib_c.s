;测试依赖

.align 4
.text
    xor r0, r0, r0
    xor r1, r1, r1
    addi r0, 100
.align 4
loop:
    addi r1, 1
    lt r1, r0, loop
    halt

.align 4
.data
hw:
    .ascii "hello world\n"
bbc:
    .byte 100
    .word 100
ccd:
    .byte 100
    .word 100
