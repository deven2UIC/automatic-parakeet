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
    print('\t2) Project 1 w/ special operation')
    print('\t3) ALU Test')
    print('\t4) Branch Test')
    print('\t5) Mem Access Test')
    print('\t6) Special Instruction Test')
    print('\t-1) Ext')


print_file_menu()
entry = int(input())
program_file = ''

while entry != '-1':
    if entry == 1:
        program_file = 'project1.txt'
    elif entry == 2:
        program_file = 'project1special.txt'
    elif entry == 3:
        program_file = 'ALU_hex.txt'
    elif entry == 4:
        program_file = 'branch_hex.txt'
    elif entry == 5:
        program_file = 'memaccess_hex.txt'
    elif entry == 6:
        program_file = 'special_hex.txt'

    mips = ISA.ISA(program_file, 'p1-special-mc.txt')

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
