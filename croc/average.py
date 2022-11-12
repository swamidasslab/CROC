#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import open
from future import standard_library
standard_library.install_aliases()
import optparse
import sys
from croc import Curve


def main(argv):
    parser = optparse.OptionParser("%prog [options] in1.curve in2.curve > ave.curve")

    (options, args) = parser.parse_args(argv)

    if len(args) == 0:
        parser.print_help()
        sys.exit()

    curves = [Curve.read_from_file(open(FILE, "r")) for FILE in args]
    Curve.average(curves).write_to_file(sys.stdout)


if __name__ == "__main__":
    main(sys.argv[1:])
