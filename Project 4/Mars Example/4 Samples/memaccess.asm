add $10, $0, $0
addi $11, $0, 80
for:	
	sw $10, 0x2000($10)	

	addi $10, $10, 4
	bne $10, $11, for
#end for
add $10, $0, $0
addi $11, $0, 80
for2:
	lw $13, 0x2000($10)	# Load T
	#nmb $13, $13, $9
	addi $13, $13, 0	
	sw $13, 0x2080($10)	# Store result

	addi $10, $10, 4
	bne $10, $11, for2
#end for2