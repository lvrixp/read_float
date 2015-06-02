#!/usr/bin/python

'''A tool to read float numbers from input file or pipe \
        and prompt total count and sum.
'''

import sys
import os
from optparse import OptionParser
import locale
import mmap

# items that will be exported
__all__ = ["count_and_sum"]

VERSION = 0.1

PROMPTMSG = \
'''\
Total count = %s
Sum of all  = %s
'''

def count_and_sum(iterable):
    '''count_and_sum(iterable)

    Accept character iterator, of which each item is a character, \
    and scan all float numbers to get the total count and sum.
    It may raise exception if there's item can't be recognized as float.

    Args:
        iterable: an iterator, each element is a character

    Returns:
        A pair that contains the count and sum of all the float been scanned

    Raises:
        ValueError: item that can be recognized as float is found
    '''
    # record the total count of float numbers
    total = [0]

    # handle special case that can't be handled by float()
    # eg. 10,000
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    def is_seperator(character):
        '''check whether a character is seperator
        '''
        return character in [' ', os.linesep, '\t']

    def item_generator(iterable, total):
        '''item_generator(iterable, total):

        Create a generator object.
        Each item in the generator is a float.
        After generator been iterated, total count of items will be set to total[0].
        '''

        # try to read 64K each time
        # need to test for optimal value of chunk size
        CHUNKSIZE = 64*1024
        start = 0
        end = 0
        while start < len(iterable):
            end = min(start + CHUNKSIZE, len(iterable))

            # end will point to next seperator
            while end < len(iterable) and not is_seperator(iterable[end]):
                end += 1
    
            for item in iterable[start:end].split():
                # add the count of item
                total[0] += 1
    
                # try to convert the item to float
                try:
                    res = float(item)
                except ValueError:
                    # if it fail, try to use locale
                    # if locale still fail, it raises ValueError
                    res = locale.atof(item)
    
                yield res

            # continue to scan another item
            start = end
    
    all_items = item_generator(iterable, total)

    #sum of all the float numbers
    try:
        sum_all = reduce(lambda a, b: a + b, all_items)
    except TypeError:
        # nothing in the 'all_items'
        return 0, 0.0

    return total[0], sum_all

def get_file_path():
    '''Check the input arguments for the file path
    '''
    parser = OptionParser()
    parser.add_option("-f", "--filepath", dest='file_path', \
                            help="file path to be read")
    options, _ = parser.parse_args()

    if options.file_path is None or not os.path.isfile(options.file_path):
        parser.print_help()
        raise ValueError("Invalid file path: %s" % options.file_path)

    return options.file_path

def main():
    '''Main function of the tool
    '''
    try:
        file_path = get_file_path()
        with open(file_path, 'r+') as fin:
            # use mmap file to gain performance against big file
            mm_obj = mmap.mmap(fin.fileno(), 0, mmap.ACCESS_READ)

            total, sum_all = count_and_sum(mm_obj)
            sys.stdout.write(PROMPTMSG % (total, sum_all))
    except ValueError, err:
        msg = "ValueError: %s\nValue can't be convert to float\n" % str(err)
        sys.stderr.write(msg)
    except mmap.error, err:
        msg = "mmmap.error: %s\nplease check the input file\n" % str(err)
        sys.stderr.write(msg)
    except BaseException, err:
        msg = "Unexpected error: %s\n" % str(err)
        sys.stderr.write(msg)

if __name__ == "__main__":
    main()

