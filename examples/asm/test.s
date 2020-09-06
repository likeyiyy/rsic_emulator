
.external
add_to_100

.align 4
.text
main:
    call add_to_100
    xor r0, r0, r0
    addi r0, 200
    add r0, r2, r2
    halt

.data
hello_world:
    .ascii "hello world!"
