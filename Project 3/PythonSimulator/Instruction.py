
class Instruction:
    '''Instantiate with a hex string'''

    # Add i type instructions here {op : name}
    i_types = {'000100': 'beq',
               '000101': 'bne',
               '001000': 'addi',
               '001100': 'andi',
               '001101': 'ori',
               '100011': 'lw',
               '101011': 'sw',
               '001111': 'lui'}

    # Add r type instructions here {op : name}
    r_types = {'000000': 'sll',
               '000010': 'srl',
               '100000': 'add',
               '100010': 'sub',
               '100100': 'and',
               '100101': 'or',
               '101010': 'slt',
               '111111': 'mtc',
               '100110': 'xor',
               '100111': 'nor'}

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
        self._shamt = ''
        self._imm = ''

        self._hex = inst_hex
        self._bin = bin(int(self._hex, 16))[2:].zfill(32)
        self._bin = self._bin[::-1]

        self._to_MIPS()

    def _to_MIPS(self):
        """Convert hex/bin instruction to MIPS text."""
        self._opcode = self._bin[26:][::-1]

        if self._opcode == '000000':
            self._r_type()
        elif self._opcode == '000010':
            self._j_type()
        else:
            self._i_type()

    def _r_type(self):
        """Converts r-types, only called internally."""
        self._type = 'r'

        self._rs = self._bin[21:26][::-1]
        self._rt = self._bin[16:21][::-1]
        self._rd = self._bin[11:16][::-1]
        self._shamt = self._bin[6:11][::-1]
        self._func = self._bin[:6][::-1]

        self._inst = self.r_types[self._func]

        if self._inst == 'sll' or self._inst == 'srl':
            self._full = '{} ${}, ${}, {}'.format(self._inst, int(self._rd, 2), int(self._rt, 2), self._twos_comp(self._shamt))
        else:
            self._full = '{} ${}, ${}, ${}'.format(self._inst, int(self._rd, 2), int(self._rs, 2), int(self._rt, 2))

    def _i_type(self):
        """Converts i-types, only called internally."""
        self._type = 'i'

        self._rs = self._bin[21:26][::-1]
        self._rt = self._bin[16:21][::-1]
        self._imm = self._bin[:16][::-1]

        self._inst = self.i_types[self._opcode]

        if self._inst == 'sw' or self._inst == 'lw':
            self._full = '{} ${}, {}(${})'.format(self._inst, int(self._rt, 2), self._twos_comp(self._imm), self._twos_comp(self._rs))
        else:
            self._full = '{} ${}, ${}, {}'.format(self._inst, int(self._rt, 2), int(self._rs, 2), self._twos_comp(self._imm))

    def _j_type(self):
        """Converts j-types, only called internally."""
        self._type = 'j'

        self._imm = self._bin[0:26][::-1]
        self._inst = self.j_types[self._opcode]

        self._full = '{} {}'.format(self._inst, self._imm)

    def _twos_comp(self, b):
        """Returns twos comp of bin string, returns int."""
        if (b[0] == '0'):
            return int(b, 2)
        val = 0

        for i in range(len(b)):
            if (b[(len(b) - 1) - i] == '0'):
                val += (2 ** i)

        return -1 * (val + 1)

    def print_all(self):
        """Prints instruction and all binary/hex field info."""
        print('Hex: {}'.format(self._hex))
        print('Bin: 0b{}'.format(self._bin))

        if self._type == 'r':
            print('Func: {}'.format(self._func))
            print('$rs: {}'.format(self._rs))
            print('$rt: {}'.format(self._rt))
            print('$rd: {}'.format(self._rd))
            print('Inst: {}'.format(self._inst))
            print('Full: {}'.format(self._full))
        elif self._type == 'i':
            print('Opcode: {}'.format(self._opcode))
            print('$rs: {}'.format(self._rs))
            print('$rt: {}'.format(self._rt))
            print('imm: {}'.format(self._imm))
            print('Inst: {}'.format(self._inst))
            print('Full: {}'.format(self._full))
        else:
            pass

    def print_inst(self):
        """Prints inst in MIPS text."""
        print('{}'.format(self._full))

    def get_inst(self):
        """Returns instruction as string."""
        return self._full

    def get_action(self):
        """Returns corresponding function name for instruction."""
        return self._inst

    def get_rs(self):
        """Returns int value for field $rs."""
        return int(self._rs, 2)

    def get_rt(self):
        """Returns int value for field $rt."""
        return int(self._rt, 2)

    def get_rd(self):
        """Returns int value for field $rd."""
        return int(self._rd, 2)

    def get_shamt(self):
        """Returns int value for field shamt."""
        return self._twos_comp(self._shamt)

    def get_imm(self):
        """Returns int value for immediate field."""
        return self._twos_comp(self._imm)

    def get_offset(self):
        return self._twos_comp(self._imm) << 2

"""
Functions for each supported instructions. Each are indexed in a dictionary in the main 
program file where they can be called automatically.
"""
def beq(core, inst):
    core._branch = core._branch + 1

    operand1 = core._regs[inst.get_rs()]
    operand2 = core._regs[inst.get_rt()]

    if operand1 == operand2:
        core._offset = inst.get_offset()


def bne(core, inst):
    core._branch = core._branch + 1

    operand1 = core._regs[inst.get_rs()]
    operand2 = core._regs[inst.get_rt()]

    if operand1 != operand2:
        core._offset = inst.get_offset()

