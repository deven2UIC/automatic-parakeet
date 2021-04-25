import Memory

mem = Memory.Memory(2)
# mem.print_cache()

mem.write(0, 1)
# print('Read Address: {}\tBin: {}'.format(0, bin(1)[2:].zfill(16)))
val = mem.read(0)
# print('Read Address: {}\tBin: {}'.format(0, bin(1)[2:].zfill(16)))
val = mem.read(0)
# mem.print_cache()

mem.write(2, 10)
# print('Read Address: {}\tBin: {}'.format(16, bin(10)[2:].zfill(16)))
val = mem.read(2)
# mem.print_cache()
# print('Read Address: {}\tBin: {}'.format(16, bin(10)[2:].zfill(16)))
val = mem.read(2)
# mem.print_cache()

mem.write(16, 10)
# print('Read Address: {}\tBin: {}'.format(16, bin(10)[2:].zfill(16)))
val = mem.read(16)
# mem.print_cache()
# print('Read Address: {}\tBin: {}'.format(16, bin(10)[2:].zfill(16)))
val = mem.read(16)
mem.print_cache()

# for i in range(100):
#     # print('Attempted Address: {}\tBin: {}'.format(i, bin(i)[2:].zfill(16)))
#     mem.write(i, i)
#
# for i in range(100):
#     # print('Attempted Address: {}\tBin: {}'.format(i, bin(i)[2:].zfill(16)))
#     val = mem.read(i)
#     if val == i:
#         print('valid read')
#     else:
#         print('INVALID READ')
#     mem.print_cache()
