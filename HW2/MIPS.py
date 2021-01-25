# char of hex digit -> a string of 4 binary bits.
def hextobin(c):
    num = int(c, base=16)
    b = bin(num)
    #    print(f'c is {c}, num is {num}, b[2:].zfill(4) is {b[2:].zfill(4)}')
    return (b[2:].zfill(4))


# parse an 8-digit string of hex into 32-bit binary string
def parse_hex8(s):
    b = ""
    for i in range(8):
        b += hextobin(s[i])
    #        print(f'now b is {b}')
    print(f'{s[:-1]} -> {b[0:6]} {b[6:11]} {b[11:16]} {b[16:32]}')
    return b


def instr_analysis(s):
    # decide if this is an addi instruction
    inst = ''
    if (s[0:6] == '001000'):
        #print(f'op = {s[0:6]}, addi instruction. \n')
        inst = 'addi'
    elif (s[0:6] == '001100'):
        #print(f'op = {s[0:6]}, andi instruction. \n')
        inst = 'andi'
    elif (s[0:6] == '001101'):
        #print(f'op = {s[0:6]}, ori instruction. \n')
        inst = 'ori'
    elif (s[0:6] == '001110'):
        #print(f'op = {s[0:6]}, xori instruction. \n')
        inst = 'xori'
    elif (s[0:6] == '101011'):
        #print(f'op = {s[0:6]}, sw instruction. \n')
        inst = 'sw'
    elif (s[0:6] == '100011'):
        #print(f'op = {s[0:6]}, lw instruction. \n')
        inst = 'lw'
    elif (s[0:6] == '000000'):
        #print(f'op = {s[0:6]}, R-type instruction. \n')
        inst = 'R-type'
    else:
        #print(f'op = {s[0:6]}, unknown instruction. \n')
        inst = 'unknown'

    return inst

def twoscomp(b):
    val = 0

    for i in range(len(b)):
        if (b[ (len(b) - 1) - i] == '0'):
            val += (2 ** i)

    return -1 * (val + 1)

def get_func_name(func):
    name = 'Unknown'

    if (func == '100000'):
        name = 'add'
    elif (func == '100100'):
        name = 'and'
    elif (func == '100010'):
        name = 'sub'
    elif (func == '100110'):
        name = 'xor'
    elif (func == '100010'):
        name = 'sub'

    return name

def print_asm_line(inst, b):
    inst_b = b[:6]

    #R-Type instructions
    if (inst_b == '000000'):
        func = b[-6:]
        func_name = get_func_name(func)

        read_reg_b_1 = b[6:11]
        read_reg_b_2 = b[11:16]
        dest_reg_b = b[16:21]

        read_reg_1 = int(read_reg_b_1, base = 2)
        read_reg_2 = int(read_reg_b_2, base = 2)
        dest_reg = int(dest_reg_b, base = 2)

        print('MIPS Instruction: ' + str(func_name) + ', $' + str(dest_reg) + ', $' + str(read_reg_1) + ', $' + str(read_reg_2))

    #I-Type instructions
    else:
        read_reg_b = b[6:11]
        dest_reg_b = b[11:16]
        imm_b = b[16:]

        read_reg = int(read_reg_b, base=2)
        dest_reg = int(dest_reg_b, base=2)
        imm = int(imm_b, base=2)

        if (imm_b[:1] == '1'):
            imm = twoscomp(imm_b)

        print('MIPS Instruction: ' + str(inst) + ', $' + str(dest_reg) + ', $' + str(read_reg) + ', ' + str(imm))



def read_file():
    f = open('mc.txt')
    print('\nNow reading lines from mc.txt:\n')
    for line in f:
        print(line)
        mc = parse_hex8(line)
        inst = instr_analysis(mc)
        print_asm_line(inst, mc)
    f.close()

read_file()