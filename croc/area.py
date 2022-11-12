#!/usr/bin/python
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
import optparse
import sys
from croc import Curve


def main(argv):
    parser = optparse.OptionParser("%prog [options] < in.curve > out.area")
    (options, args) = parser.parse_args(argv)

    C = Curve.read_from_file(sys.stdin)
    print(C.area())


if __name__ == "__main__":
    main(sys.argv[1:])
