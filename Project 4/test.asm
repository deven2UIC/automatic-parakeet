# test program
addi $8, $0, 2
addi $9, $0, 52 #
sw_loop:
sw $8, 0x2000($9)
beq $9, $0, sw_done
addi $9, $9, -4
sub $8, $0, $8
addi $8, $8, -17
xor $8, $8, $9
beq $0, $0, sw_loop
sw_done:
addi $8, $0, 0x2174 #
addi $9, $0, 0x2000
addi $10, $9, 60 #
outer_loop:
addi $14, $0, 3
lw $11, 0($9)
inner_loop:
lw $12, 0($9)
slt $13, $12, $11
beq $13, $0, skip
add $11, $0, $12
skip:
addi $9, $9, 4
addi $14, $14, -1
bne $14, $0, inner_loop
sw $11, 0($8)
addi $8, $8, 44 #
addi $9, $9, -8
slt $13, $9, $10
bne $13, $0, outer_loop