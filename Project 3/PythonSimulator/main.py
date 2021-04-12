import Instruction
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
    print('\t 1) Escape Array')
    print('\t 2) Target Match')
    print('\t 3) Full project 3')
    print('\t 4) N/A')
    print('\t 5) N/A')
    print('\t 6) N/A')
    print('\t-1) Exit')


print_file_menu()
entry = int(input())
program_file = ''

while entry != -1:
    if entry == 1:
        program_file = 'escape_array.txt'
    elif entry == 2:
        program_file = 'target_match.txt'
    elif entry == 3:
        program_file = 'all.txt'
    elif entry == 4:
        program_file = 'branch_hex.txt'
    elif entry == 5:
        program_file = 'memaccess_hex.txt'
    elif entry == 6:
        program_file = 'special_hex.txt'

    engine = ISA.ISA(program_file, 'p1-special-mc.txt')

    print_menu()
    entry = input()
    print()
    while entry != '-1':
        if (entry == ""):
            engine.step()
        elif entry == '.':
            engine.step_back()
        elif entry == 'run':
            engine.run()
        elif entry == 'mem':
            engine.print_mem()
        elif entry == 'regs':
            engine.print_regs()
        elif entry == 'stats':
            engine.print_stats()
        elif entry[:3] == 'PC=':
            engine.goto_PC(int(entry[3:]))

        print_menu()
        entry = input()
        print()

    print_file_menu()
    entry = entry = int(input())
