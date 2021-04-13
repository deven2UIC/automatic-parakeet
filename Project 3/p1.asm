addi $8, $0, -23456		# A[0] = $8 = 3
lui $9, 0x1f2d			# $9 = 0x12340000
ori $9, $9, 0x3d4c		# T = $9 = 0x1234fedc

# Part I (Start), uses $8, 10-13
addi $11, $11, 1
addi $13, $13, 20		# $13 dictates how many loops to do
load_array:
sw $8, 0x2020($10)		# $10 increments memory address

# Part II (Start), uses $9, 14-whatever
xor $14, $8, $9			# 1's in $14 means bits don't match, 0's in $14 means bits match
addi $15, $15, 32
sub $17, $17, $17

count:
slt $16, $14, $0		# $16 = 1 if MSB = 1 and that bit doesn't match
bne $16, $0, skip
addi $17, $17, 1		# Count number of matching bits

skip:
addi $15, $15, -1
sll $14, $14, 1
bne $15, $0, count
sw $17, 0x2080($10)

addi $19, $10, 0x2020
slt $16, $17, $18		# Compare this element's matching bits with highest ($18)
bne $16, $0, less
add $18, $0, $17		# If higher # bits match, update $18 with that value
sw $8, 0x2000($0)		# Update best match element
sw $17, 0x2004($0)		# Update the # bits match
sw $19, 0x2008($0)		# Update the address of A[i]

# Part II (End)

less:
slt $12, $8, $0			# $12 = 1 if $8 < 0
beq $12, $0, cont		# If $8 < 0, run this code
sub $8, $0, $8			# Flip $8 contents
add $8, $8, $11			# Increment $8 contents twice
add $8, $8, $11
sub $8, $0, $8			# Flip $8 contents back

cont:
add $8, $8, $11			# Always increment $8
addi $11, $11, 1		# Increase gap between neighbors
sub $8, $0, $8			# Flip $8 contents
addi $10, $10, 4		# Next array element
addi $13, $13, -1		# Loop one less time
bne $13, $0, load_array 
# Part I (End)
