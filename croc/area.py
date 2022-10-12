#!/usr/bin/python
import optparse
import sys
from croc import Curve

def main(argv):
    parser = optparse.OptionParser("%prog [options] < in.curve > out.area" )
    (options, args) = parser.parse_args(argv)

    C = Curve.read_from_file(sys.stdin)
    print C.area()

if __name__=="__main__":
    main(sys.argv[1:])
