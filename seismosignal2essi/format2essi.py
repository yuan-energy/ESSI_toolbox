#!/usr/bin/python

import sys
import numpy as np 

read_filename = sys.argv[1] 

file_pre = read_filename.split('.dat')[0]

data_filename = str(file_pre) + '.data' 

with open(read_filename, 'r') as fin:
    data = fin.read().splitlines(True)
with open(data_filename, 'w') as fout:
    fout.writelines(data[1:])


t_a_v_d = np.loadtxt(data_filename)


t = t_a_v_d[:, 0] 
a = t_a_v_d[:, 1] 
v = t_a_v_d[:, 2] 
d = t_a_v_d[:, 3] 


acc_file = file_pre + '_acc.txt'
vel_file = file_pre + '_vel.txt'
dis_file = file_pre + '_dis.txt'

with open(acc_file, 'w') as fout:
	for i in range(len(t)):
		fout.write( str(t[i]) + ' \t ' + str(a[i]) + ' \n' )
with open(vel_file, 'w') as fout:
	for i in range(len(t)):
		fout.write( str(t[i]) + ' \t ' + str(v[i]) + ' \n' )
with open(dis_file, 'w') as fout:
	for i in range(len(t)):
		fout.write( str(t[i]) + ' \t ' + str(d[i]) + ' \n' )


