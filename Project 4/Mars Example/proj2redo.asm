addi $8, $0, 3 # A[0] = $8 = 3
lui $9, 0x0 # $9 = 0x12340000
ori $9, $9, 0xFEDC # T = $9 = 0x1234fedc

add $10, $0, $0
addi $11, $0, 80
add $13, $8, $0

for:
sw $13, 0x2020($10)
srl $15, $10, 2

slt $14, $13, $0
bne $14, $0, else
if: # previous number is positive
	sub $12, $0, $13
	addi, $15, $15, 1
	sub $12, $12, $15
	j done
else: # previous number is negative
	sub $12, $0, $13
	addi, $15, $15, 1
	add $12, $12, $15

done:
add $13, $12, $0


addi $10, $10, 4
bne $10, $11, for

#========

add $10, $0, $0
addi $11, $0, 80

for2:
	lw $13, 0x2020($10)	# Load T
	add $16, $0, $0	# counter = 0
	#nmb $13, $13, $9
	xor $13, $13, $9 	# Step 1: get xor
	nor $13, $13, $13 	# Step 2: get xnor
				# Step 3: Count number of 1's (no XNOR)
	addi $14, $0, 1 	# Create bitmask
	while:
		and $15, $14, $13	# Apply bitmask
		beq $15, $0, skip	# if(mask & same_bits == 1)
			addi $16, $16, 1	# Increment counter
		skip:
		sll $14, $14, 1
		bne $14, $0, while
	#end while
	#End nmb
	
	sw $16, 0x2080($10)	# Store result

	addi $10, $10, 4
	bne $10, $11, for2
#end for2
