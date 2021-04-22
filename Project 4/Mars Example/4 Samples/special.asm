add $10, $0, $0
addi $11, $0, 80

for2:
	add $13, $10, $11
	sw $13, 0x2000($10)	# Store result
		
	addi $10, $10, 4
	bne $10, $11, for2
#end for2