import numpy as np 
import matplotlib.pyplot as plt 
import h5py as h5 
import sys
import os
# *************************************************************************************
# Custom of Plot Parameters
# *************************************************************************************
period_lower_limit = 0.1
period_upper_limit = 5.0
damping = 0.05
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
# ****************************************************************************************************
# Response_spectrum function
# ****************************************************************************************************
def response_spectrum(dt, acc_in, damping, period_lower_limit, period_upper_limit):
	# **************************************************************************************
	# Input
	# **************************************************************************************
	#   * dt            := the time step
	#   * acc_in        := the np.array of acceleration in g
	#   * damping       := the absolute value of damping ratio. e.g. 0.05
	#   * period limits := the limit for the analysis and plot.
	# **************************************************************************************
	# Output
	# **************************************************************************************
	#   * period          := the array of natural period. e.g.(0.01, 0.02, 0.03, ... 5.00).
	#   * pseudo_acc_spec := the array of pseudo acceleration spectrum  in g.
	#   * dis_spec        := the array of displacement spectrum in meter.
	# **************************************************************************************
	period_interval = 0.05 #  interval of period 
	M = 9.8   #%%% Mass, unit N. 
	g = 9.8   #%%% gravity constant in m/s^2
	initial_dis = 0.0  #%%% initial displacement in inch
	initial_vel = 0.0   #%%%% initial velocity in inch/s
	initial_acc = 0.0   #%%%% initial acceleration in inch/s^2
	#%%%#%%% Begin the main program #%%%#%%%%
	m = M/g  
	acc_in=-m*acc_in*g      #%%%% generate equivalent dynamic force due to ground motion    
	No_time_step = len(acc_in)  
	dis = np.zeros(No_time_step) 
	vel = np.zeros(No_time_step) 
	acc = np.zeros(No_time_step)  
	period = np.linspace(period_lower_limit, period_upper_limit, (period_upper_limit-period_lower_limit) /period_interval )  
	N = len(period)   
	dis_spec = np.zeros(N)  
	acc_sepc = np.zeros(N)  
	pseudo_acc_spec = np.zeros(N) 
	for j in range(N):   #%%%%% loop over all periods that needs to calculate response spectrum 	
		w=2*np.pi/period[j]  
		c= 2*damping*m*w  
		K = m*w*w  
		K0 = K + 2*c/dt + 4*m/(dt*dt)       #%%% constant stiffness, does not need to put inside for loop  
		for i in range(1, No_time_step):    #%%% second loop over all time steps 
			P0 = acc_in[i] + c*(2*dis[i-1]/dt + vel[i-1]) + m*(4*dis[i-1]/(dt*dt)+4*vel[i-1]/dt+acc[i-1])  
			dis[i] = P0/K0  
			vel[i] = 2/dt*(dis[i]-dis[i-1])-vel[i-1]  
			acc[i] = 4/(dt*dt)*(dis[i]-dis[i-1]-dt*vel[i-1]-dt*dt*acc[i-1]/4)  
		dis_positive = [ abs(item) for item in dis]
		dis_spec[j] = max(dis_positive)
		acc_positive = [ abs(item) for item in acc]
		acc_sepc[j] = max(acc_positive)/g        #%%% true acceleration spectrum value in g 
		pseudo_acc_spec[j] = dis_spec[j]*w*w/g   #%%% pseudo acceleration spectrum value in g, note its difference with true acceleration spectrum. 
	return period, pseudo_acc_spec, dis_spec     # displacement spectrum in m.  
# ****************************************************************************************************





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
out_filename = prefix + "_node_" + str(nodetag) + "_" + sys.argv[3] + "_spectrum"

if argc == 5 :
	out_filename = sys.argv[4]
# *************************************************************************************






# *************************************************************************************
# Read the HDF5 File (accept both sequential and parallel)
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
# Calculate the response spectrum
# *************************************************************************************
dt = time[1] - time[0]
acc_in_g = [item/9.8 for item in target_acc]
[ period, pseudo_acc_spec, dis_spec ] = response_spectrum(dt, np.array(acc_in_g), damping, period_lower_limit, period_upper_limit)




# *************************************************************************************
# Plot the data 
# *************************************************************************************
f, (ax1, ax2) = plt.subplots(1, 2)
freqs = [1./item for item in period]
ax1.semilogx(freqs, pseudo_acc_spec, 'k-', linewidth=3)  
ax1.set(xlabel = 'Frequency [Hz]', ylabel = 'Pseudo-Spectral Acceleration Sa [g]', title = 'Pseudo-Spectral Acceleration')
ax1.grid()

ax2.semilogx(freqs, dis_spec, 'k-', linewidth=3)  
ax2.set(xlabel = 'Frequency [Hz]', ylabel = 'Spectral Displacement [m]', title = 'Spectral Displacement')
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
