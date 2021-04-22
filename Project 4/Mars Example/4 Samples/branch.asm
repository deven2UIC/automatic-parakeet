addi $8, $0, 0
addi $9, $0, 10
addi $10, $0, 0
while:
	andi $11, $8, 0x1
	beq $11, $0, skip
		addi, $10, $10, 0x1
		addi $8, $8, -0x2
		addi $9, $9, -0x2
	skip:
	addi, $8, $8, 2
	bne $8, $9, while
#end while