ori $7, $0, 12
add $8, $0, $0
loop:
loop2:
sw $8, 0x2000($7)
addi $7, $7, 4
beq $8, $0, out
addi $8, $8, -1
beq $0, $0, loop
out:
sw $7, 0x2000($0)
addi $9, $0, 8196
lw $10, -4($9)
slt $8, $0, $0
