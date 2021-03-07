# Escape array A[0]– A[19]: at M[0x2020, 0x2024, … ]
# Match bit number array: at M[0x2080, 0x2084, … ]
# Best match element: at M[0x2000]
# Best match bit number: at M[0x2004]
# Address of the best match element: at M[0x2008]

addi $8, $0, -23456		# A[0] = $8 = 3
lui $9, 0x1F2E			# $9 = 0x12340000
ori $9, $9, 0x3D4C 		# T = $9 = 0x1234fedc

addi $t2, $zero, 0x2020	# Set $t2 to 0x2020 as &A[0]
addi $t3, $zero, 0x2070	# Set $t3 to 0x2070 as last element of A[]
addi $t4, $zero, 0		# Set $t4 to 0, save for comparisons
addi $t5, $zero, 0		# Set $t5 to 0, save as incrementor
addi $t7, $zero, 80		# Offset for T values

addi $s0, $s0, 1		# Bitmask
addi $s1, $s1, 0		# Bit counter

sw $t0, 0($t2)		# Store A[0]
xor $t0, $t0, $t1
nor $t0, $t0, $t0	# Gets bitwise ($t0 XNOR $t1)	
			# $t6 = matching bits
# Time to count the bits		
While3:
	beq $s0, $zero, After3	# When the bitmask rolls over to 0, while loop is over
	
	and $s2, $s0, $t0	# Apply bitmask
	beq $s2, $zero, skip3	# Don't increment if 0
		addi $s1, $s1, 1	# Increment bit counter
	skip3:
		
	sll $s0, $s0, 1		# Shift bitmask to the left
j While3
After3:
sw $s1, 0x60($t2)	# Store bit counter in array w/ offset 0x60
addi $s1, $zero, 0	# Reset bit counter
addi $s0, $zero, 0x1	# Reset bitmask
j While
addi $t2, $t2, 4 	# Increment array pointer3
addi $t5, $t5, 1 	# Increment i

While:
	slt $t4, $t2, $t3	# Sets $t4 to 1 if i < LIMIT
	beq $t4, $zero, After	# Branch of $t4 == 0
	
	lw $t6, -4($t2)		# Load previous value
	nor $t6, $t6, $t6	# flip all bits
	addi $t6, $t6, 1	# Add 1 to get twos complement
				# $t6 = -A[i-1]	
	
	andi $t4, $t5, 0x1	# if( i is odd ) then A[i-1] is positive
	beq $t4, $zero, else1
		sub $t6, $t6, $t5	# $t6 = -1*(abs(A[i-1])+i)
		J endif1
	else1:				# else ( i is even ) then A[i-1] is negative
		add $t6, $t6, $t5	# $t6 = abs(A[i-1])+i
	endif1:

	sw $t6, 0($t2)		# Store result in memory
	
	#=========================Part 2==========================
	# Free registers: $t6
	xor $t6, $t6, $t1
	nor $t6, $t6, $t6	# Gets bitwise ($t6 XNOR $t1)	
				# $t6 = matching bits
	
	# Time to count the bits		
	While2:
		beq $s0, $zero, After2	# When the bitmask rolls over to 0, while loop is over
		
		and $s2, $s0, $t6	# Apply bitmask
		beq $s2, $zero, skip	# Don't increment if 0
			addi $s1, $s1, 1	# Increment bit counter
		skip:
		
		sll $s0, $s0, 1		# Shift bitmask to the left
	j While2
	After2:
	
	sw $s1, 0x60($t2)	# Store bit counter in array w/ offset 0x60
	addi $s1, $zero, 0	# Reset bit counter
	addi $s0, $zero, 0x1	# Reset bitmask
	#=========================Part 2==========================
	
	addi $t2, $t2, 4 	# Increment array pointer3
	addi $t5, $t5, 1 	# Increment i
j While

After:

addi $t2, $zero, 0x2020
addi $t6, $zero, 0	# Best match

While4:
	slt $t4, $t2, $t3	# Sets $t4 to 1 if i < LIMIT
	beq $t4, $zero, After4	# Branch of $t4 == 0
	
	lw $t5, 0x60($t2)
	
	slt $t4, $t6, $t5
	beq $t4, $zero, skip4
		sw $t5, 0x2004($zero)	# Store # of bits
		sw $t2, 0x2008($zero)	# Store address
		
		lw $t5, 0($t2)
		sw $t5, 0x2000($zero)	# Store value
	skip4:
	
	addi $t2, $t2, 4 	# Increment array pointer3
	addi $t5, $t5, 1 	# Increment i
j While4

After4:




