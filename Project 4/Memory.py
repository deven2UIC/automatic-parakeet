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
    ADDRESS_BITS = 32
    DEBUG = False

    # Number of bits in each category
    _offset_bits = 0
    _set_bits = 0
    _tag_bits = 0

    # actual memory array, init to 0
    _mem = [0] * 65536

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
        self._hit_count = 0
        self._miss_count = 0
        self._access_count = 0

        # cache array
        self._cache = []

        # Each cache object is instantiated and added to cache
        for i in range(self._S):
            self._cache.append(CacheBlock(self._N, self._b))

        self._output_file = open('log.txt', 'w')

    def read(self, add):
        """Reads value from mem/cache. Must be word aligned"""
        valid, val = self._read_cache(add)
        if not valid:
            val = self._read_mem(add)
            self._write_cache(add)
            self._miss_count += 1  # CACHE MISS
        else:
            self._hit_count += 1  # CACHE HIT
            pass

        self._access_count += 1
        self._output_file.write(
            '\tAccess Count: {}\tHit Count: {}\tMiss Count: {}\n\n'.format(self._access_count, self._hit_count,
                                                                         self._miss_count))
        return val

    def write(self, add, val):
        """Writes value to mem/cache. Must be word aligned"""
        self._write_mem(add, val)
        valid = self._write_cache(add)
        if valid:
            self._hit_count += 1
        else:
            self._miss_count += 1

        self._access_count += 1
        self._output_file.write(
            '\tAccess Count: {}\tHit Count: {}\tMiss Count: {}\n\n'.format(self._access_count, self._hit_count,
                                                                         self._miss_count))

    def _read_cache(self, add):
        """Attempts cache read, returns boolean for result and a value"""
        # Retrive address components and convert to int
        tag_bin, set_index_bin, offset_bin = self.int_to_bin_string(add)
        tag = int(tag_bin, 2)
        if self._set_bits == 0:
            set_index = 0
        else:
            set_index = int(set_index_bin, 2)
        offset = int(offset_bin, 2)

        if self.DEBUG:
            print('READ CACHE: Address: {}\tTag: {}\tSet: {}\tOffset: {}'.format(add, tag, set_index, offset))

        # Retrieve blocks corresponding to set index
        blocks = self._cache[set_index]
        # Ways are indexed by tag, so check if tag is in the ways dict
        if tag not in blocks.ways.keys():
            # Retrieve correct block from memory
            mem_block = self._mem[add: add + self._b]

            # Assign memory block to LRU way
            replaced_tag = blocks.overwrite_LRU(tag, mem_block)
            return False, 0  # If tag is not present, automatic miss

        # print('Tag found checking if valid')
        valid, LRU, data = blocks.ways[tag]

        if valid:
            blocks.update_LRU(tag)  # Update LRU after hit
            replaced_tag = tag
        else:
            # Retrieve block from memory
            mem_block = self._mem[add: add + self._b]

            # Assign memory block to LRU way
            replaced_tag = blocks.overwrite_LRU(tag, mem_block)

        val = self._list_to_int(data[offset: offset + 4])

        if valid:
            outcome = 'HIT'
            self._output_file.write('CACHE READ\tADDRESS: {}\\{}\n'.format(bin(add), hex(add)))
            self._output_file.write('\tOutcome: {}\n'.format(outcome))
        else:
            outcome = 'MISS'
            self._output_file.write('CACHE READ\tADDRESS: {}\\{}\n'.format(bin(add), hex(add)))
            self._output_file.write('\tOutcome: {}\tReplaced Tag: {}\n'.format(outcome, replaced_tag))

        return valid, val  # Could still be miss, must check valid

    def _write_cache(self, add):
        """Attempts cache write, returns True if successful"""
        # Retrive address components and convert to int
        tag_bin, set_index_bin, offset_bin = self.int_to_bin_string(add)
        tag = int(tag_bin, 2)
        if self._set_bits == 0:
            set_index = 0
            set_index_bin = '0b0'
        else:
            set_index = int(set_index_bin, 2)
        offset = int(offset_bin, 2)

        # Retrieve blocks corresponding to set index
        blocks = self._cache[set_index]
        # Get new block from memory (just updated)
        new_block = self._mem[add: add + self._b]

        if tag not in blocks.ways.keys():
            # Overwrite LRU block
            replaced_tag = blocks.overwrite_LRU(tag, new_block)
            success = False
        else:
            # Overwrite same outdate block
            success = blocks.overwrite_block(tag, new_block)
            replaced_tag = tag

        if success:
            outcome = 'HIT'
            self._output_file.write('CACHE READ\tADDRESS: {}\\{}\n'.format(bin(add), hex(add)))
            self._output_file.write('\tOutcome: {}\n'.format(outcome))
        else:
            outcome = 'MISS'
            self._output_file.write('CACHE READ\tADDRESS: {}\\{}\n'.format(bin(add), hex(add)))
            self._output_file.write('\tOutcome: {}\tReplaced Tag: {}\n'.format(outcome, replaced_tag))

        return success

    def _read_mem(self, add):
        """Reads 4 byte block from memory"""
        val_list = self._mem[add: add + 4]
        return self._list_to_int(val_list)

    # Tested
    def _write_mem(self, add, val):
        """Writes 4 byte block to memory"""
        if val < 0:
            val = (val + 1) * -1
            val_bin = bin(val)[2:].zfill(32)
            val_new = ''
            for i in range(len(val_bin)):
                if val_bin[i] == '0':
                    val_new += '1'
                else:
                    val_new += '0'
            val_bin = val_new
        else:
            val_bin = bin(val)
            val_bin = val_bin[2:].zfill(32)

        for i in range(4):
            self._mem[add + i] = int( val_bin[i * 8: (i * 8) + 8], 2 )

    # Tested
    def int_to_bin_string(self, add):
        """Takes int memory address and cache address bin string (tag/set index/offset)"""
        # Convert to binary string
        add_bin = bin(add)[2:].zfill(self.ADDRESS_BITS)

        # Split and assign to each category
        tag = add_bin[:self._tag_bits]
        set_index = add_bin[self._tag_bits: self._tag_bits + self._set_bits]
        offset = add_bin[-1 * self._offset_bits:]
        # print('Tag: {}\tSet Ind: {}\tOffset: {}'.format(tag, set_index, offset))
        return tag, set_index, offset

    # Tested
    def _list_to_int(self, val):
        val0 = bin(val[0])[2:].zfill(8)
        val1 = bin(val[1])[2:].zfill(8)
        val2 = bin(val[2])[2:].zfill(8)
        val3 = bin(val[3])[2:].zfill(8)
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

    def print_cache(self):
        """Print formatted cache to screen"""
        print('===================Cache Contents====================')
        self.print_stats()
        for i in range(len(self._cache)):
            print('Set Index: {}'.format(i))
            for way in self._cache[i].ways.items():
                tag, (valid, LRU, data) = way
                print('\tTag: {}\tValid: {}\tLRU: {}'.format(bin(tag)[2:].zfill(self._tag_bits), valid, LRU))
                print('\t{}'.format(data))
        print('=====================END CACHE======================\n')

    def print_cache_log(self):
        """Print formatted cache to screen"""
        self._output_file.write('===================Cache Contents====================\n')
        self.print_stats()
        for i in range(len(self._cache)):
            self._output_file.write('Set Index: {}\n'.format(i))
            for way in self._cache[i].ways.items():
                tag, (valid, LRU, data) = way
                self._output_file.write('\tTag: {}\tValid: {}\tLRU: {}\n'.format(bin(tag)[2:].zfill(self._tag_bits), valid, LRU))
                self._output_file.write('\t{}\n'.format(data))
        self._output_file.write('=====================END CACHE======================\n\n')

    def print_mem(self):
        """Prints memory content."""
        print('===================Mem Contents====================')
        mem_val = 0
        count = 0
        for i in range(0, 256, 4):
            mem_val = self._read_mem(i)
            print('0x{:>2}: {:>5}'.format(hex(i)[2:], mem_val), end='\t')
            count += 1
            if count == 8:
                count = 0
                print()
        print('=====================END MEM======================\n')

    def print_mem_log(self):
        """Prints memory content."""
        self._output_file.write('===================Mem Contents====================\n')
        mem_val = 0
        count = 0
        for i in range(0, 256, 4):
            mem_val = self._read_mem(i)
            self._output_file.write('0x{:>2}: {:>5}\t'.format(hex(i)[2:], mem_val))
            count += 1
            if count == 8:
                count = 0
                self._output_file.write('\n')
        self._output_file.write('=====================END MEM======================\n\n')

    def print_stats(self):
        print('Access Count: {}\tHit Count: {}\tMiss Count: {}'.format(self._access_count, self._hit_count, self._miss_count))

    def close_log(self):
        self._output_file.close()

