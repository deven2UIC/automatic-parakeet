

class Instruction:
    """Instantiate with a hex string"""

    # Add i type instructions here {op : name}
    i_types = {'0000': 'init',
               '0001': 'init',
               '0010': 'init',
               '0011': 'init',
               '0100': 'addi1',
               '0101': 'addi2',
               '0111': 'beqR0',
               '1000': 'bneR0',
               '1010': 'sll',
               '1111': 'halt'
               }

    # Add r type instructions here {op : name}
    r_types = {'1001': 'sltR01',
               '1110': 'sltR02',
               '1011': 'xor',
               '1100': 'sub',
               '0110': 'sw',
               '1101': 'add'
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
        elif self._inst[:3] == 'beq':
            pass
        else:
            self._rx = self._bin[2:4][::-1]

        # Get value for imm
        if self._inst[:4] == 'addi' or self._inst == 'sll':
            self._imm = self._bin[:2][::-1]  # Take the last 2
        else:
            self._imm = self._bin[:4][::-1]  # Take the last 4

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
        if self._type == 'r':
            full = '{} ${}, ${}'.format(self._inst, int(self._rx, 2), int(self._ry, 2))
        elif self._type == 'i':
            full = '{} ${}, {}'.format(self._inst, int(self._rx, 2), int(self._imm, 2))
        print(full)

    def print_inst_true(self):
        """Prints inst as entered in text."""
        print(self._full)

    def get_inst(self):
        """Returns instruction as string."""
        if self._type == 'r':
            full = '{} ${}, ${}'.format(self._inst, special_reg(self), special_reg_y(self))
        elif self._type == 'i':
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

    def get_offset(self):
        return self._twos_comp(self._imm) << 2


"""
Helper functions and data for the operation functions
"""
def twos_comp(x):   # string x of 0/1
    # find rightmost 1's index xxxx1000
    rightmost1_idx = -1
    for i in range(len(x)-1, -1, -1):
        print(i)
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


def special_imm(inst):
    """Finds special immediate values for operation from dict"""
    if inst.get_action() in imm_vals:
        return imm_vals[inst.get_action()][inst.get_imm()]
    else:
        return inst.get_imm()

def special_reg(inst):
    if inst.get_action() in reg_vals:
        return reg_vals[inst.get_action()][inst.get_rx()]
    else:
        return inst.get_rx()

def special_reg_y(inst):
    if inst.get_action() in reg_vals:
        return reg_vals[inst.get_action()][inst.get_ry()]
    else:
        return inst.get_ry()


"""
Functions for each supported instructions. Each are indexed in a dictionary in the main 
program file where they can be called automatically.
"""
def init(core, inst):
    """Rx =- imm [-8,7]"""
    core.set_reg(inst.get_rx(), twos_comp(inst.get_imm()))

def addi1(core, inst):
    """Rx = Rx + imm{-1, 1, 4, 20, 32}"""
    s_reg = special_reg(inst)
    operand1 = core.get_reg(s_reg)
    operand2 = special_imm(inst)
    core.set_reg(special_reg(inst), operand1 + operand2)

def addi2(core, inst):
    s_reg = special_reg(inst)
    operand1 = core.get_reg(s_reg)
    operand2 = special_imm(inst)
    core.set_reg(special_reg(inst), operand1 + operand2)

def sw(core, inst):
    address = special_reg_y(inst)
    value = special_reg(inst)
    core.set_mem(address, value)

def beqR0(core, inst):
    offset = twos_comp(inst.get_imm())
    r0 = core.get_reg(0)
    if r0 == 0:
        core.set_offset(offset)

def bneRO(core, inst):
    offset = twos_comp(inst.get_imm())
    r0 = core.get_reg(0)
    if r0 != 0:
        core.set_offset(offset)

def sltR01(core, inst):
    Rx_val = core.get_reg(special_reg(inst))
    Ry_val = core.get_reg(special_reg_y(inst))
    if Rx_val < Ry_val:
        core.set_reg(0, 1)
    else:
        core.set_reg(0, 0)

def sltR02(core, inst):
    Rx_val = core.get_reg(special_reg(inst))
    Ry_val = core.get_reg(special_reg_y(inst))
    if Rx_val < Ry_val:
        core.set_reg(0, 1)
    else:
        core.set_reg(0, 0)

def sll(core, inst):
    Rx = special_reg(inst)
    Rx_val = core.get_reg(Rx)
    imm = twos_comp(inst.get_imm())
    Rx_val = Rx_val << (imm + 1)
    core.set_reg(Rx, Rx_val)

def xor(core, inst):
    Rx = special_reg(inst)
    Ry = special_reg_y(inst)
    Rx_val = core.get_reg(Rx)
    Ry_val = core.get_reg(Ry)

    # !!! vHIGHLY SUSPICIOUSv !!!
    result = Rx_val ^ Ry_val
    # !!! ^HIGHLY SUSPICIOUS^ !!!

    core.set_reg(Rx, result)

def sub(core, inst):
    Rx = special_reg(inst)
    Ry = special_reg_y(inst)
    Rx_val = core.get_reg(Rx)
    Ry_val = core.get_reg(Ry)

    result = Rx_val - Ry_val

    core.set_reg(Rx, result)

def add(core, inst):
    Rx = special_reg(inst)
    Ry = special_reg_y(inst)
    Rx_val = core.get_reg(Rx)
    Ry_val = core.get_reg(Ry)

    result = Rx_val + Ry_val

    core.set_reg(Rx, result)


def halt(core, inst):
    core.set_offset(-1)


imm_vals = {
    'addi1': {
        0: -23456,
        1: 305463004,
        2: 1,
        3: 0x2020
    },
    'addi2': {
        0: 32,
        1: 1,
        2: -1,
        3: 20
    },
    'bne': {
        0: 2,
        1: -5,
        2: 5,
        3: -29
    },
    'beq': {
        0: 4,
        1: 1,
        2: 2,
        3: 3
    }
}

reg_vals = {
    'addi1': {
        0: 8,
        1: 9,
        2: 10,
        3: 19
    },
    'addi2': {
        0: 15,
        1: 10,
        2: 17,
        3: 13
    },
    'sw': {
        0: 8,
        1: 10,
        2: 17,
        3: 19
    },
    'sub': {
        0: 8,
        1: 0,
        2: 17
    },
    'slt1': {
        0: 0,
        1: 14,
        2: 17,
        3: 18
    },
    'slt2': {
        0: 0,
        1: 8,
    },
    'add': {
        0: 8,
        1: 11,
        2: 17,
        3: 18
    }
}
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
