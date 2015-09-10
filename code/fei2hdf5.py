#!/usr/bin/python
import scipy as sp
import numpy as np
import h5py
import time
import sys
import re


#--------------------------------------------------------------
# Input 
#--------------------------------------------------------------
model_file=sys.argv[1:]

model_file_number=len(model_file)
model_all='0'
for i in range(model_file_number):
	model_text= open(model_file[i],'r')
	model=model_text.read()
	model_all=model+'\r\n'+model_all
	model_text.close()

#remove the comments lines
model_all=re.sub("\/\/.*", "", model_all)
model_all=re.sub("include.*", "", model_all)

model_line=model_all.splitlines()
model_line_number=len(model_line)

element_number = model_all.count('add element')
node_number = model_all.count('add node')





#--------------------------------------------------------------
# Pattern definition 
#--------------------------------------------------------------
pattern_name=re.compile('model name "(\w)*" *;.*')
pattern_node=re.compile('add node (#|No) .*[0-9]+ at.*')
pattern_8nodebrick=re.compile('add element (#|No) .*[0-9]+ type 8NodeBrick(\w)* with nodes.*')
pattern_27nodebrick=re.compile('add element (#|No) .*[0-9]+ type 27NodeBrick(\w)* with nodes.*')
pattern_4nodeandes=re.compile('add element (#|No) .*[0-9]+ type 4NodeShell_ANDES(\w)* with nodes.*')
 



#--------------------------------------------------------------
# Extract model_name 
#--------------------------------------------------------------
def extract_model_name():
	for line_num in range(model_line_number):
		matched_line=pattern_name.match(model_line[line_num])
		if matched_line:
			model_name_line=matched_line.group().split()
			model_name=filter(str.isalpha,model_name_line[2])
	return model_name




#--------------------------------------------------------------
# Extract node_coordinate and Number_of_DOFs 
#--------------------------------------------------------------
dimension=3
def extract_node_coordinate():
	node_coordinate=np.zeros((node_number,dimension))
	Number_of_DOFs=np.zeros(node_number,dtype=np.int)
	node_line=0
	for line_num in range(model_line_number):
		matched_line=pattern_node.match(model_line[line_num])
		if matched_line:
			node_coordinate_line=re.split('at|,|with',matched_line.group())
			for n_coor in range(dimension):
				node_coordinate[node_line][n_coor] = filter(lambda decimal: decimal in '-0123456789.' , node_coordinate_line[n_coor+1])
			Number_of_DOFs[node_line] = filter(str.isdigit, node_coordinate_line[4])
			node_line=node_line+1
	return (node_coordinate,Number_of_DOFs)




#--------------------------------------------------------------
# Extract 8NodeBrick  node_number_per_element and element_node 
#--------------------------------------------------------------
def extract8NodeBrick():
	node_number_per_element=np.zeros(element_number,dtype=np.int)
	# element_node=np.zeros((element_number, node_number_per_element),dtype=np.int)
	element_node=[]
	element_line=0;
	for line_num in range(model_line_number):
		matched_line=pattern_8nodebrick.match(model_line[line_num])
		if matched_line:
			element_node_line=re.split('nodes|,|use',matched_line.group())
			# element_node_line=matched_line.group().split()
			node_number_per_element[element_line] = 8
			for n_node in range(node_number_per_element[element_line]):
				element_node.append(filter(str.isdigit, element_node_line[n_node+1]))
			element_line=element_line+1

	element_node = map(int,element_node)
	return element_node




#--------------------------------------------------------------
# Extract 27NodeBrick  node_number_per_element and element_node 
#--------------------------------------------------------------
def extract27NodeBrick():
	node_number_per_element=np.zeros(element_number,dtype=np.int)
	# element_node=np.zeros((element_number, node_number_per_element),dtype=np.int)
	element_node=[]
	element_line=0;
	for line_num in range(model_line_number):
		matched_line=pattern_27nodebrick.match(model_line[line_num])
		if matched_line:
			element_node_line=re.split('nodes|,|use',matched_line.group())
			node_number_per_element[element_line] = 27
			# node_number_per_element[element_line] = filter(str.isdigit, element_node_line[4])
			for n_node in range(node_number_per_element[element_line]):
				element_node.append(filter(str.isdigit, element_node_line[n_node+1]))
			element_line=element_line+1

	element_node = map(int,element_node)
	return element_node