class CacheBlock:
    """Holds an entire data block w/ multiple ways"""
    def __init__(self, ways, size):
        """Initialize block to 0s"""
        self.ways = {
            # tag : (valid, LRU, data)
        }
        for i in range(ways):
            data = [0] * size
            # (valid, LRU, data)
            self.ways[i] = (False, 0, data)

    def update_LRU(self, used_tag):
        """Update LRU priority bits after cache hit DO NOT USE WITH MISS"""
        if len(self.ways) > 1:
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
                for way in self.ways.items():
                    tag, (valid, LRU, data) = way
                    LRU -= min_LRU
                    self.ways[tag] = (valid, LRU, data)

    def overwrite_LRU(self, new_tag, mem_block):
        """Replace the LRU block, used after cache miss"""
        replaced_tag = ''
        if len(self.ways) > 1:
            LRU_list = [way[1] for way in self.ways.values()]
            max_LRU = max(LRU_list)

            # Find way with lowest priority
            for way in self.ways.items():
                tag, (valid, LRU, data) = way

                if LRU == 0:
                    # Delete LRU block
                    del self.ways[tag]
                    replaced_tag = tag
                    # Assign new block
                    LRU = max_LRU + 1

                    self.ways[new_tag] = (True, LRU, mem_block)
                    break

            # Decrement each priority so lowest is 0
            # This will indicate the LRU block
            min_LRU = min(LRU_list)
            if min_LRU > 0:
                for way in self.ways.items():
                    tag, (valid, LRU, data) = way
                    LRU -= min_LRU
                    self.ways[tag] = (valid, LRU, data)
        else:
            self.ways[new_tag] = (True, 0, mem_block)
            replaced_tag = new_tag

        return replaced_tag

    def overwrite_block(self, new_tag, mem_block):
        """Overwrite block with existing tag"""
        (valid, LRU, data) = self.ways[new_tag]
        if len(self.ways) > 1:
            LRU_list = [way[1] for way in self.ways.values()]
            max_LRU = max(LRU_list)
            self.ways[new_tag] = (True, max_LRU + 1, mem_block)
        else:
            self.ways[new_tag] = (True, 0, mem_block)
        self.update_LRU(new_tag)
        return valid
