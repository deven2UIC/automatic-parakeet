from math import log
from ctypes import *

class Memory:
    """Holds ana manages memory, including cache functionality and stats"""

    _config_dict = {
        0: {
            'N': 1,
            'S': 8,
            'b': 16
        },
        1: {
            'N': 8,
            'S': 1,
            'b': 16
        },
        2: {
            'N': 2,
            'S': 4,
            'b': 16
        },
        3: {
            'N': 4,
            'S': 2,
            'b': 16
        }
    }

    # Constants
    ADDRESS_BITS = 16
    DEBUG = True

    # Number of bits in each category
    _offset_bits = 0
    _set_bits = 0
    _tag_bits = 0

    # actual memory array, init to 0
    _mem = [0] * 65536

    # cache array
    _cache = []

    def __init__(self, config=0):
        # Configure memory
        self._N = self._config_dict[config]['N']  # N = number of ways
        self._S = self._config_dict[config]['S']  # S = number of sets
        self._b = self._config_dict[config]['b']  # b = block size (bytes)

        # Set address bit ranges
        self._offset_bits = int(log(self._b, 2))
        self._set_bits = int(log(self._S, 2))
        self._tag_bits = self.ADDRESS_BITS - self._offset_bits - self._set_bits

        if self.DEBUG:
            print('N={}\tS={}\tb={}'.format(self._N, self. _S, self._b))
            print('Tag Bits: {}\tSet Index Bits: {}\tOffset Bits: {}'.format(
                self._tag_bits, self._set_bits, self._offset_bits))

        # Initialize stats to 0
        _hit_count = 0
        _miss_count = 0
        _access_count = 0

        # Each cache object is instantiated and added to cache
        for i in range(self._S):
            self._cache.append(CacheBlock(self._N, self._b))

    def _read_cache(self, add):
        """Attempts cache read, returns boolean for result and a value"""
        # Retrive address components and convert to int
        tag, set_index, offset = self.int_to_bin_string(add)
        tag = int(tag, 2)
        set_index = int(set_index, 2)
        offset = int(offset, 2)

        if self.DEBUG:
            print('READ CACHE: Tag: {}\tSet: {}\tOffset: {}'.format(tag, set_index, offset))

        # Retrieve blocks corresponding to set index
        blocks = self._cache[set_index]
        # Ways are indexed by tag, so check if tag is in the ways dict
        if tag not in blocks.ways.keys():
            # print('Tag not found, automatic miss and creation of new way')
            # Retrieve correct block from memory
            mem_block = self._mem[add: add + self._b]

            # Assign memory block to LRU way
            blocks.set_LRU(tag, mem_block)
            print('\tCACHE MISS')
            return False, 0  # If tag is not present, automatic miss

        # print('Tag found checking if valid')
        valid, LRU, data = blocks.ways[tag]

        if valid:
            # print('Valid tag')
            blocks.update_LRU(tag)
            print('\tCACHE HIT')
        else:
            # print('Invalid tag')
            # Retrieve block from memory
            mem_block = self._mem[add: add + self._b]

            # Assign memory block to LRU way
            blocks.set_LRU(tag, mem_block)
            print('\tCACHE MISS')

        return valid, data[offset]  # Could still be miss, must check valid

    def _write_cache(self, add, write_data):
        """Attempts cache write, returns True if successful"""
        # Retrieve address components and convert to int
        tag, set_index, offset = self.int_to_bin_string(add)
        tag = int(tag, 2)
        set_index = int(set_index, 2)
        offset = int(offset, 2)

        if self.DEBUG:
            print('WRITE: Tag: {}\tSet: {}\tOffset: {}'.format(tag, set_index, offset))

        # Retrieve blocks corresponding to set index
        blocks = self._cache[set_index]

        if tag in blocks.ways.keys():
            # Retrieve entire block from cache
            valid, LRU, block_data = blocks.ways[tag]

            # If block is valid, write, else return false
            if valid:
                # print('Valid tag')
                blocks.update_LRU(tag)
                print('\tCACHE HIT')
            else:
                # print('Invalid tag')
                # Retrieve block from memory
                mem_block = self._mem[add: add + self._b]

                # Assign memory block to LRU way
                blocks.set_LRU(tag, mem_block)
                print('\tCACHE MISS')
        else:
            # print('Invalid tag')
            # Retrieve block from memory
            mem_block = self._mem[add: add + self._b]

            # Assign memory block to LRU way
            blocks.set_LRU(tag, mem_block)
            print('\tCACHE MISS')

    def read(self, add):
        """Reads value from mem/cache. Must be word aligned"""
        valid0, data0 = self._read_cache(add)
        valid1, data1 = self._read_cache(add + 1)
        valid2, data2 = self._read_cache(add + 2)
        valid3, data3 = self._read_cache(add + 3)

        val = 0
        if valid0:
            val += data0 << 24
            val += data1 << 16
            val += data2 << 8
            val += data3
        else:
            val = self._read_mem(add)

        return val

    def write(self, add, val):
        """Writes value to mem/cache. Must be word aligned"""
        byte = [0] * 4
        byte[0] = (val & 0xFF000000) >> 24
        byte[1] = (val & 0x00FF0000) >> 16
        byte[2] = (val & 0x0000FF00) >> 8
        byte[3] = (val & 0x000000FF)

        for i in range(4):
            self._mem[add + i] = byte[i]

        for i in range(4):
            self.write_byte(add + i, byte[i])

    def _read_mem(self, add):
        val = 0
        for i in range(4):
            val += self._mem[add + i] << (24 - i * 8)
        return val

    def _write_mem(self, add):
        val = 0
        for i in range(4):
            val += self._mem[add + i] << (24 - i * 8)
        return val

    def read_byte(self, add):
        """Reads byte value from memory with attempt at cache first"""
        valid, data = self._read_cache(add)

        if valid:
            return data  # valid bit is set, cache hit
        else:
            return self._mem[add]  # valid is not set, cache miss w/ mem access

    def write_byte(self, add, val):
        """Writes byte value to memory with attempt at cache first"""
        self._write_cache(add, val)
        self._mem[add] = val

    def read_mem_4byte(self, add):
        val0 = bin(self._mem[add])[2:].zfill(4)
        val1 = bin(self._mem[add + 1])[2:].zfill(4)
        val2 = bin(self._mem[add + 2])[2:].zfill(4)
        val3 = bin(self._mem[add + 3])[2:].zfill(4)
        val = val0 + val1 + val2 + val3

        val_int = 0
        if val[0] == '1':
            for i in range(len(val)):
                if val[i] == '0':
                    val_int += 2 ** (31 - i)
            val_int += 1
            val_int *= -1
        else:
            val_int = int(val, 2)

        return val_int

    def read_mem_block(self, add):
        block = self._mem[add: add + self._b * 4]

    # Tested
    def int_to_bin_string(self, add):
        """Takes int memory address and returns bin string"""
        # Convert to binary string
        add_bin = bin(add)[2:].zfill(self.ADDRESS_BITS)

        # Split and assign to each category
        tag = add_bin[:self._tag_bits]
        set_index = add_bin[self._tag_bits: self._tag_bits + self._set_bits]
        offset = add_bin[-1 * self._offset_bits:]
        # print('Tag: {}\tSet Ind: {}\tOffset: {}'.format(tag, set_index, offset))
        return tag, set_index, offset

    def print_cache(self):
        """Print formatted cache to screen"""
        print('===================Cache Contents====================')
        for i in range(len(self._cache)):
            print('Set Index: {}'.format(i))
            for way in self._cache[i].ways.items():
                tag, (valid, LRU, data) = way
                print('\tTag: {}\tValid: {}\tLRU: {}'.format(bin(tag)[2:].zfill(self._tag_bits), valid, LRU))
                print('\t{}'.format(data))
            print()
        print('=====================END CACHE======================\n')

    def print_mem(self):
        """Prints memory content."""
        print('Memory:')
        mem_val = 0
        count = 0
        for i in range(0, 256, 4):
            mem_val = self.read_mem_4byte(i)
            print('0x{:>2}: {:>5}'.format(hex(i)[2:], mem_val), end='\t')
            count += 1
            if count == 8:
                count = 0
                print()

