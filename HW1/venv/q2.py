def twoscomp(b):
    val = 0

    for i in range(len(b)):
        if (b[ (len(b) - 1) - i] == '0'):
            val += (2 ** i)

    return -1 * (val + 1)

def hextobin(c):
    num = int(c, base=16)
    b = bin(num)
    return(b[2:].zfill(32))

while(True):
    s = input('Enter instruction: \n')
    print('Entry: ' + s)

    #dec = int(s, base=16)
    #print(f'Instruction: {dec}')

    b = hextobin(s)
    print(f'Binary: {b}\n')

    inst_b = b[:6]
    read_reg_b = b[6:11]
    dest_reg_b = b[11:16]
    imm_b = b[16:]

    print('instruction: ', inst_b)
    print('read reg:    ', read_reg_b)
    print('dest reg:    ', dest_reg_b)
    print('imm:         ', imm_b, '\n')

    read_reg = int(read_reg_b, base=2)
    dest_reg = int(dest_reg_b, base=2)
    imm = int(imm_b, base=2)

    if (inst_b == '001000'):
        inst = 'addi'
    elif (inst_b == '001100'):
        inst = 'andi'
    elif (inst_b == '001101'):
        inst = 'ori'
    elif (inst_b == '001110'):
        inst = 'xori'
    else:
        inst = 'not found'

    if (imm_b[:1] == '1'):
        imm = twoscomp(imm_b)

    print('MIPS Instruction: ' +  str(inst)  + ', $' + str(dest_reg) + ', $' + str(read_reg) + ', ' + str(imm))
    print()