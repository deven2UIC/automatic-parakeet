

class Instruction:
    """Instantiate with a hex string"""

    # Add i type instructions here {op : name}
    i_types = {'0000': 'init',
               '0001': 'init',
               '0010': 'init',
               '0011': 'init',
               '0100': 'addi',
               '0101': 'subi',
               '1000': 'bneR0',
               '1010': 'sll',
               '1111': 'halt'
               }

    # Add r type instructions here {op : name}
    r_types = {'1001': 'sltR0',
               '1110': 'lw',
               '0110': 'sw',
               '1011': 'nxt',
               '1100': 'sub',
               '1101': 'mtc',
               '0111': 'mov'
               }

    # Add j type instructions here {op : name}
    j_types = {'000010': 'j'}

    def __init__(self, inst_hex):
        self._full = ''
        self._inst = ''
        self._func = ''
        self._type = ''
        self._opcode = ''
        self._rs = ''
        self._rt = ''
        self._rd = ''
        self._rx = ''
        self._ry = ''
        self._imm = ''

        self._hex = inst_hex
        self._bin = bin(int(self._hex, 16))[2:].zfill(8)
        self._bin = self._bin[::-1]
        # print('Hex: {}\tBinary: {}'.format(self._hex, self._bin[::-1]))
        self._to_ISA()

    def _to_ISA(self):
        """Convert hex/bin instruction to MIPS text."""
        self._opcode = self._bin[-4:][::-1]

        if self._opcode in self.r_types.keys():
            self._r_type()
        elif self._opcode in self.i_types.keys():
            self._i_type()
        elif self._opcode in self.j_types.keys():
            self._j_type()

    def _r_type(self):
        """Converts r-types, only called internally."""
        # print('[0:1]: {}'.format(self._bin[:2][::-1]))
        # print('[2:3]: {}'.format(self._bin[2:4][::-1]))
        # print('[4:5]: {}'.format(self._bin[4:6][::-1]))
        # print('[6:7]: {}'.format(self._bin[6:][::-1]))
        self._type = 'r'
        self._inst = self.r_types[self._opcode]

        self._rx = self._bin[2:4][::-1]
        self._ry = self._bin[0:2][::-1]

        # print('opcode: {}'.format(self._opcode))
        # print('rx: {}'.format(self._rx))
        # print('ry: {}'.format(self._ry))
        # print('inst: {}'.format(self._inst))

        self._full = '{} ${}, ${}'.format(self._inst, int(self._rx, 2), int(self._ry, 2))
        #print('Name: {}\n'.format(self._full))

    def _i_type(self):
        """Converts i-types, only called internally."""
        self._type = 'i'
        self._inst = self.i_types[self._opcode]

        # Get value for rx, if necessary
        if self._inst == 'init':
            self._rx = self._bin[4:6][::-1]
        elif self._inst[:3] == 'beq' or self._inst[:3] == 'bne':
            pass
        else:
            self._rx = self._bin[2:4][::-1]

        # Get value for imm
        if self._inst[:4] == 'addi' or self._inst[:4] == 'subi' or self._inst == 'sll':
            self._imm = self._bin[:2][::-1]  # Take the last 2
        else:
            self._imm = self._bin[:4][::-1]  # Take the last 4

        # Set full instruction string
        if self._inst[:3] == 'beq' or self._inst[:3] == 'bne':
            self._full = '{} {}'.format(self._inst, int(self._imm, 2))
        else:
            self._full = '{} ${}, {}'.format(self._inst, int(self._rx, 2), int(self._imm, 2))

        #print('Name: {}\n'.format(self._full))

    def _j_type(self):
        """Converts j-types, only called internally."""
        self._type = 'j'

        self._imm = self._bin[0:26][::-1]
        self._inst = self.j_types[self._opcode]

        self._full = '{} {}'.format(self._inst, self._imm)

    def _twos_comp(self, b):
        """Returns twos comp of bin string, returns int."""
        if b[0] == '0':
            return int(b, 2)
        val = 0

        for i in range(len(b)):
            if b[(len(b) - 1) - i] == '0':
                val += (2 ** i)

        return -1 * (val + 1)

    def print_all(self):
        """Prints instruction and all binary/hex field info."""
        print('Hex: {}'.format(self._hex))
        print('Bin: 0b{}'.format(self._bin))

        if self._type == 'r':
            print('Func: {}'.format(self._func))
            print('$rx: {}'.format(self._rs))
            print('$ry: {}'.format(self._rt))
            print('Inst: {}'.format(self._inst))
            print('Full: {}'.format(self._full))
        elif self._type == 'i':
            print('Opcode: {}'.format(self._opcode))
            print('$rx: {}'.format(self._rs))
            print('imm: {}'.format(self._imm))
            print('Inst: {}'.format(self._inst))
            print('Full: {}'.format(self._full))
        else:
            pass

    def print_inst(self):
        """Prints inst with special regs/imm vals in text."""
        full = 'ERROR'
        if self._type == 'r':
            full = '{} ${}, ${}'.format(self._inst, special_reg(self), special_reg_y(self))
        elif self._type == 'i':
            if self._inst[:3] == 'beq' or self._inst[:3] == 'bne':
                full = '{} {}'.format(self._inst, special_imm(self))
            else:
                full = '{} ${}, {}'.format(self._inst, special_reg(self), special_imm(self))
        print(full)

    def print_inst_true(self):
        """Prints inst as entered in text."""
        print(self._full)

    def get_inst(self):
        """Returns instruction as string."""
        full = 'ERROR'
        if self._type == 'r':
            full = '{} ${}, ${}'.format(self._inst, special_reg(self), special_reg_y(self))
        elif self._type == 'i':
            if self._inst[:3] == 'beq' or self._inst[:3] == 'bne':
                full = '{} {}'.format(self._inst, special_imm(self))
            else:
                full = '{} ${}, {}'.format(self._inst, special_reg(self), special_imm(self))

        return full

    def get_inst_true(self):
        """Returns instruction as string."""
        return self._full

    def get_action(self):
        """Returns corresponding function name for instruction."""
        return self._inst

    def get_rx(self):
        """Returns int value for field $rs."""
        return int(self._rx, 2)

    def get_ry(self):
        """Returns int value for field $rt."""
        return int(self._ry, 2)

    def get_imm(self):
        """Returns int value for immediate field."""
        return int(self._imm, 2)

    def get_imm_twos(self):
        """Returns int value for immediate field."""
        return twos_comp(self._imm)

    def get_offset(self):
        return self._twos_comp(self._imm)