def addi(core, inst):
    core._ALU = core._ALU + 1

    operand1 = inst._rs
    operand2 = inst._imm

    op_val1 = core._regs[int(operand1, 2)]
    op_val2 = inst.get_imm()

    core._regs[inst.get_rt()] = op_val1 + op_val2

def andi(core, inst):
    core._ALU = core._ALU + 1

    operand1 = inst._rs
    operand2 = inst._imm

    op_val1 = core._regs[int(operand1, 2)]
    op_val2 = inst.get_imm()

    core._regs[inst.get_rt()] = op_val1 & op_val2


def ori(core, inst):
    core._ALU = core._ALU + 1

    operand1 = inst._rs
    operand2 = inst._imm

    op_val1 = core._regs[int(operand1, 2)]
    op_val2 = int(operand2, 2)

    core._regs[inst.get_rt()] = op_val1 | op_val2


def lw(core, inst):
    core._memory = core._memory + 1

    mem_address = int((core._regs[inst.get_rs()] + inst.get_imm() - 0x2000) / 4)
    core._regs[inst.get_rt()] = core._mem[mem_address]


def sw(core, inst):
    core._memory = core._memory + 1

    #print('$rs = {}'.format(core._regs[inst.get_rs()]))
    #print('Offset: {}'.format(inst.get_imm()))
    mem_address = int((core._regs[inst.get_rs()] + inst.get_imm() - 0x2000) / 4)
    #print('Mem Address: {}'.format(mem_address))
    core._mem[mem_address] = core._regs[inst.get_rt()]
    #core.print_state()
    #print()


def lui(core, inst):
    core._ALU = core._ALU + 1

    core._regs[inst.get_rt()] = inst.get_imm() << 16


def sll(core, inst):
    core._ALU = core._ALU + 1

    operand1 = core._regs[inst.get_rt()]
    operand2 = inst.get_shamt()

    res = operand1 << operand2

    if (res == 4294967296):
        res = 0

    core._regs[inst.get_rd()] = res


def srl(core, inst):
    core._ALU = core._ALU + 1

    operand1 = core._regs[inst.get_rt()]
    operand2 = inst.get_shamt()

    res = operand1 >> operand2
    core._regs[inst.get_rd()] = res


def add(core, inst):
    core._ALU = core._ALU + 1

    operand1 = core._regs[inst.get_rs()]
    operand2 = core._regs[inst.get_rt()]

    core._regs[inst.get_rd()] = operand1 + operand2


def sub(core, inst):
    core._ALU = core._ALU + 1

    operand1 = core._regs[inst.get_rs()]
    operand2 = core._regs[inst.get_rt()]

    core._regs[inst.get_rd()] = operand1 - operand2


def and_(core, inst):
    core._ALU = core._ALU + 1

    operand1 = core._regs[inst.get_rs()]
    operand2 = core._regs[inst.get_rt()]

    core._regs[inst.get_rd()] = operand1 & operand2


def or_(core, inst):
    core._ALU = core._ALU + 1

    operand1 = core._regs[inst.get_rs()]
    operand2 = core._regs[inst.get_rt()]

    core._regs[inst.get_rd()] = operand1 | operand2

def xor(core, inst):
    core._ALU = core._ALU + 1

    operand1 = core._regs[inst.get_rs()]
    operand2 = core._regs[inst.get_rt()]

    core._regs[inst.get_rd()] = operand1 ^ operand2

def nor(core, inst):
    core._ALU = core._ALU + 1

    operand1 = core._regs[inst.get_rs()]
    operand2 = core._regs[inst.get_rt()]

    core._regs[inst.get_rd()] = ~(operand1 | operand2)


def slt(core, inst):
    core._other = core._other + 1

    operand1 = core._regs[inst.get_rs()]
    operand2 = core._regs[inst.get_rt()]
    if (operand1 < operand2):
        core._regs[inst.get_rd()] = 1
    else:
        core._regs[inst.get_rd()] = 0


def twos_comp(x):   # string x of 0/1
    # find rightmost 1's index xxxx1000
    rightmost1_idx = -1
    for i in range(len(x)-1, -1, -1):
        print(i)
        if(x[i]=='1'):
            rightmost1_idx = i
            break
    # print(f'rightmost 1 idx is {rightmost1_idx}')
    y_same = x[rightmost1_idx:]
    y_flip = ""
    for i in range(rightmost1_idx):
        y_flip += str(1-int(x[i]))
    y = y_flip+y_same
    return(y)


def int_to_32bin_string(i):
    if i>=0:
        s = bin(i)[2:].zfill(32)
    else:   # neg number
        t = bin(0-i)[2:].zfill(32)
        s = twos_comp(t)
    return(s)


def mtc(core, inst):
    core._ALU = core._ALU + 1

    operand1 = core._regs[inst.get_rs()]
    operand2 = core._regs[inst.get_rt()]

    operand1_str = int_to_32bin_string(operand1)
    operand2_str = int_to_32bin_string(operand2)

    count = 0
    for i in range(len(operand1_str)):
        if operand1_str[i] == operand2_str[i]:
            count += 1

    core._regs[inst.get_rd()] = count


def j(core, inst):
    core._jump = core._jump + 1
    core._offset = inst.get_offset()
    core._PC = -4
