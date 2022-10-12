======================
File Formats
======================


There are several file formats which are used by the commandline utilities to read and store data and curves. To illustrate these formats,
we will consider a toy dataset consisting of 10 examples, 5 of which are positive (1) and 5 of which are negative(0). Their scores are given below. 

    =====  =====
    Score  Label
    =====  =====
    0.1      0
    0.2      0 
    0.3      1
    0.4      0
    0.5      0
    0.6      1
    0.7      1
    0.8      1
    0.9      0
    1.0      1
    =====  =====

Scored-Label Files
------------------

The most straightforward, and preferred, way of storing and communicating data is the scored-label format. In this format, each line
lists two numbers, first a floating point score and second an integer 1 (for positive) or 0 (for negative). Our toy example could be a text file
with the contents::

    0.1      0
    0.2      0
    0.3      1
    0.4      0
    0.5      0
    1.0      1
    0.6      1
    0.7      1
    0.8      1
    0.9      0


Notice that the data does not need to be in sorted order; the CROC package always assumes that higher scores are better than lower scores. 
If this classifier does not follow this convention (lower scores are better) you will have to manually modify the scores so that 
the rankings used to compute the curves is correct. The simplest way of doing this is by negating all the output. For example, our toy example
would become::

    -0.1      0
    -0.2      0
    -0.3      1
    -0.4      0
    -0.5      0
    -1.0      1
    -0.6      1
    -0.7      1
    -0.8      1
    -0.9      0

By convention, scored-label files should always have ".scored-label" as the file extention.

Rank Files
--------------

For classifiers that do not ever produce ties, the data can be more compactly stored using rank files. Each line of the file should be
an integer. The first integer is the total number of instances (both positive and negative) in the dataset. The following lines
should list one by one the ranks of the positive instances. There are two conventions for counting ranks described below.

Rank0 Files
^^^^^^^^^^^

In this format, the ranks are zero-indexed. In other words, the best ranked instance is ranked 0, the next best is ranked 1, etc. 
For example, our toy data could be stored in a text file as::

    10
    0
    2
    3
    4
    7

By convention, files in this format should always have ".rank0" as the file extention.

Rank1 Files
^^^^^^^^^^^

n this format, the ranks are one-indexed. In other wordsk, the best ranked instance is ranked 1, the next best is ranked 2, etc. 
For example, our toy data could be stored in a text file as::

    10
    1       
    3
    4
    5
    8

By convention, files in this format should always have ".rank1" as the file extention.


Curve Files
-----------

Curve files store the (x,y) cordinates of a performance curve. Each coordinate is stored on a seperate line, the x-coordinate 
is first and should be seperate from the y-coordinate by whitespace. For example, running the :program:`croc-curve` program on 
our toy data with the following command::

    croc-curve < in.scored-data > out.curve

will produce a fille called "out.curve" with the following contents::

    0.0 0.0
    0.0 0.2
    0.2 0.2
    0.2 0.8
    0.6 0.8
    0.6 1.0
    1.0 1.0
 
Notice that the first coordinate should always be (0,0) and the last coordinate will always be (1,1). 