"""
Helper functions and data for the operation functions
"""
def twos_comp(x):   # string x of 0/1
    # find rightmost 1's index xxxx1000
    if type(x) is not str:
        x = bin(x)[2:]

    rightmost1_idx = -1
    for i in range(len(x)-1, -1, -1):
        # print(i)
        if x[i] == '1':
            rightmost1_idx = i
            break
    # print(f'rightmost 1 idx is {rightmost1_idx}')
    y_same = x[rightmost1_idx:]
    y_flip = ""
    for i in range(rightmost1_idx):
        y_flip += str(1-int(x[i]))
    y = y_flip+y_same
    return y

def int_to_16bin_string(num_int):
    if num_int >= 0:
        s = bin(num_int)[2:].zfill(16)
    else:   # neg number
        t = bin(0 - num_int)[2:].zfill(16)
        s = twos_comp(t)
    return(s)

def special_imm(inst):
    """Finds special immediate values for operation from dict"""
    if inst.get_action() in imm_vals:
        return imm_vals[inst.get_action()][inst.get_imm()]
    else:
        return inst.get_imm()

"""
Functions for each supported instructions. Each are indexed in a dictionary in the main 
program file where they can be called automatically.
"""
def init(core, inst):
    """Rx =- imm [-8,7]"""
    # core.print_state()
    # input()
    core.set_reg(special_reg(inst), inst.get_imm())

