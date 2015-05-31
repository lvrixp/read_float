'''A tool to read float numbers from input file or pipe, and prompt total count and sum.
'''

import sys
import os
from optparse import OptionParser
import fileinput
import locale

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

    Accept iterator, of which each item is a string, \
    and scan the float in each item to get the total count and sum.
    It may raise exception if there's item can't be recognized as float.

    Args:
        iterable: an iteratable item that carries float numbers

    Returns:
        A pair that contains the count and sum of all the float been scanned

    Raises:
        ValueError: item that can be recognized as float is found
    '''

    # _total to record the total count of float numbers
    _total = [0]

    # handle special case that can't be handled by float()
    # eg. 10,000
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    def _item_generator(iterable, total):
        '''_item_generator(iterable, total):

        Embedded utility of 'count_and_sum',
        it create an generator object on each item found in the iterator.
        Each item in the generator is a string that been stripped.
        After generator been iterated, total count of items will be calculated.
        '''
        for _item in iterable:
            for _sub_item in _item.split():
                # add to the total count of items
                total[0] += 1
                _sub_item = _sub_item.strip()
                try:
                    retval = float(_sub_item)
                except ValueError, err:
                    # if locale still can't handle it
                    # it will raise ValueError again
                    # and upper level will handle it
                    retval = locale.atof(_sub_item)

                yield retval

        # handle the case if there's nothing input
        yield 0

    _all_items = _item_generator(iterable, _total)

    #sum of all the float numbers
    _sum = reduce(lambda a, b: float(a) + float(b), _all_items)

    return _total[0], _sum


def _get_file_path():
    '''Check the input arguments for the file path
    '''
    _parser = OptionParser()
    _parser.add_option("-f", "--filepath", dest='file_path', help="file path to be read")
    _options, _ = _parser.parse_args()

    if _options.file_path == '-':
        return '-'

    if _options.file_path is None or not os.path.isfile(_options.file_path):
        _parser.print_help()
        raise ValueError("Invalid file path: %s" % _options.file_path)

    return _options.file_path

def _main():
    '''Main function of the tool
    '''
    try:
        _file_path = _get_file_path()
        _fin = fileinput.input(_file_path)
        _total, _sum = count_and_sum(_fin)
        sys.stdout.write(PROMPTMSG % (_total, _sum))
    except ValueError, err:
        msg = "ValueError: %s\n" % str(err)
        sys.stderr.write(msg)
    except SystemExit, err:
        msg = "SystemExit: %s\n" % str(err)
    except BaseException, err:
        msg = "Unexpected error: %s\n" % str(err)
        sys.stderr.write(msg)

if __name__ == "__main__":
    _main()

