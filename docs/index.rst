================
The CROC Package
================

A package for calculating ROC curves and Concentrated ROC (CROC) curves written by `Dr. S. Joshua Swamidass <http://swami.wustl.edu>`_.

Citation
--------

Please cite this paper when reporting any work which uses this software:

  | **A CROC Stronger than ROC: Measuring, Visualizing, and Optimizing Early Retrieval**
  | S. Joshua Swamidass, Chloe-Agathe Azencott, Kenny Daily and Pierre Baldi
  | *Bioinformatics*, April 2010, `doi:10.1093/bioinformatics/btq140 <http://bioinformatics.oxfordjournals.org/cgi/content/abstract/btq140>`_

Description
-----------

This pure-python package is designed to be a standardized implementation of performance curves
and metrics for use either in python scripts or through a simple commandline interface. As a standardized implementation
its output is robust enough to be using in publishable scientific work.

With this package, one can easily:

#. compute the coordinates of both Accumulation Curves and ROC curves.
#. handle ties appropriately using several methods.
#. compute the BEDROC metric.
#. vertically add and average the performance curves of several cross-validation folds.
#. focus on the early part of the ROC curve by using several x-axis transforms.

Documentation
-------------

The docstrings in this module are fairly complete and the scripts provide simple access to
the most common functions. Further documentation can be found here:

.. toctree::
    :maxdepth: 2

    install
    scripts
    formats
    r
    api


R-Interface
-----------

Daniel Himmelstein has written up a basic R interface to CROC which is avialable on github (`here <https://github.com/dhimmel/crocr>`_).

Roadmap
---------------

- Github repository established
- As of v1.2, this package now compatible with Python 3. 

TODO:

- Improve test cases (beyond just doctests)
- Refactor to use numpy for v2.0
- Improved CLI interface for v2.0

.. _author : http://swami.wustl.edu/