def mov(core, inst):
    Rx = special_reg(inst)
    Ry = special_reg_y(inst)
    Ry_val = core.get_reg(Ry)
    core.set_reg(Rx, Ry_val)

def addi(core, inst):
    """Rx = Rx + imm{-1, 1, 4, 20, 32}"""
    s_reg = special_reg(inst)
    operand1 = core.get_reg(s_reg)
    operand2 = special_imm(inst)
    core.set_reg(special_reg(inst), operand1 + operand2)

def subi(core, inst):
    """Rx = Rx - imm"""
    s_reg = special_reg(inst)
    operand1 = core.get_reg(s_reg)
    operand2 = special_imm(inst)
    core.set_reg(special_reg(inst), operand1 - operand2)

def sub(core, inst):
    Rx = special_reg(inst)
    Ry = special_reg_y(inst)
    Rx_val = core.get_reg(Rx)
    Ry_val = core.get_reg(Ry)
    core.set_reg(Rx, Rx_val - Ry_val)

def sw(core, inst):
    Ry = special_reg_y(inst)
    address = core.get_reg(Ry)
    Rx = special_reg(inst)
    value = core.get_reg(Rx)
    core.set_mem(address, value)

def lw(core, inst):
    Rx = special_reg(inst)
    Ry = special_reg_y(inst)
    Ry_val = core.get_reg(Ry)

    load_val = core.get_mem(Ry_val)
    core.set_reg(Rx, load_val)

def bneRO(core, inst):
    #core.print_state()
    #input()
    offset = inst.get_offset()
    #print('Offset: {}'.format(offset))
    r0 = core.get_reg(0)
    #print('r0: {}'.format(r0))

    if offset < 0:
        offset = offset - 1

    if r0 != 0:
        core.set_offset(offset)

def sltR0(core, inst):
    Rx_val = core.get_reg(special_reg(inst))
    Ry_val = core.get_reg(special_reg_y(inst))
    #print('Rx_val: {}'.format(Rx_val))
    #print('Ry_val: {}'.format(Ry_val))
    if Rx_val < Ry_val:
        core.set_reg(0, 1)
        #print('Set r0 to 1')
    else:
        core.set_reg(0, 0)
        #print('Set r0 to 0')

def sll(core, inst):
    Rx = special_reg(inst)
    Rx_val = core.get_reg(Rx)
    imm = inst.get_imm()
    Rx_val = Rx_val << imm
    core.set_reg(Rx, Rx_val)

def halt(core, inst):
    core.set_offset(-1)

def nxt(core, inst):
    Rx = special_reg(inst)
    Ry = special_reg_y(inst)
    Rx_val = core.get_reg(Rx)
    Ry_val = core.get_reg(Ry)

    if Rx_val > 0:
        Rx_val = (-1 * Rx_val) - (Ry_val + 1)
    else:
        Rx_val = (-1 * Rx_val) + (Ry_val + 1)

    core.set_reg(Rx, Rx_val)

def mtc(core, inst):
    Rx = special_reg(inst)
    Ry = special_reg_y(inst)
    Rx_val = core.get_reg(Rx)
    Ry_val = core.get_reg(Ry)

    #print('Rx_val: {}'.format(Rx_val))
    #print('Ry_val: {}'.format(Ry_val))

    operand1_str = int_to_16bin_string(Rx_val)
    operand2_str = int_to_16bin_string(Ry_val)

    #print('Rx_bin: {}'.format(operand1_str))
    #print('Ry_bin: {}'.format(operand2_str))

    count = 0
    for i in range(len(operand1_str)):
        #print('operand1[{}] = {}'.format(i, operand1_str[i]), end='\t')
        #print('operand2[{}] = {}'.format(i, operand2_str[i]))
        if operand1_str[i] == operand2_str[i]:
            #print('Incremented')
            count += 1
    #print('Matches: {}'.format(count))
    core.set_reg(Rx, count)

