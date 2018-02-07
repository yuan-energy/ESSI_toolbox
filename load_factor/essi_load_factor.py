#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This Script is used to combine hdf5 output from Real-ESSI.
Author: Yuan Feng
Date:   Tue Feb 6 15:03:57 PST 2018
Input:
	Input: 
	>>> One specification filename, which contains two columns:
    	* List of h5output files
    	* List of factors
    >>> One output filename.
Output:
	* One combined h5output == files[i]*factors[i]
"""

import numpy as np 
import h5py as h5 
import os
import sys 
# sys.path.append('./src')
# Self-defined file:
import src.h5op as h5op
import src.essi_utils as essi_utils

# Specifications
argc = len(sys.argv)
if argc < 3 :
	print("----------------------------------------------------------------")
	print("User Input ERROR from essi_load_factor.py")
	print("Wrong Number of argc : " + str(argc-1))
	print("essi_load_factor.py requires two inputs:")
	print("\t One specification filename, which contains two columns:")
	print("\t\t * List of h5output filenames")
	print("\t\t * List of load factors")
	print("\t One output filename.")
	print("----------------------------------------------------------------")
	exit()


fname = sys.argv[1]
file_o = sys.argv[2]

# Read Specifications
[files, factors] = essi_utils.spec_reader(fname)


h5op.combine_file(files, factors, essi_utils.ans_groups(), file_o) 



