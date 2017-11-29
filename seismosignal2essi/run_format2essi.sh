#!/bin/bash
# *****************************************************************
# Convert the format of SeismoSignal to Real-ESSI input
#   * Input : .dat file which has 4 columns : 
#             time, acc, vel, dis
#   * Output: Three .txt files, which has separated 
#             acc, vel, dis information in each file
# *****************************************************************

# clean existing Output
rm -rf ans

# Convert Format
./format2essi.py x.dat
./format2essi.py y.dat
./format2essi.py z.dat

# Create the directory to save the data
mkdir ans

# Remove the intermediate files.
rm *.data

# Move the results to the folder ans.
mv *.txt ./ans


