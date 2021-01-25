addi $t0, $zero, -2
addi $8, $t0, 5
add $t0, $t0, $t0
addi $9, $0, 0x2020
sw $8, 0($9)
addi $9, $9, 4
sub $8, $0, $8
andi $8, $8, 15
sw $8, 0($9)
sw $9, 4($9)
lw $t6, 0x2028($0)
lw $t6, 0($9)