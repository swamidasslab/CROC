#!/usr/bin/python
import optparse
import sys
from croc import SampleCurves, BEDROC, CeilingAC, Curve, ScoredData, Exponential

def main(argv):
    parser = optparse.OptionParser("%prog [options] < input.scoreddata > output.curve 2> info")
    parser.add_option("-a", "--alpha", type='float', dest="alpha", help="The alpha used to parameterize the BEDROC curve (DEFAULT=20.0)", default = 20.0)
    parser.add_option("-b", "--best", type="str", dest='best_file', help="file to store the best possible performance curve", default=None)
    parser.add_option("-w", "--worst", type="str", dest='worst_file', help="file to store the worst possible performance curve", default=None)
    parser.add_option("-r", "--random", type="str", dest='random_file', help="file to store the random performance curve", default=None)
    parser.add_option("-s", type="int", dest="samples", help="the number of times to sample the random curve (Default=500)", default=500)

    (options, args) = parser.parse_args(argv)

    assert( options.alpha > 0 )
    
    S = ScoredData.read_from_file(sys.stdin)
    F = lambda sweep: CeilingAC(sweep).transform(Exponential(options.alpha))

    RESULTS = BEDROC(S, options.alpha)

    area = RESULTS['area']
    curve = RESULTS['curve']
    Barea = RESULTS['max_area']
    Bcurve = RESULTS['max_curve']
    Warea = RESULTS['min_area']
    Wcurve = RESULTS['min_curve']
    bedroc = RESULTS['BEDROC']

    print >>sys.stderr, "Area Under Curve = ", area
    print >>sys.stderr, "Area Under Best Curve = ", Barea
    print >>sys.stderr, "Area Under Worst Curve = ", Warea
    print >>sys.stderr, "BEDROC = ", bedroc

    if options.best_file:
        file = open(options.best_file, 'w')
        Bcurve.write_to_file(file)

    if options.worst_file:
        file = open(options.worst_file, 'w')
        Wcurve.write_to_file(file)

    if options.random_file:
        curve, average, std_deviation = SampleCurves(lambda : F(S.sweep_threshold_random()), options.samples)
        file = open(options.random_file, 'w')
        curve.write_to_file(file)
        std_error = std_deviation / ( options.samples ** 0.5 )

        print >>sys.stderr, "Area Under Random Curve (average) = ", average
        print >>sys.stderr, "Area Under Random Curve (standard deviation) = ", std_deviation
        print >>sys.stderr, "Area Under Random Curve (standard error) = ", std_error

        print >>sys.stderr, "Random BEDROC (average) = ", (average - Warea) / (Barea - Warea)
        print >>sys.stderr, "Random BEDROC (standard deviation) = ", std_deviation / (Barea - Warea)
        print >>sys.stderr, "Random BEDROC (standard error) = ", std_error / (Barea - Warea)

if __name__=="__main__":
    main(sys.argv[1:])
