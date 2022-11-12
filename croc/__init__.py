from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import str
from builtins import range
from builtins import int
from future import standard_library
standard_library.install_aliases()
from builtins import object
import math
import random
from functools import reduce
from ._version import __version__


def SampleCurves(sample, N=500):
    """A convenience function which samples random curves and returns (1) a vertically averaged curve
    of all samples, (2) the average of all the areas of these samples, and (3) the unbiased standard
    deviation of the samples. For input, the function requires "sample" to be a callable object which
    returns randomly sampled Curve objects.
    """
    assert N >= 1
    assert type(N) == int
    SUM = Curve([(0, 0), (1, 0)])
    AREA = []
    for i in range(N):
        C = sample()
        SUM += C
        AREA.append(C.area())
    curve = SUM.vertical_scale(1.0 / N)
    average = reduce(lambda a, b: a + b, AREA) / N
    std_deviation = reduce(lambda a, b: a + b, ((x - average) ** 2 for x in AREA)) / (
        N - 1
    )
    return curve, average, std_deviation


def BEDROC(scoreddata, alpha):
    """A convenience function which appropriately computes the BEDROC score (and associated curves and
    areas). Output is a dictionary with the relevant data appropriately labeled. For usage examples,
    please see the croc_bedroc script.
    """
    out = {}
    T = Exponential(alpha)
    out["curve"] = CeilingAC(scoreddata.sweep_threshold()).transform(T)
    out["min_curve"] = CeilingAC(scoreddata.sweep_threshold_worst()).transform(T)
    out["max_curve"] = CeilingAC(scoreddata.sweep_threshold_best()).transform(T)

    out["area"] = out["curve"].area()
    out["min_area"] = out["min_curve"].area()
    out["max_area"] = out["max_curve"].area()

    out["BEDROC"] = (out["area"] - out["min_area"]) / (
        out["max_area"] - out["min_area"]
    )
    return out