def special_reg(inst):
    Rx = inst.get_rx()
    if Rx == 0:
        return 4
    else:
        return Rx
    # if inst.get_action() in reg_vals:
    #     return reg_vals[inst.get_action()][inst.get_rx()]
    # else:
    #     return inst.get_rx()

def special_reg_y(inst):
    Ry = inst.get_ry()
    if Ry == 0:
        return 4
    else:
        return Ry

    # if inst.get_action() in reg_vals:
    #     return reg_vals[inst.get_action()][inst.get_ry()]
    # else:
    #     return inst.get_ry()


imm_vals = {
    # Dict of dicts containing all 'special' immediate values
    # i.e. any value that is not its literal value.
    'addi': {
        0: 32,
        1: 1,
        2: 2,
        3: 3
    },
    'subi': {
        0: 31,
        1: 1,
        2: 2,
        3: 3
    },
    'beqR0': {
        0: -6,
        1: 1,
        2: 2,
        3: 3
    }
}



# reg_vals = {
#     # Dict of dicts containing all 'special' register values
#     # i.e. any register access that is not it's literal value.
#     'addi1': {
#         0: 8,
#         1: 9,
#         2: 10,
#         3: 19
#     },
#     'addi2': {
#         0: 15,
#         1: 10,
#         2: 17,
#         3: 13
#     },
#     'sw': {
#         0: 8,
#         1: 10,
#         2: 17,
#         3: 19
#     },
#     'sub': {
#         0: 8,
#         1: 0,
#         2: 17
#     },
#     'sltR01': {
#         0: 0,
#         1: 14,
#         2: 17,
#         3: 18
#     },
#     'sltR02': {
#         0: 0,
#         1: 8,
#     },
#     'add': {
#         0: 8,
#         1: 11,
#         2: 17,
#         3: 18
#     },
#     'sll': {
#         0: 0,
#         1: 14,
#         2: 2,
#         3: 3
#     },
#     'xor': {
#         0: 14,
#         1: 8,
#         2: 2,
#         3: 3
#     }
# }
# def beq(core, inst):
#     core._branch = core._branch + 1
#
#     operand1 = core._regs[inst.get_rs()]
#     operand2 = core._regs[inst.get_rt()]
#
#     if operand1 == operand2:
#         core._offset = inst.get_offset()
#
#
# def bne(core, inst):
#     core._branch = core._branch + 1
#
#     operand1 = core._regs[inst.get_rs()]
#     operand2 = core._regs[inst.get_rt()]
#
#     if operand1 != operand2:
#         core._offset = inst.get_offset()
#
# def addi(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = inst._rs
#     operand2 = inst._imm
#
#     op_val1 = core._regs[int(operand1, 2)]
#     op_val2 = inst.get_imm()
#
#     core._regs[inst.get_rt()] = op_val1 + op_val2
#
# def andi(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = inst._rs
#     operand2 = inst._imm
#
#     op_val1 = core._regs[int(operand1, 2)]
#     op_val2 = inst.get_imm()
#
#     core._regs[inst.get_rt()] = op_val1 & op_val2
#
#
# def ori(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = inst._rs
#     operand2 = inst._imm
#
#     op_val1 = core._regs[int(operand1, 2)]
#     op_val2 = int(operand2, 2)
#
#     core._regs[inst.get_rt()] = op_val1 | op_val2
#
#
# def lw(core, inst):
#     core._memory = core._memory + 1
#
#     mem_address = int((core._regs[inst.get_rs()] + inst.get_imm() - 0x2000) / 4)
#     core._regs[inst.get_rt()] = core._mem[mem_address]
#
#
# def sw(core, inst):
#     core._memory = core._memory + 1
#
#     #print('$rs = {}'.format(core._regs[inst.get_rs()]))
#     #print('Offset: {}'.format(inst.get_imm()))
#     mem_address = int((core._regs[inst.get_rs()] + inst.get_imm() - 0x2000) / 4)
#     #print('Mem Address: {}'.format(mem_address))
#     core._mem[mem_address] = core._regs[inst.get_rt()]
#     #core.print_state()
#     #print()
#
#
# def lui(core, inst):
#     core._ALU = core._ALU + 1
#
#     core._regs[inst.get_rt()] = inst.get_imm() << 16
#
#
# def sll(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = core._regs[inst.get_rt()]
#     operand2 = inst.get_shamt()
#
#     res = operand1 << operand2
#
#     if (res == 4294967296):
#         res = 0
#
#     core._regs[inst.get_rd()] = res
#
#
# def srl(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = core._regs[inst.get_rt()]
#     operand2 = inst.get_shamt()
#
#     res = operand1 >> operand2
#     core._regs[inst.get_rd()] = res
#
#
# def add(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = core._regs[inst.get_rs()]
#     operand2 = core._regs[inst.get_rt()]
#
#     core._regs[inst.get_rd()] = operand1 + operand2
#
#
# def sub(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = core._regs[inst.get_rs()]
#     operand2 = core._regs[inst.get_rt()]
#
#     core._regs[inst.get_rd()] = operand1 - operand2
#
#
# def and_(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = core._regs[inst.get_rs()]
#     operand2 = core._regs[inst.get_rt()]
#
#     core._regs[inst.get_rd()] = operand1 & operand2
#
#
# def or_(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = core._regs[inst.get_rs()]
#     operand2 = core._regs[inst.get_rt()]
#
#     core._regs[inst.get_rd()] = operand1 | operand2
#
# def xor(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = core._regs[inst.get_rs()]
#     operand2 = core._regs[inst.get_rt()]
#
#     core._regs[inst.get_rd()] = operand1 ^ operand2
#
# def nor(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = core._regs[inst.get_rs()]
#     operand2 = core._regs[inst.get_rt()]
#
#     core._regs[inst.get_rd()] = ~(operand1 | operand2)
#
#
# def slt(core, inst):
#     core._other = core._other + 1
#
#     operand1 = core._regs[inst.get_rs()]
#     operand2 = core._regs[inst.get_rt()]
#     if (operand1 < operand2):
#         core._regs[inst.get_rd()] = 1
#     else:
#         core._regs[inst.get_rd()] = 0
#
#
# def twos_comp(x):   # string x of 0/1
#     # find rightmost 1's index xxxx1000
#     rightmost1_idx = -1
#     for i in range(len(x)-1, -1, -1):
#         print(i)
#         if(x[i]=='1'):
#             rightmost1_idx = i
#             break
#     # print(f'rightmost 1 idx is {rightmost1_idx}')
#     y_same = x[rightmost1_idx:]
#     y_flip = ""
#     for i in range(rightmost1_idx):
#         y_flip += str(1-int(x[i]))
#     y = y_flip+y_same
#     return(y)
#
#
# def int_to_32bin_string(i):
#     if i>=0:
#         s = bin(i)[2:].zfill(32)
#     else:   # neg number
#         t = bin(0-i)[2:].zfill(32)
#         s = twos_comp(t)
#     return(s)
#
#
# def mtc(core, inst):
#     core._ALU = core._ALU + 1
#
#     operand1 = core._regs[inst.get_rs()]
#     operand2 = core._regs[inst.get_rt()]
#
#     operand1_str = int_to_32bin_string(operand1)
#     operand2_str = int_to_32bin_string(operand2)
#
#     count = 0
#     for i in range(len(operand1_str)):
#         if operand1_str[i] == operand2_str[i]:
#             count += 1
#
#     core._regs[inst.get_rd()] = count
#
#
# def j(core, inst):
#     core._jump = core._jump + 1
#     core._offset = inst.get_offset()
#     core._PC = -4
