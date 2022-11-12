================
The CROC Package
================

A package for calculating ROC curves and Concentrated ROC (CROC) curves written by `Dr. S. Joshua Swamidass <http://swami.wustl.edu>`_.

Citation
--------

  | **A CROC Stronger than ROC: Measuring, Visualizing, and Optimizing Early Retrieval**
  | S. Joshua Swamidass, Chloe-Agathe Azencott, Kenny Daily and Pierre Baldi
  | *Bioinformatics*, April 2010, `doi:10.1093/bioinformatics/btq140 <http://bioinformatics.oxfordjournals.org/cgi/content/abstract/btq140>`_

Description
-----------

This pure-python package is designed to be a standardized implementation of performance curves
and metrics for use either in python scripts or through a simple commandline interface. As a standardized implementation
its output is robust enough to be using in publishable scientific work.

With this package, one can easily:

#. Compute the coordinates of both Accumulation Curves and ROC curves.
#. Handle ties appropriately using several methods.
#. Compute the BEDROC metric.
#. Vertically add and average the performance curves of several cross-validation folds.
#. Focus on the early part of the ROC curve by using several x-axis transforms.

The docstrings in this module are fairly complete and the scripts provide simple access to
the most common functions. 