class ScoredData(object):
    def __init__(self, scored_labels=[]):
        """The base constructor for this class which takes as input a list of 2-tuples representing
        paired scores (as floats where larger scores mean more likely to be positive) and labels
        (1 or 0 with 1 being the positive class).
        """
        self.num = self.num_pos = self.num_neg = 0
        self.score_labels = {}
        self._score_label = {}
        self.nummixed = 0
        for S, L in scored_labels:
            self.add(S, L)

    def __eq__(self, other):
        return self.score_labels.__eq__(other.score_labels)

    @staticmethod
    def read_from_file(file):
        """An alternate constructor which reads data from a file. The file format is white space delimited
        text file with the first column the score and the second column the label.
        """
        SD = ScoredData()
        for line in file:
            S, L = line.split()
            SD.add(float(S), int(L))
        return SD

    @staticmethod
    def read_from_file_ranks1(file):
        """An alternate constructor which reads white space delimited ranks (1-indexed) from a file.
        The first integer should be N, the total number of positive and negative instances. The rest of
        the integers should be the ranks of the positive instances.
        """
        data = [int(R) for R in (" ".join(file.readlines())).split()]
        ranks = data[1:]
        N = data[0]
        return ScoredData.from_ranks1(ranks, N)

    @staticmethod
    def read_from_file_ranks0(file):
        """An alternate constructor which reads white space delimited ranks (0-indexed) from a file.
        The first integer should be N, the total number of positive and negative instances. The rest of
        the integers should be the ranks of the positive instances.
        """
        data = [int(R) for R in (" ".join(file.readlines())).split()]
        ranks = data[1:]
        N = data[0]
        return ScoredData.from_ranks0(ranks, N)

    @staticmethod
    def from_ranks1(positive_ranks, N):
        """An alternate constructor which takes as input the 1-indexed ranks of all the positive instances.
        Scores are fixed at the negative of the 0-indexed rank of each instance. Ties are not
        allowed in this constructor. N is the total number of negative and positive instances.
        """
        return ScoredData.from_ranks0([R - 1 for R in positive_ranks], N)

    @staticmethod
    def from_ranks0(positive_ranks, N):
        """An alternate constructor which takes as input the 0-indexed ranks of all the positive instances.
        Scores are fixed at the negative of the 0-indexed rank of each instance. Ties are not
        allowed in this constructor. N is the total number of negative and positive instances.
        """
        for R in positive_ranks:
            assert R >= 0
            assert R < N
            assert int(R) == R

        ranks = set(positive_ranks)
        assert len(ranks) == len(positive_ranks)  # No ties allowed in this constructor!

        scored_labels = [(-n, 1 if n in positive_ranks else 0) for n in range(N)]

        return ScoredData(scored_labels)

    def add(self, score, label):
        """Preferred method to add score-label pairs to instance"""
        label = 1 if not not label else 0
        self.num_pos += label
        self.num_neg += 1 - label
        self.num += 1

        assert self.num_pos + self.num_neg == self.num

        self.score_labels[score] = self.score_labels.get(score, [])
        score_labels = self.score_labels[score]
        score_labels.append(label)

        if len(score_labels) == 1:
            self._score_label[score] = label
        elif label != self._score_label[score]:
            self._score_label[score] = "mixed"
            self.nummixed += 1

    def mixed_tie_count(self):
        """Returns the number of scores associated with instances with different labels."""
        return self.nummixed

    def sweep_threshold(self, tie_mode="smooth"):
        """An iterater that yields TP, TN, FP, FN with a threshold at infinity and gradually sweeping down to
        negative infinity. Ties can be handeled in several ways:

        * smooth (preferred) - construct a smooth slanted line which interpolates the TP, TN, FP, and FN appropriately
        * ignore - output the instances in the order they were presented to the ScoredData instance.
        * sample - randomly shuffle the ties.
        """
        if self.num_pos == 0 or self.num_neg == 0:
            raise AssertionError(
                "There must be at least one positive and one negative example. This data has %i positive(s) and %i negative(s)."
                % (self.num_pos, self.num_neg)
            )

        # from sympy import Rational
        # from sympy import cache
        from fractions import Fraction as Rational

        def smooth_ties(ties):
            sum = 0
            for t in ties:
                sum += t
            return [Rational(sum, len(ties))] * len(ties)

        def ignore_ties(ties):
            return ties

        def sample_ties(ties):
            return random.sample(ties, len(ties))

        if tie_mode == 1 or tie_mode == "smooth":
            tie_mode = smooth_ties
        elif tie_mode == 0 or tie_mode == "ignore":
            tie_mode = ignore_ties
        elif tie_mode == 2 or tie_mode == "sample":
            tie_mode = sample_ties
        else:
            raise ValueError(
                "tie_mode must equal 'smooth_ties', 'ignore_ties', or 'sample_ties'."
            )

        TP = FP = 0
        TN = self.num_neg
        FN = self.num_pos

        yield TP, TN, FP, FN

        SCORES = list(self.score_labels.items())
        SCORES.sort()
        SCORES.reverse()

        for S, Ls in SCORES:
            if self._score_label[S] == "mixed":
                Ls = tie_mode(Ls)
            for L in Ls:
                # if type(L) == int: L = Rational(L)
                TP += L
                FP += 1 - L
                FN -= L
                TN -= 1 - L
                if int(TP) == TP:
                    TP = int(TP)
                    FP = int(FP)
                    FN = int(FN)
                    TN = int(TN)
                    yield TP, TN, FP, FN
                else:
                    yield float(TP), float(TN), float(
                        FP
                    ), float(FN)

        assert TN == 0
        assert FN == 0
        # cache.clear_cache()

    def sweep_threshold_best(self):
        """Equivalent to the sweep_threshold method, but assumes all the positives are ranked at the top of the list."""
        TP = FP = 0.0
        TN = self.num_neg
        FN = self.num_pos
        yield TP, TN, FP, FN

        for L in [1] * self.num_pos + [0] * self.num_neg:
            TP += L
            FP += 1 - L
            FN -= L
            TN -= 1 - L
            yield TP, TN, FP, FN

        assert TN == 0
        assert FN == 0

    def sweep_threshold_worst(self):
        """Equivalent to the sweep_threshold method, but assumes all the positives are ranked at the bottom of the list."""
        TP = FP = 0.0
        TN = self.num_neg
        FN = self.num_pos
        yield TP, TN, FP, FN

        for L in [0] * self.num_neg + [1] * self.num_pos:
            TP += L
            FP += 1 - L
            FN -= L
            TN -= 1 - L
            yield TP, TN, FP, FN

        assert TN == 0
        assert FN == 0

    def sweep_threshold_random(self):
        """Equivalent to the sweep_threshold method, but randomly shuffles the positives throughout the list."""
        TP = FP = 0.0
        TN = self.num_neg
        FN = self.num_pos
        yield TP, TN, FP, FN

        labels = [0] * self.num_neg + [1] * self.num_pos
        random.shuffle(labels)

        for L in labels:
            TP += L
            FP += 1 - L
            FN -= L
            TN -= 1 - L
            yield TP, TN, FP, FN

        assert TN == 0
        assert FN == 0


