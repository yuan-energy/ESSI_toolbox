# -*- coding: utf-8 -*-
# Yuan 

import numpy as np 
import h5py as h5

def ans_groups():
	"""This list contains the h5 answer group 
	   which need multiplication with the load factors.
	Input: None
	Output: list of groups of ESSI answers.
	"""
	_groups = []
	_groups.append('/Model/Elements/Gauss_Outputs')
	_groups.append('/Model/Elements/Element_Outputs')
	_groups.append('/Model/Elements/Fibers/Fiber_Outputs')
	_groups.append('/Model/Nodes/Generalized_Displacements')
	_groups.append('/Model/Nodes/Generalized_Accelerations')
	return _groups

def spec_reader(fname):
	"""This function read the file, which contains two columns.
       The first column is the hdf5 filename list.
       The second column is the corresponding load factors.
	Input: 1 specification file name.
	Output: Two lists:
	        * H5 output filenames
	        * the corresponding factors.
	"""
	with open(fname) as f:
	    content = f.readlines()
	content = [x.strip() for x in content] 
	files = []
	factors = []
	for line in content:
		data = line.split()
		files.append(data[0])
		try:
			factors.append(float(data[1]))
		except IndexError:
			print( '--------------------------------------------------------------------------')
			print( 'User Input ERROR found from function spec_reader() in file essi_utlis.py ')
			print( 'The length of files should be equal to the length of factors. ')
			print( '--------------------------------------------------------------------------')
			exit()
	return files, factors