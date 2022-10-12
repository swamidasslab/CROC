=========================
Installation Instructions
=========================

Requirements
------------

CROC requires that both `Python 2.x`_ and Sympy_ are installed and in working order.

From Source
------------

After downloading the most recent tarball from the `Python Package Index`_, the following commands will build and install
CROC::

    tar xzvf CROC.tar.gz
    cd CROC
    python setup.py build
    sudo python setup.py install


Easy Install
-------------

On Unix/Linux systems, Macs, and Windows/Cygwin (with cygwin python installed) installing CROC is as simple as running the command::

    easy_install CROC


Easy Install Problems on Cygwin + Windows Python
************************************************

There is bug in how easy_install, Python and cygwin work together when 
the windows version of python is called from cygwin. In this situation, 
none of the commandline utilities will function properly and the egg that 
easy_install creates is not importable from a cygwin python session.


The best work around for this issue is to install from source code to create a non-egg installation which will be
importable. To get the commandline utilities working, it is best to install a cygwin version of python and install 
CROC using this version. This will appropriately generate the scripts files in a way that will work with cygwin. 

Testing the Installation
------------------------

Once installed, all the dostrings can be tested with the command::

    python -m croc

.. _Python 2.x: http://www.python.org/
.. _Sympy: http://code.google.com/p/sympy/
.. _Python Package Index: http://pypi.python.org/pypi/CROC/