def ROC(sweep):
    """Create a ROC curve.

    >>> SD = ScoredData.from_ranks1([2,4],4)
    >>> ROC(SD.sweep_threshold())
    Curve([(0.0, 0.0), (0.5, 0.0), (0.5, 0.5), (1.0, 0.5), (1.0, 1.0)])
    """
    C = Curve()
    for TP, TN, FP, FN in sweep:
        TPR = float(TP) / (TP + FN)
        FPR = float(FP) / (FP + TN)
        C.append(FPR, TPR)
    return C


def SlantedAC(sweep):
    """Create a slanted AC curve.

    >>> SD = ScoredData.from_ranks1([2,4],4)
    >>> SlantedAC(SD.sweep_threshold())
    Curve([(0.0, 0.0), (0.25, 0.0), (0.5, 0.5), (0.75, 0.5), (1.0, 1.0)])
    """
    C = Curve()
    for TP, TN, FP, FN in sweep:
        TPR = float(TP) / (TP + FN)
        F = float(FP + TP) / (FP + TN + TP + FN)
        C.append(F, TPR)
    return C


def CeilingAC(sweep):
    """Create a stepped AC curve."""
    C = Curve()
    lastTPR = lastF = 0
    for TP, TN, FP, FN in sweep:
        TPR = float(TP) / (TP + FN)
        F = float(FP + TP) / (FP + TN + TP + FN)
        C.append(lastF, TPR)
        C.append(F, TPR)
        lastTPR = TPR
        lastF = F
    return C


def FloorAC(sweep):
    """Create a stepped AC curve."""
    C = Curve()
    lastTPR = lastF = 0
    for TP, TN, FP, FN in sweep:
        TPR = float(TP) / (TP + FN)
        F = float(FP + TP) / (FP + TN + TP + FN)
        if F < 0:
            continue
        C.append(F, lastTPR)
        C.append(F, TPR)
        lastTPR = TPR
        lastF = F
    return C


