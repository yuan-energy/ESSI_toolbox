# -*- coding: utf-8 -*-
# Yuan 

import numpy as np 
import h5py as h5 
import os

def copy_group(h5source, h5dest, h5group):
	h5source.copy(h5group, h5dest)

def copy_file(h5source, h5dest):
	for key in h5source :
		copy_group(h5source, h5dest, key)

def assign_group(h5group, data):
	h5group[...] = data

def assign_data(h5dest, h5group, new_data):
	g = h5dest[h5group]
	assign_group(g, new_data)

def extract_data(h5source, h5group):
	return h5source[h5group][()]

def clear_file_silent(file):
	try:
	    os.remove(file)
	except OSError:
	    pass

def combine_file(source_file_list, mul_factor_list, h5group_list, h5out_file):
	# clean old file
	clear_file_silent(h5out_file)
	# copy file structure(group)
	f_in = h5.File(source_file_list[0], 'r')
	f_out = h5.File(h5out_file, 'w')
	copy_file(f_in , f_out)
	# copy file content
	for h5group in h5group_list :
		if h5group in f_out:
			for id in range(len(source_file_list)) :
				raw_data = extract_data(h5.File(source_file_list[id], 'r'), h5group)
				if 'new_data' in locals():
					new_data = new_data + raw_data * mul_factor_list[id]
				else:
					new_data = raw_data * mul_factor_list[id]
				assign_data(f_out, h5group, new_data)
			del new_data
	f_out.close()

