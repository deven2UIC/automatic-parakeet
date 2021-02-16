# read from .asm file, build a table of PC: instr
print ('Reading in asm file...')
f = open('code.asm')
lines = f.readlines()
f.close()
print(lines)

instr_dict = {}
label_dict = {}

type_dict = {}
type_dict['add'] =  'r'
type_dict['slt'] =  'r'
type_dict['addi'] = 'i'
type_dict['ori'] =  'i'
type_dict['lw'] =   'i'
type_dict['sw'] =   'i'
type_dict['beq'] =  'i'

# R-type only
funct_dict = {}
funct_dict['add'] =  0b100000
funct_dict['slt'] =  0b101010

# All types
op_dict = {}
op_dict['add'] =  0b000000
op_dict['slt'] =  0b000000
op_dict['addi'] = 0b001000
op_dict['ori'] =  0b001101
op_dict['lw'] =   0b100011
op_dict['sw'] =   0b101011
op_dict['beq'] =  0b000100

# PC : instr
PC = 0
for ln in lines:
    pos = ln.find(":")
    if pos >= 0:
        label_dict[ln[:-2]] = PC
        continue
    # print(f'pos = {pos} for {ln}')
    instr_dict[PC]=ln[:-1]  # do not include \n in the end of an instruction
    PC += 4

print('\nBelow are all the instructions:')
for PC, instr in instr_dict.items():
    print(f'{PC}: {instr}')

print('\nBelow are all the labels:')
for label, PC in label_dict.items():
    print(f'{label} =  {PC} -> {instr_dict[PC]}')

print('\nNow break each instruction into components:')
for PC, instr in instr_dict.items():
    i_new = instr.replace(",", "")  # get rid of ","
    # print(i_new)
    i_list = i_new.split(" ")       # generate a list by splitting the string with " "
    print(f'{instr} decomposed into {i_list}')

machine = []
print('\nMachine code for asm file:')
for PC, instr in instr_dict.items():
    func = instr.split()
    func[1] = func[1].replace('$', '')
    func[1] = func[1].replace(',', '')
    func[2] = func[2].replace('$', '')
    func[2] = func[2].replace(',', '')
    #print(instr)

    op = op_dict[func[0]]

    if ( type_dict[ func[0] ] == 'r'):        # R-type instructions
        func[3] = func[3].replace('$', '')
        func[3] = func[3].replace(',', '')

        rd = int(func[1], base=10)
        rd = rd << 11

        rs = int(func[2], base=10)
        rs = rs << 21

        rt = int(func[3], base=10)
        rt = rt << 16

        inst_bin = (op << 26) + rs + rt + rd + funct_dict[func[0]]
        print('PC = {0}:  0x{1:08x}'.format(PC, inst_bin))
    else:                                   # I-type instructions
        if (func[0] == 'sw' or func[0] == 'lw'): # sw/lw
            rt = int(func[1], base=10)
            add = func[2].split('(')
            offset = add[0]
            base = add[1]

            if (offset.find('0x') != -1):
                offset.replace('0x', '')
                offset = int(offset, base=16)
            else:
                offset = int(offset, base=10)

            base = base.replace(')', '')
            base = int(base, base=10)

            inst_bin = (op << 26) + (base << 21) + (rt << 16) + offset
            print('PC = {0}:  0x{1:08x}'.format(PC, inst_bin))

        elif ( func[0] == 'beq'):
            inst_bin = 0
            rs = int(func[1], base=10)
            rt = int(func[2], base=10)
            label = func[3]
            offset = (label_dict[label] - (PC + 4)) >> 2

            inst_bin = (op << 26) + (rs << 21) + (rt << 26) + offset
            print('PC = {0}:  0x{1:08x}'.format(PC, inst_bin))

        else: # all other I-types
            rt = int(func[1], base=10)
            rs = int(func[2], base=10)

            imm = func[3]
            if (imm.find('0x') != -1):
                imm.replace('0x', '')
                imm_b = int(imm, base=16)
            else:
                imm_b = int(imm, base=10)

            inst_bin = (op << 26) + (rs << 21) + (rt << 16) + imm_b
            print('PC = {0}:  0x{1:08x}'.format(PC, inst_bin))

    #print('')



