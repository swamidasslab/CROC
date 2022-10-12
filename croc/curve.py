#!/usr/bin/python
import optparse
import sys
from croc import (
    SampleCurves,
    ROC,
    SlantedAC,
    CeilingAC,
    FloorAC,
    Curve,
    ScoredData,
    Linear,
    Exponential,
    Logarithm,
    Power,
)


def main(argv):
    parser = optparse.OptionParser(
        "%prog [options] < input.scoreddata > output.curve 2> info"
    )
    parser.add_option(
        "-m",
        "--tie_mode",
        type="str",
        dest="tie_mode",
        help="tie resolution method {sample,smooth,ignore}.",
        default="smooth",
    )
    parser.add_option(
        "-c",
        "--curve_type",
        type="str",
        dest="curve_type",
        help="curve type {roc,ac,slantedac,ceilingac,floorac}.",
        default="roc",
    )
    parser.add_option(
        "-t",
        "--transform",
        type="str",
        dest="transform",
        help="a python code snipit which evals to a Transform object (DEFAULT = Linear()) typical constructors include Linear, Power, Logarithm, and Exponential.",
        default="Linear()",
    )
    parser.add_option(
        "-b",
        "--best",
        type="str",
        dest="best_file",
        help="file to store the best possible performance curve",
        default=None,
    )
    parser.add_option(
        "-w",
        "--worst",
        type="str",
        dest="worst_file",
        help="file to store the worst possible performance curve",
        default=None,
    )
    parser.add_option(
        "-r",
        "--random",
        type="str",
        dest="random_file",
        help="file to store the random performance curve",
        default=None,
    )
    parser.add_option(
        "-s",
        "--samples",
        type=int,
        dest="samples",
        help="the number of times to sample ties (with 'sample' tie-mode) and the random curve (Default=500)",
        default=500,
    )
    parser.add_option(
        "--r0",
        action="store_true",
        dest="r0",
        help="Input is a rank file, indexed from 0 (Default is Scored-Label format).",
    )
    parser.add_option(
        "--r1",
        action="store_true",
        dest="r1",
        help="Input is a rank file, indexed from 1 (Default is Scored-Label format).",
    )

    (options, args) = parser.parse_args(argv)

    assert options.tie_mode in ["sample", "smooth", "ignore"]
    assert options.curve_type in ["roc", "slantedac", "ceilingac", "floorac", "ac"]
    assert options.transform != None
    assert not (options.r0 and options.r1)

    options.transform = eval(options.transform)

    rS = ScoredData.read_from_file
    if options.r0:
        rS = ScoredData.read_from_file_ranks0
    if options.r1:
        rS = ScoredData.read_from_file_ranks1

    S = rS(sys.stdin)

    if options.curve_type == "roc":
        M = ROC
    elif options.curve_type == "ac":
        M = SlantedAC
    elif options.curve_type == "slantedac":
        M = SlantedAC
    elif options.curve_type == "celingac":
        M = CeilingAC
    elif options.curve_type == "floorac":
        M = FloorAC

    F = lambda sweep: M(sweep).transform(options.transform)

    if options.tie_mode == "sample":
        curve, average, std_deviation = SampleCurves(
            lambda: F(S.sweep_threshold(tie_mode="sample")), options.samples
        )
        std_error = std_deviation / (options.samples**0.5)

        curve.write_to_file(sys.stdout)
        print("Area Under Curve (average) = ", average, file=sys.stderr)
        print(
            "Area Under Curve (standard deviation) = ", std_deviation, file=sys.stderr
        )
        print("Area Under Curve (standard error) = ", std_error, file=sys.stderr)
    else:
        C = F(S.sweep_threshold(tie_mode=options.tie_mode))
        C.write_to_file(sys.stdout)
        print("Area Under Curve = ", C.area(), file=sys.stderr)

    if options.best_file:
        file = open(options.best_file, "w")
        C = F(S.sweep_threshold_best())
        C.write_to_file(file)
        print("Area Under Best Curve = ", C.area(), file=sys.stderr)

    if options.worst_file:
        file = open(options.worst_file, "w")
        C = F(S.sweep_threshold_worst())
        C.write_to_file(file)
        print("Area Under Worst Curve = ", C.area(), file=sys.stderr)

    if options.random_file:
        curve, average, std_deviation = SampleCurves(
            lambda: F(S.sweep_threshold_random()), options.samples
        )
        std_error = std_deviation / (options.samples**0.5)

        file = open(options.random_file, "w")
        curve.write_to_file(file)
        print("Area Under Random Curve (average) = ", average, file=sys.stderr)
        print(
            "Area Under Random Curve (standard deviation) = ",
            std_deviation,
            file=sys.stderr,
        )
        print("Area Under Random Curve (standard error) = ", std_error, file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
