import Instruction


class ISA:
    _regs = [0] * 20  # 20 registers
    _mem = [0] * 256  # 256 memory locations
    _mem_history = {}
    _regs_history = {}

    _total = 0
    _ALU = 0
    _jump = 0
    _branch = 0
    _memory = 0
    _other = 0

    class ProgramState:
        """Holds previous program states including register/memory content and stats"""
        regs = [0] * 20  # 20 registers
        mem = [0] * 256  # 256 memory locations

        total = 0
        ALU = 0
        jump = 0
        branch = 0
        memory = 0
        other = 0

        def __init__(self, regs, mem, total, alu, jump, branch, memory, other):
            regs = regs
            mem = mem
            total = total
            ALU = alu
            jump = jump
            branch = branch
            memory = memory
            other = other

    _state_history = {}

    _actions = {'init': Instruction.init,
                'addi1': Instruction.addi1,
                'addi2': Instruction.addi2,
                'sw': Instruction.sw,
                'beqR0': Instruction.beqR0,
                'bneRO': Instruction.bneRO,
                'sltR01': Instruction.sltR01,
                'sltR02': Instruction.sltR02,
                'sll': Instruction.sll,
                'xor': Instruction.xor,
                'sub': Instruction.sub,
                'add': Instruction.add,
                'halt': Instruction.halt,
                }

    def __init__(self, in_filename, out_filename):
        # Set initial values for MIPS engine
        self._offset = 0
        self._program = {}
        self._PC = 0

        # Read in hex file
        self._f = open(in_filename)
        inst_all = self._f.read()
        inst_temp = inst_all.split('\n')

        # Store all instructions by initializing Instruction objects into _program dictionary
        # indexed by _PC
        self._program_len = len(inst_temp)
        self._PC_last = self._program_len - 1
        print('# instructions: {}\tLast Instruction: {}'.format(len(inst_temp), self._PC_last))
        for i in range(0, len(inst_temp)):
            self._program[self._PC] = Instruction.Instruction(inst_temp[i])
            self._PC = self._PC + 1

        # Output assembly file
        self._output_f = open(out_filename, 'w')
        for key in self._program:
            self._program[key].print_inst()
            self._output_f.write(self._program[key].get_inst() + '\n')
        self._output_f.close()

        print()
        self._PC = 0
        #self.print_state()
        self._save_cur_state()

    def run(self):
        """Runs until _PC executes last instruction."""
        can_run = True
        while can_run:
            cur_inst = self._program[self._PC]
            #print('PC: {}\t{}'.format(self._PC, cur_inst.get_inst()))
            can_run = self._step()

        print("Program terminated successfully, printing end state...PC={}".format(self._PC))
        self.print_state()

    def _step(self):
        """Runs the next instruction."""
        cur_inst = self._program[self._PC]  # Set current instruction
        #print('PC: {}\t{}'.format(self._PC, cur_inst.get_inst()))
        self._actions[self._program[self._PC].get_action()](self, self._program[self._PC])  # Execute instruction
        self._regs[0] = 0  # $0 = 0 always
        self._PC = self._PC + self._offset + 1  # Increment PC
        self._offset = 0  # Return offset to 0 after potential branch
        self._total = self._total + 1

        self._save_cur_state()

        if self._PC > self._PC_last:
            self._PC = self._PC_last
            return False
        else:
            return True

    def step(self):
        """Runs the next instruction."""
        # End condition and program close
        if self._PC > self._PC_last:
            self._PC = self._PC_last
            print("Program terminated successfully, printing end state...PC={}".format(self._PC))
            self._save_cur_state()
            #self.print_state()
            return

        # Program run
        cur_inst = self._program[self._PC]  # Set current instruction
        self.print_state()
        self._actions[self._program[self._PC].get_action()](self, self._program[self._PC])  # Execute instruction
        self._regs[0] = 0  # $0 = 0 always
        self._PC = self._PC + self._offset + 1  # Increment PC
        self._offset = 0  # Return offset to 0 after potential branch
        self._total = self._total + 1

        self._save_cur_state()

    def step_back(self):
        """Returns to the previous instruction."""
        if self._PC > 0:
            self._load_state(self._PC - 1)
            self.print_state()
        else:
            print('Error: Already at beginning\n')

    def _save_cur_state(self):
        # regs, mem, total, alu, jump, branch, memory, other)
        _cur_state = self.ProgramState(self._regs, self._mem, self._total, self._ALU, self._jump,
                                       self._branch, self._memory, self._other)

        _cur_state.regs = self._regs
        _cur_state.mem = self._mem
        _cur_state.total = self._total
        _cur_state.ALU = self._ALU
        _cur_state.jump = self._jump
        _cur_state.branch = self._branch
        _cur_state.memory = self._memory
        _cur_state.other = self._other

        self._state_history[self._PC] = _cur_state

    def _load_state(self, pc):
        self._PC = pc
        self._mem = self._state_history[pc].mem
        self._regs = self._state_history[pc].regs
        self._total = self._state_history[pc].total
        self._ALU = self._state_history[pc].ALU
        self._jump = self._state_history[pc].jump
        self._branch = self._state_history[pc].branch
        self._memory = self._state_history[pc].memory
        self._other = self._state_history[pc].other

    def goto_PC(self, pc):
        """Brings program to specified pc, after execution."""
        if (pc & 0b00) != 0:
            print('Error: PC must be multiple of 4.')

        if pc in self._state_history.keys():
            self._load_state(pc)
            self.print_state()
        else:
            print('Error: program has not yet reached this point.\n')

    def print_mem(self):
        """Prints memory content."""
        print('Memory:')
        mem_index = 0
        for i in range(0, len(self._mem), 0x20):
            for j in range(0, 0x20, 4):
                print('{}: {:5d}'.format(hex(i + j + 0x2000), self._mem[mem_index]), end='\t')
                mem_index = mem_index + 1
            print()

    def print_regs(self):
        """Prints register content."""
        print('Registers:')
        for i in range(0, 8):
            print('${} = {}'.format(i, self._regs[i]), end='\t')
        print()

        for i in range(8, 12):
            print('${} = {}'.format(i, self._regs[i]), end='\t')
        print()

        for i in range(8, 20):
            print('${} = {}'.format(i, self._regs[i]), end='\t')
        print()

    def set_reg(self, reg, val):
        """Set register reg with 'val'"""
        self._regs[reg] = val

    def get_reg(self, reg):
        """Get value of register 'reg'"""
        return self._regs[reg]

    def set_mem(self, add, val):
        """Set value of memory address 'add' with value 'val'"""
        pass

    def get_mem(self, add):
        """Get value of memory address 'add'"""
        pass

    def print_stats(self):
        """Prints stats for instruction count/usage."""
        print('Total : {}'.format(self._total))
        print('ALU   : {}'.format(self._ALU))
        print('Jump  : {}'.format(self._jump))
        print('Branch: {}'.format(self._branch))
        print('Memory: {}'.format(self._memory))
        print('Other : {}'.format(self._other))

    def print_state(self):
        print('********************** Program State at PC = {} **********************'.format(self._PC))
        if self._PC > 0:
            prev_inst = self._program[self._PC - 1].get_inst()  # Set current instruction
        else:
            prev_inst = 'No previous'
        cur_inst = self._program[self._PC]  # Set current instruction

        print('PC: {}\tJust executed: {}\tLoaded instruction: {}'.format(self._PC, prev_inst, cur_inst.get_inst()))
        self.print_regs()
        self.print_mem()
        self.print_stats()
        print('********************** Program State END ******************************\n'.format(self._PC))