ori $7, $zero, 0x14
add $8, $7, $7
Label3:
slt $9, $8, $0
bne $9, $0, Label1
sw $8, 0x2000($7)
Label1:
srl $8, $8, 1
sub $8, $0, $8
andi $8, $8, 15
addi $7, $7, -4
beq $7, $0, Label2
beq $0, $0, Label3
Label2:
lw $9, 0x2004($0)
