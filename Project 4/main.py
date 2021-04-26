import ISA

def print_menu():
    print('Options:')
    print('\tStep >>        (enter)')
    print('\tStep <<        (.)')
    print('\tRun program    (run)')
    print('\tShow memory    (mem)')
    print('\tShow registers (regs)')
    print('\tShow stats     (stats)')
    print('\tGo to PC =     (PC=*)\tMust be multiple of 4, can\'t jump to previous loop iterations')
    print('\tEntry: ', end='')

def print_file_menu():
    print('Which file would you like to run?')
    print('\t1) Project 1')
    print('\t2) test')
    print('\t-1) Ext')

def print_mem_menu():
    print('Which memory configuration would you like to run?')
    print('\t1) N=1, S=8, b=16')
    print('\t2) N=8, S=1, b=16')
    print('\t3) N=2, S=4, b=16')
    print('\t4) N=4, S=2, b=16')
    val = input()
    return val

def main():
    print_file_menu()
    entry = int(input())
    program_file = ''

    while entry != '-1':
        if entry == 1:
            program_file = 'project1.txt'
        elif entry == 2:
            program_file = 'test.txt'

        mem_config = int(print_mem_menu()) - 1

        mips = ISA.ISA(program_file, 'output.txt', mem_config)

        print_menu()
        entry = input()
        print()

        while entry != '-1':
            if entry == "":
                mips.step()
            elif entry == '.':
                mips.step_back()
            elif entry == 'run':
                mips.run()
            elif entry == 'mem':
                mips.print_mem()
            elif entry == 'regs':
                mips.print_regs()
            elif entry == 'stats':
                mips.print_stats()
            elif entry[:3] == 'PC=':
                mips.goto_PC(int(entry[3:]))

            print_menu()
            entry = input()
            print()

        print_file_menu()
        entry = entry = int(input())


if __name__ == "__main__":
    main()