class Curve(object):
    """A class that encodes, left to right, a monotonically increasing parametric curve."""

    @staticmethod
    def average(curves):
        """
        A static function which vertically averages a list of curves. For example:

        >>> C1 = Curve([(0,0), (1,1)])
        >>> C2 = Curve([(0,0), (0,1), (1,1)])
        >>> Curve.average([C1,C2])
        Curve([(0.0, 0.0), (0.0, 0.5), (1.0, 1.0)])
        """
        return Curve.sum(curves).vertical_scale(1 / float(len(curves)))

    @staticmethod
    def sum(curves):
        """
        A static function which vertically sumss a list of curves. For example:

        >>> C1 = Curve([(0,0), (1,1)])
        >>> C2 = Curve([(0,0), (0,1), (1,1)])
        >>> Curve.sum([C1,C2])
        Curve([(0.0, 0.0), (0.0, 1.0), (1.0, 2.0)])
        """
        return reduce(lambda A, B: A + B, curves)

    def __eq__(self, other):
        """
        Curves are equal if their coordinates are the same.

        >>> Curve([(0,0), (1, 1)]) == Curve([(0,0), (1, 1)])
        1
        >>> Curve([(0,0), (1, 1)]) != Curve([(0,0)])
        1

        Curves are also equal to lists composed of the same coordinates
        >>> [(0,0), (1, 1)] == Curve([(0,0), (1, 1)])
        1
        >>> Curve([(0,0), (1, 1)]) == [(0,0), (1, 1)]
        1
        """
        return list(self).__eq__(list(other))

    def write_to_file(self, file):
        for x, y in self:
            print(x, y, file=file)

    @staticmethod
    def read_from_file(file):
        """
        Read a curve from in a input file.

        >>> from io import StringIO
        >>> file = StringIO('0 0 \\n 0 1 \\n 1 1')
        >>> Curve.read_from_file(file)
        Curve([(0.0, 0.0), (0.0, 1.0), (1.0, 1.0)])
        """
        C = Curve()
        for L in file:
            x, y = L.split()
            C.append(x, y)
        return C

    def __init__(self, coords=[]):
        """
        Construct a new curve from an iterable argument using this curve's append method.

        Curves can be constructed in two ways. First, we can initialize a curve and then iteratively
        add each coordinate.

        >>> C = Curve()
        >>> C.append(0, 0)
        >>> C.append(1, 1)
        >>> C
        Curve([(0.0, 0.0), (1.0, 1.0)])

        Or we can pass a list of coordinates to the constructor to accomplish the same effect.

        >>> C = Curve([(0, 0), (1, 1)])
        >>> C
        Curve([(0.0, 0.0), (1.0, 1.0)])

        Notice, all the integers were automatically converted to floats.  We can also create a copy of a curve by passing it as the argument to the initializer:

        >>> D = Curve(C)
        >>> D
        Curve([(0.0, 0.0), (1.0, 1.0)])
        >>> C is D
        0
        """
        self._coord = []
        for x, y in coords:
            self.append(x, y)

    def append(self, x, y):
        """Append an x,y coordinate pair to this curve performing basic error checking to ensure
        resulting curve is monotonically increasing and that vertically and horizontolly colinear points
        are removed, and duplicate points are removed.

        >>> C = Curve()
        >>> C.append(0, 0) #initialize first coordinate to the origin

        Adding a coordinate that decreases either the x or y component will throw an exception.

        >>> C.append(-1,0)
        Traceback (most recent call last):
            ...
        AssertionError
        >>> C.append(0,-1)
        Traceback (most recent call last):
            ...
        AssertionError

        Adding a duplicate coordinate will do nothing.

        >>> C
        Curve([(0.0, 0.0)])
        >>> C.append(0,0)
        >>> C
        Curve([(0.0, 0.0)])

        Adding a monotonically increasing coordinate will work fine.

        >>> C.append(0,1)
        >>> C
        Curve([(0.0, 0.0), (0.0, 1.0)])

        Internal vertically or horizontally colinear are removed.

        >>> C.append(0,2)
        >>> C != [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
        1
        >>> C
        Curve([(0.0, 0.0), (0.0, 2.0)])

        On slanted lines, colinear points are not removed.

        >>> C = Curve()
        >>> C.append(0, 0)
        >>> C.append(1, 1)
        >>> C.append(2, 2)
        >>> C
        Curve([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)])

        """
        x = float(x)
        y = float(y)
        if len(self) >= 1:
            assert x >= self[-1][0] - 0.000001  # assert that x monotonically increases.
            assert y >= self[-1][1] - 0.000001  # assert that y monotonically increases.
            if (x, y) == self[-1]:
                return  # no need to append duplicate point

        if len(self) >= 2:
            if (self[-2][0] == self[-1][0]) and (self[-1][0] == x):
                del self[-1]  # eliminate horizontal colinear point
            elif (self[-2][1] == self[-1][1]) and (self[-1][1] == y):
                del self[-1]  # eliminate vertical colinear point
        self._coord.append((x, y))

    def __delitem__(self, i):
        """Delete a the i-th coordinate

        >>> C = Curve([(0,0), (1,1)])
        >>> del C[1]
        >>> C
        Curve([(0.0, 0.0)])

        """
        del self._coord[i]

    def __getitem__(self, i):
        """Return the i-th coordinate

        >>> C = Curve([(0,0), (1,1)])
        >>> C[0]
        (0.0, 0.0)
        """
        return self._coord[i]

    def __iter__(self):
        """Coordinates of a curve can be iterated over:

        >>> C = Curve([(0,0), (1,1)])
        >>> for x, y in C:
        ...     print(x, y)
        0.0 0.0
        1.0 1.0
        """
        return iter(self._coord)

    def __str__(self):
        return str(self._coord)

    def __len__(self):
        """The number of coordinates of a curve is accessed using the len function.

        >>> C = Curve([(0,0), (1,1)])
        >>> len(C)
        2
        """
        return len(self._coord)

    def __repr__(self):
        return "Curve(" + repr(self._coord) + ")"

    def area(self):
        """Integrate along the coordinates of a curve using the trapezoid rule.

        Here are some examples:

        >>> Curve( [(0,0), (1,1) ] ).area()
        0.5
        >>> Curve( [(0,0), (1,0), (1,1)] ).area()
        0.0
        >>> Curve( [(0,0), (0,1), (1,1)] ).area()
        1.0
        """
        area = 0.0
        last_x, last_y = self._coord[0]
        for x, y in self._coord:
            area += (y + last_y) * (x - last_x) / 2.0
            last_x = x
            last_y = y
        return area

    def __add__(self, other):
        """
        Vertically add two curves together. Requires that the two curves start at the same x-position and end at the same x-position.

        Be sure the begin and end x positions are the same or an exception will be thrown:

        >>> Curve([(0,0), (1,1)]) + Curve([(0.3,0), (1,1)])
        Traceback (most recent call last):
            ...
        AssertionError
        >>> Curve([(0,0), (1,1)]) + Curve([(0,0), (1.3,1)])
        Traceback (most recent call last):
            ...
        AssertionError

        Here are some examples of how this code will add curves, you may want to plot them out.

        >>> C1 = Curve([(0,0),(1,1)])
        >>> C2 = Curve([(0,0), (0,0.5), (1,0.5), (1,1)])
        >>> C3 = Curve([(0,0), (0.5,0), (0.5,1), (1,1)])

        >>> C1 + C2
        Curve([(0.0, 0.0), (0.0, 0.5), (1.0, 1.5), (1.0, 2.0)])
        >>> C1 + C3
        Curve([(0.0, 0.0), (0.5, 0.5), (0.5, 1.5), (1.0, 2.0)])
        >>> C2 + C3
        Curve([(0.0, 0.0), (0.0, 0.5), (0.5, 0.5), (0.5, 1.5), (1.0, 1.5), (1.0, 2.0)])

        And remember that adding a curve to itself is like vertically scaling it by 2.

        >>> (C1 + C1) == C1.vertical_scale(2)
        1
        >>> (C2 + C2) == C2.vertical_scale(2)
        1
        >>> (C3 + C3) == C3.vertical_scale(2)
        1

        Of course, addition is commutative:

        >>> (C2 + C1) == (C1 + C2)
        1
        >>> (C1 + C3) == (C3 + C1)
        1
        >>> (C2 + C3) == (C3 + C2)
        1

        And adding two curves with area = 0.5 will result in a curve with area = 1.0.

        >>> (C2 + C1).area()
        1.0
        >>> (C1 + C3).area()
        1.0
        >>> (C2 + C3).area()
        1.0
        """
        assert self[0][0] == other[0][0]
        assert self[-1][0] == other[-1][0]

        c1 = list(self)
        c2 = list(other)
        C = Curve()

        last_p1 = c1.pop(0)
        last_p2 = c2.pop(0)
        C.append(last_p1[0], last_p1[1] + last_p2[1])

        while c1 or c2:
            if not c1:
                for p in c2:  # add rest of c2
                    C.append(p[0], p[1] + last_p1[1])
                    last_p2 = p
                break
            if not c2:
                for p in c1:  # add rest of c1
                    C.append(p[0], p[1] + last_p2[1])
                    last_p1 = p
                break

            x = min(c1[0][0], c2[0][0])

            if c1[0][0] == x:
                p1 = c1.pop(0)
            else:
                p1 = (
                    x,
                    ((c1[0][0] - x) * last_p1[1] + (x - last_p1[0]) * c1[0][1])
                    / (c1[0][0] - last_p1[0]),
                )

            if c2[0][0] == x:
                p2 = c2.pop(0)
            else:
                p2 = (
                    x,
                    ((c2[0][0] - x) * last_p2[1] + (x - last_p2[0]) * c2[0][1])
                    / (c2[0][0] - last_p2[0]),
                )

            C.append(x, p1[1] + p2[1])

            last_p1 = p1
            last_p2 = p2
        return C

    def vertical_scale(self, scale):
        """Return a new Curve object that has y values shrunk or expanded by a given scale factor.

        An example:

        >>> c = Curve( [(0,0), (1,1) ] )
        >>> c.vertical_scale(2)
        Curve([(0.0, 0.0), (1.0, 2.0)])
        """
        return self.transform(lambda x: x * scale, "y")

    def transform(self, transform, axis="x"):
        """Return a new curve with the x or y coordinates transformed"""
        if axis == "x":
            return Curve([(transform(x), y) for x, y in self])
        elif axis == "y":
            return Curve([(x, transform(y)) for x, y in self])
        else:
            raise ValueError("axis must be 'x' or 'y'")


