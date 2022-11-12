from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
import os
import time
import sys

from distutils.core import setup


# Loads _version.py module without importing the whole package.
def get_version_and_cmdclass(pkg_path):
    import os
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location(
        "version",
        os.path.join(pkg_path, "_version.py"),
    )
    module = module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(module)  # type: ignore
    return module.__version__, module.get_cmdclass(pkg_path)


version, cmdclass = get_version_and_cmdclass("CROC")


setup(name="CROC",
    version=version,
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
    author="S. Joshua Swamidass",
    url="http://swami.wustl.edu/CROC",
    author_email="swamidass@gmail.com",
    install_requires=["future"],
    classifiers=["Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "License :: Free for non-commercial use",
        "Natural Language :: English",
        "Environment :: Console",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
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