#--------------------------------------------------------------
# Extract 4NodeANDES  node_number_per_element and element_node 
#--------------------------------------------------------------
def extract4NodeANDES():
	node_number_per_element=np.zeros(element_number,dtype=np.int)
	# element_node=np.zeros((element_number, node_number_per_element),dtype=np.int)
	element_node=[]
	element_line=0;
	for line_num in range(model_line_number):
		matched_line=pattern_4nodeandes.match(model_line[line_num])
		if matched_line:
			element_node_line=re.split('nodes|,|use',matched_line.group())
			node_number_per_element[element_line] = 4
			# node_number_per_element[element_line] = filter(str.isdigit, element_node_line[4])
			for n_node in range(node_number_per_element[element_line]):
				element_node.append(filter(str.isdigit, element_node_line[n_node+1]))
			element_line=element_line+1

	element_node = map(int,element_node)
	return element_node




#--------------------------------------------------------------
# Extract main
#--------------------------------------------------------------

model_name=extract_model_name()

(node_coordinate,Number_of_DOFs)=extract_node_coordinate()

andes4=model_all.count('4NodeANDES')
brick8=model_all.count('8NodeBrick')
brick27=model_all.count('27NodeBrick')

if andes4>0:
	element_node=extract4NodeANDES()
	node_number_per_element=np.linspace(4,4,element_number)
	node_number_per_element=map(int,node_number_per_element)

if brick8>0:
	element_node=extract8NodeBrick()
	node_number_per_element=np.linspace(8,8,element_number)
	node_number_per_element=map(int,node_number_per_element)
if brick27>0:
	element_node=extract27NodeBrick()
	node_number_per_element=np.linspace(27,27,element_number)
	node_number_per_element=map(int,node_number_per_element)










#--------------------------------------------------------------
# Calculate  node--> Index_to_Coordinates   
#--------------------------------------------------------------
Index_to_Coordinates = np.zeros(node_number,dtype=np.int)
for n_node in range(1,node_number):
	Index_to_Coordinates[n_node]=Index_to_Coordinates[n_node-1]+dimension






#--------------------------------------------------------------
# Generate hdf5 
#--------------------------------------------------------------
h5out_file_name='feicheck_'+model_name+'.h5.feioutput'
h5file=h5py.File(h5out_file_name,"w")

# element_node_one_column=element_node.reshape(element_number*node_number_per_element,1)
h5file.create_dataset("Model/Elements/Connectivity", data=element_node)

node_coordinate_one_column=node_coordinate.reshape(node_number*dimension,1)
h5file.create_dataset("Model/Nodes/Coordinates", data=node_coordinate_one_column)

node_number_per_element=np.insert(node_number_per_element,0,-1)
h5file.create_dataset("Model/Elements/Number_of_Nodes", data=node_number_per_element)

Number_of_DOFs=np.insert(Number_of_DOFs,0,-1)
h5file.create_dataset("Model/Nodes/Number_of_DOFs", data=Number_of_DOFs)

Index_to_Coordinates=np.insert(Index_to_Coordinates,0,-1)
h5file.create_dataset("Model/Nodes/Index_to_Coordinates", data=Index_to_Coordinates)

Number_of_Time_Steps=1
h5file.create_dataset("Number_of_Time_Steps", data=Number_of_Time_Steps)

h5file.create_dataset("Number_of_Elements", data=element_number)

h5file.create_dataset("Number_of_Nodes", data=node_number)

Time_Steps=1
h5file.create_dataset("time", data=Time_Steps)

localtime = time.asctime( time.localtime(time.time()) )
h5file.create_dataset("Date_and_Time",data=str(localtime))

h5file.close()
#--------------------------------------------------------------
# Generate hdf5 end
#--------------------------------------------------------------