class Transform(object):
    """The interface which all x-axis transforms should implement. The __call__ method
    should expect as map the input in the range [0,1] to the output domain [0,1] with
    f(0) = 0 and f(1) = 1.
    """

    def __init__(self, alpha):
        """This initializer accepts the paremeter alpha in the range (0,Inf] and attatches
        it to the instance. Classes which derive from Transform should either use alpha
        or over ride this method with a method which takes an appropriate number of parameters
        and implements appropriate type checking assertions.
        """
        assert alpha > 0.0
        self.alpha = alpha

    def __call__(self, x):
        raise NotImplementedError


class Logarithm(Transform):
    """
    This class encodes the logarithmic transform computed as: f(x) = log(1 + x * alpha)/log(1 + alpha)
    """

    def __call__(self, x):
        """
        >>> Logarithm(10)(1)
        1.0
        >>> Logarithm(100)(0)
        0.0
        """
        assert x <= 1.0
        assert x >= 0.0
        return math.log(1.0 + x * self.alpha) / math.log(1.0 + self.alpha)


class Exponential(Transform):
    """This class encodes the exponential transform computed as:
    f(x) = (1 - exp(-alpha * x)) / (1 - exp(-alpha))
    """

    def __call__(self, x):
        """
        >>> Exponential(10)(1)
        1.0
        >>> Exponential(100)(0)
        0.0
        """

        assert x <= 1.0
        assert x >= 0.0
        return (1.0 - math.exp(-self.alpha * x)) / (1.0 - math.exp(-self.alpha))


class Power(Transform):
    """This class encodes the exponential transform computed as:
    f(x) = x ^ (1/(1 + alpha))
    """

    def __call__(self, x):
        assert x <= 1.0
        assert x >= 0.0
        return x ** (1.0 / (1.0 + self.alpha))


class Linear(Transform):
    def __init__(self):
        pass

    def __call__(self, x):
        assert x <= 1.0
        assert x >= 0.0
        return x


def main():
    import doctest

    doctest.testmod()


if __name__ == "__main__":
    main()
