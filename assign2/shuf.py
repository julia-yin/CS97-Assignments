#! /usr/local/cs/bin/python3
#
# Copyright 2020 Julia Yin <juliayin@ucla.edu>

import random
import sys
import argparse

class randline:
    def __init__(self, filename):
        if (filename == "blank" or filename == "-"):
            self.lines = sys.stdin,readlines()
            if (len(self.lines) <= 0):
                return 0
        else:
            f = open(filename, 'r')
            self.lines = f.readlines()
            f.close()

    def chooseline(self):
        return random.choice(self.lines)

def main():
    usage_msg = """
Write a random permutation of the input lines to standard output.

With no FILE, or when FILE is -, read standard input.

shuf [option]... [file]
shuf -e [option]... [arg]...
shuf -i lo-hi [option]...

Optional Arguments:
  -i LO-HI   treat each number LO through HI as an input line
  -n COUNT   output at most COUNT lines (default all)
  -r         output lines can be repeated (default false)
  -e         treat each command-line operand as an input line
  --help     display this help and exit
  --version  output version information and exit """

    parser = argparse.ArgumentParser()

    # add options to parser: --echo (-e), --input-range (-i), --head-count (-n)
    #                        --repeat (-r), --help
    parser.add_argument("-e", "--echo",
                       action="store", dest="echo", nargs="+",
                       help="treat each command-line operand as an input line")
    parser.add_argument("-i", "--input-range",
                       action="store", dest="irange",
                       help="treat each number LO through HI as an input line")
    parser.add_argument("-n", "--head-count",
                       action="store", dest="count",
                       help="output COUNT lines (default all)")
    parser.add_argument("-r", "--repeat",
                       action="store_true", dest="repeat", default=False,
                       help="output lines can be repeated (default false)")
    
    options, args = parser.parse_known_args(sys.argv[1:])

    # check for -n -i -r options
    bool_n = bool(options.count)
    bool_i = bool(options.irange)
    bool_r = bool(options.repeat)
    bool_e = bool(options.echo)

    numlines = None
    lines = []

    # -n option: output at most count lines, default all
    # read in numlines and check if valid
    if bool_n:
        try:
            numlines = int(options.count)
        except:
            parser.error("invalid NUMLINES: {0}".
                         format(options.count))

        # negative -n case
        if numlines < 0:
            parser.error("negative count: {0}".
                         format(options.count))

    # -i option: range of lines lo-hi to output
    if bool_i:
        try:
            # read in lo and hi values from input string
            output_range = str(options.irange)
            split_str = output_range.split("-")
            lo = int(split_str[0])
            hi = int(split_str[1])
            lines = list(range(lo, hi + 1))
        
        except:
            # check for errors in lo and hi
            parser.error("invalid input: {0}".
                         format(options.irange))
       
        # check that lo and hi are non-negative 
        if lo < 0 or hi < 0:
            parser.error("negative range: {0}".
                         format(output_range))


    # -e option: treat each command-line operand as an input line
    if bool_e:
        try: 
            #read in text from command line
            lines = options.echo
        except:
            parser.error("invalid input: {0}".
                         format(options.echo))

    # generates lines based on stdin or file input (not -i or -e)
    if not bool_i and not bool_e:
        if len(args) == 0 or args[0] == "-":
            lines = sys.stdin.readlines()
        else:
            input_file = args[0]
            generator = randline(input_file)
            lines = generator.lines

    # start printing randomized lines
    try:
        random.shuffle(lines)
        
        # default: no repeat
        if not bool_r:
            if bool_n:
                numlines = min(len(lines), int(options.count))
            else:
                numlines = len(lines)
            
            # -i requires spaces between lines
            if bool_i or bool_e:
                for x in range(0, numlines):
                    sys.stdout.write(str(lines[x])+'\n')
            else:
                for x in range(0, numlines):
                    sys.stdout.write(str(lines[x]))

        # repeat: bool_r is True 
        else:
            if not bool_n:
                numlines = True
            while numlines != 0:
                # -i requires spaces between lines
                if bool_i or bool_e:
                    sys.stdout.write(str(lines[0])+'\n')
                else:
                    sys.stdout.write(str(lines[0]))
                random.shuffle(lines)

                # numlines is a bool only when no -n is specified
                if isinstance(numlines, bool) is False:
                    numlines -= 1

    except IOError as err:
        parser.error("I/O error({0}): {1}".
                     format(errno, strerror))

if __name__ == "__main__":
    main()
