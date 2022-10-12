import commands 
import os
import time
import sys

from distutils.core import setup

#Determine & save the revision number for the ETC
warning=""
vfname=os.path.join('.','VERSION')
try:
    # Always try to determine the version using svnversion
    warning=""
    stat,revset=commands.getstatusoutput('hg id -n')
    if stat != 0:
        raise ValueError("cannot extract version information")
    if revset.find("+") >= 0 :
        warning="this copy is modified."

    f=open(vfname,'w')
    f.write(revset)
    f.close()

except ValueError:
    #If we can't generate it, then see if the version file already
    #exists from when the source distribution was being assembled. 
    try :
        f=open(vfname,"r")
        revset=f.readline()
        f.close()
    except IOError:
        warning="Can't determine version."
        sys.exit()

VERSION = "1.1."+revset

print warning
print "assuming that the version is " + VERSION

setup(name="CROC",
    version=VERSION,
    description="A package for calculating ROC curves and Concentrated ROC (CROC) curves.",
    long_description="""================
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
the most common functions. Further documentation can be found at http://swami.wustl.edu/CROC/
""",
    requires=["sympy"],
    author="S. Joshua Swamidass",
    url="http://swami.wustl.edu/CROC",
    author_email="swamidass@gmail.com",
    classifiers=["Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "License :: Free for non-commercial use",
        "Natural Language :: English",
        "Environment :: Console",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Visualization"],
    scripts=['scripts/croc-average', 'scripts/croc-bedroc', 'scripts/croc-area', 'scripts/croc-curve'],
    packages=['croc']
)
