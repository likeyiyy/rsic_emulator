;加法函数: 寄存器R0 = R0 + R1
;乘法函数: 寄存器R0 = R0 * R1

.import abc,cde
.import efg,cdf


.align 4
.text
add_handler:
     add r0, r1, r0

mul_handler: mul r0, r1, r0

add_to_100:
    xor r0, r0, r0
    xor r2, r2, r2
    lui r1, hundred

loop: addi r0, r0, 1
      add r0, r2, r2
      lte r2, r1, loop
      ret

.data
hundred:
    .byte 100