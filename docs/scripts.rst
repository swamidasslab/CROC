=======
Scripts
=======

These scripts provide a simple interface to the most useful logic of this package. If the scripts were installed appropriately, they may be called
easily by typing their name at the command line. For example, the :program:`croc-average` program can be called like so::

    croc-average [options]

If the scripts did not install properly, it is also possible to call the scripts directly from the package using the python module command::

    python -m croc.average [options]

Help on all available options can be accessed with the '-h' option. Details about the file formats can be found in :doc:`formats`. Currently these 
programs only use the scored-data format and do not have options for rank0 and rank1 format. Future versions will add support
for these filees. 

The examples below use the the toy data from the :doc:`formats` section. 

croc-area
---------
.. program:: croc-area

A script which can compute the area under a performance curve. For our a basic ROC curve
computed on our toy data, the command::

    croc-area < toy.curve

will yield the output:: 

    0.24


croc-average
------------
.. program:: croc-average

A script which can vertically average performance curves. A obvious example demonstrates that
averaging a curve with itself will produce the same curve::

    croc-average toy.curve toy.curve > average.curve
    diff toy.curve average.curve

This program would be most useful in averaging the perfromance curves of several different runs
for the same algorithm. For example, to aggregate the results of several folds of a cross-validated
experiment.

croc-bedroc
-----------
.. program:: croc-average

A script which can compute the BEDROC metric and several relevant performance curves.
For example, our toy data can be run with the following command::

    croc-bedroc < toy.scored-data

Produces the following output::

    Area Under Curve =  0.00367360390433
    Area Under Best Curve =  0.231293025802
    Area Under Worst Curve =  1.04986260659e-05
    BEDROC =  0.0158382274831

There are several options available to output relevant curves.


croc-curve
----------
.. program:: croc-curve

A script which can compute several different types of performance curves and metrics. On our toy data,
it could be run as::

    croc-curve < toy.scored-data >  toy.curve

To generate a standard ROC curve output file::

    0.0 0.0
    0.4 0.0
    0.4 0.2
    0.8 0.2
    0.8 0.8
    1.0 0.8
    1.0 1.0

While sending the area to stderr::
    
    Area Under Curve =  0.24

There are several options available to tune how this program deals with ties, the type of performance
curve that is generated, and the transform that will applied to the x-axis. The details of many of these
possibiliities will be explained in detail in a forthcoming publication. Until then, it would likely be
best to stick with standard ROC and AC curves with no x-transforms, or to use the :program:`croc-bedroc` program
to compute the BEDROC metric and curves.


