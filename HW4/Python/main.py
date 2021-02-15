# read from .asm file, build a table of PC: instr
print ('Reading in asm file...')
f = open('code.asm')
lines = f.readlines()
f.close()
print(lines)

instr_dict = {}
label_dict = {}
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

    print(func)

    if ( func[0] == 'add'):        # R-type instructions
        print(func)
        op = 0
        rd = func[1]
        rs = func[2]
        rt = func[3]


    elif (func[0] == 'slt'):
        print(func)
    elif ( func[0] == 'addi'):     # I-type instructions
        print(func)
    elif ( func[0] == 'ori'):
        print(func)
    elif ( func[0] == 'lw'):
        print(func)
    elif ( func[0] == 'sw'):
        print(func)
    elif ( func[0] == 'beq'):
        print(func)

    print('\n')


