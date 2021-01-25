def read_file():
    f = open('mc.txt')
    print('\nNow reading lines from mc.txt:\n')
    for line in f:
        print(line)
        mc = parse_hex8(line)
        instr_analysis(mc)
    f.close()

def get_inst(s):
    # decide if this is an addi instruction
    if(s[0:6]=='001000'):
        print(f'op = {s[0:6]}, addi instruction. \n')
    elif(s[0:6]=='000000'):
        print(f'op = {s[0:6]}, R-type instruction. \n')
    else:
        print(f'op = {s[0:6]}, unknown instruction. \n')

def user_input():
    h = input("give me an instruction in 8-digit hex: \n")
    mc = parse_hex8(h)
    return mc

# parse an 8-digit string of hex into 32-bit binary string
def parse_hex8(s):
    b = ""
    for i in range(8):
        b += hextobin(s[i])
#        print(f'now b is {b}')
    print(f'{s[:-1]} -> {b[0:6]} {b[6:11]} {b[11:16]} {b[16:32]}')
    return b


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