class CacheBlock:
    """Holds an entire data block w/ multiple ways"""
    def __init__(self, ways, size):
        """Initialize block to 0s"""
        self.ways = {
            # tag : (valid, LRU, data)
        }
        for i in range(ways):
            data = [0] * (size / 4)
            # (valid, LRU, data)
            self.ways[i] = (False, 0, data)

    def update_LRU(self, used_tag):
        """Update LRU priority bits after cache hit DO NOT USE WITH MISS"""
        # Get list of LRU priorities
        LRU_list = [way[1] for way in self.ways.values()]

        # Get highest priority
        max_LRU = max(LRU_list)

        # Set LRU priority to max + 1
        (valid, LRU, data) = self.ways[used_tag]
        LRU = max_LRU + 1
        self.ways[used_tag] = (valid, LRU, data)

        # Decrement each priority so lowest is 0
        # This will indicate the LRU block
        min_LRU = min(LRU_list)
        if min_LRU > 0:
            for way in self.ways.values():
                (valid, LRU, data) = way
                LRU -= min_LRU
                way = (valid, LRU, data)

    def set_LRU(self, new_tag, mem_block):
        """Replace the LRU block, used after cache miss"""
        LRU_list = [way[1] for way in self.ways.values()]
        max_LRU = max(LRU_list)

        # Find way with lowest priority
        for way in self.ways.items():
            tag, (valid, LRU, data) = way

            if LRU == 0:
                # Delete LRU block
                del self.ways[tag]

                # Assign new block
                LRU = max_LRU + 1

                self.ways[tag] = (True, LRU, mem_block)
                break

        # Decrement each priority so lowest is 0
        # This will indicate the LRU block
        min_LRU = min(LRU_list)
        if min_LRU > 0:
            for way in self.ways.values():
                (valid, LRU, data) = way
                LRU -= min_LRU
                way = (valid, LRU, data)