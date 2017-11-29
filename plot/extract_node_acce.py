import numpy as np 
import h5py as h5 
import sys
import os
import matplotlib.pyplot as plt 


# *************************************************************************************
# Plot Freq Parameters
# *************************************************************************************
plotFreq_min = 0.1
plotFreq_max = 20
# # #############################
import matplotlib.pylab as pylab
params = {
'legend.fontsize': 'xx-large',
          'figure.figsize': (20, 10),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'
}
pylab.rcParams.update(params)
# #############################
# *************************************************************************************
# FFT function
# *************************************************************************************
import scipy.fftpack
import math
def FFT(x,dt):
	N = x.size;
	T = N*dt;
	Fs = 1./dt;
	xfft  = scipy.fftpack.fft(x);
	xfreq = np.linspace(0.0, Fs/2, N/2);
	xfftHalf = 2.0/N * np.abs(xfft[:N//2]);
	xfftHalf[0] = xfftHalf[0]/2;
	return xfreq, xfftHalf

# *************************************************************************************
# PreProcess user's arguments
# *************************************************************************************
argc = len(sys.argv) 
if argc < 4 or argc > 5 :
	print (" Please specify the correct arguments ")
	print ("  * Argument 1 is HDF5 filename  ")
	print ("  * Argument 2 is the node-tag you want to extract ")
	print ("  * Argument 3 is the direction of the node, should be <x|y|z|rx|ry|rz> or other extra dofs .")
	print ("  * Argument 4 is optional, which can custom the filename of extracted txt file.")
	sys.exit()

filename = sys.argv[1]
nodetag = (int)(sys.argv[2])

if(nodetag < 0):
	print ("\n ERROR!!!:: ESSI Node tag " + str(tag) +" does not exist! \n")
	sys.exit()

the_dof = 0 
dof_set = set(['x', 'y', 'z', 'rx', 'ry', 'rz'])
if not sys.argv[3] in dof_set:
	print ("  * Argument 3 is the direction of the node, should be <x|y|z|rx|ry|rz> or other extra dofs .")
	sys.exit()

if sys.argv[3] == 'x':
	the_dof = 0  
elif sys.argv[3] == 'y':
	the_dof = 1 
elif sys.argv[3] == 'z':
	the_dof = 2 
elif sys.argv[3] == 'rx':
	the_dof = 3 
elif sys.argv[3] == 'ry':
	the_dof = 4 
elif sys.argv[3] == 'rz':
	the_dof = 5 

prefix = filename.split('.h5.feioutput')[0]
out_filename = prefix + "_node_" + str(nodetag) + "_" + sys.argv[3] + "_acce"

if argc == 5 :
	out_filename = sys.argv[4]
	
# *************************************************************************************


# *************************************************************************************
# Read the HDF5 File 
# *************************************************************************************
h5fileID0 = h5.File(filename, "r")
N_proc = h5fileID0['/Number_of_Processes_Used'][()]
h5DataFilename = []
if N_proc == 1:
	h5DataFilename = filename
else:
	PartitionInfo = h5fileID0['Model/Nodes/Partition'][()]
	PartitionId = PartitionInfo[(int)(nodetag)]
	if (PartitionId > 0) :
		if (PartitionId > 9) :
			h5DataFilename = filename.split('.feioutput')[0]+'.'+str(PartitionId)+'.feioutput'
		else:
			h5DataFilename = filename.split('.feioutput')[0]+'.0'+str(PartitionId)+'.feioutput'
	else:
		"\n ERROR!!! :: ESSI Node tag " + str(nodetag) +" does not exist! \n"
h5fileID0.close()
h5fileID = h5.File(h5DataFilename, 'r')
IndexToOutput = h5fileID['Model/Nodes/Index_to_Generalized_Displacements'][()];
acc = h5fileID['/Model/Nodes/Generalized_Accelerations'][()]
time = h5fileID['/time'][()]

target_acc_loc = IndexToOutput[nodetag]  + the_dof
target_acc = acc[target_acc_loc]







# *************************************************************************************
# Plot the data in time domain.
# *************************************************************************************
f, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(time, target_acc, '-k', linewidth=3)
ax1.set( xlabel = "Time [s]", ylabel = "Acceleration [m/s^2]", title = "Time Series of Acceleration")
ax1.grid()

# *************************************************************************************
# Plot the data in frequency domain.
# *************************************************************************************
freq, ampl = FFT( target_acc, time[1]-time[0] )
ax2.semilogx(freq, ampl, '-k', linewidth=3)
ax2.set( xlabel = "Frequency [Hz] ", ylabel = "Acceleration [m/s^2] ", xlim = [plotFreq_min, plotFreq_max] , title = "FFT of Acceleration")
ax2.grid()
plt.savefig( out_filename + ".pdf" )
plt.show()






# *************************************************************************************
# Write the data to a txt file
# *************************************************************************************
with open(out_filename + '.txt', 'w') as f : 
	for i in range(len(time)) :
		f.write( str(time[i]) + " \t " + str(target_acc[i]) + "\n")

print(" Data is written to " + out_filename + '.txt')


