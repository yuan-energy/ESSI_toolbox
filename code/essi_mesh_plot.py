#!/usr/bin/python
import sys
import os
import re
# ===============================
sys.path.append("/usr/local/visit/2.9.1/linux-x86_64/lib/site-packages/visit")
import visit





file_in=sys.argv[1]
cur_dir=os.getcwd()
file_input=os.path.join(cur_dir,file_in)



visit.Launch()

visit.OpenDatabase(file_input)

visit.AddPlot("Mesh","ESSI Domain Mesh")

visit.DrawPlots()


# # save picture option

h5_filename=os.path.basename(file_input)


out_filename = re.split(r'\.(?!\d)', h5_filename)
out_filename = out_filename[0]
# print out_filename

s = visit.SaveWindowAttributes()
s.fileName=out_filename
s.format = s.JPEG
# s.outputToCurrentDirectory = 0
# s.outputDirectory =  "/Path/To/Output/Directory"
# s.family = 1   # 1 if want Visit to automatically add 000, 001, to the end of file (We need this)
# s.progressive = 1
s.screenCapture=0
s.height = 1024 # Here you can specify the resolution 
s.width  = 1280 
visit.SetSaveWindowAttributes(s)


# # change the view point
v = visit.GetView3D()
v.viewNormal = (-0.571619, 0.405393, 0.713378)
v.viewUp = (0.308049, 0.911853, -0.271346)
# print "The view is: ", v
visit.SetView3D(v)
visit.SaveWindow()

v = visit.GetView3D()
# print "The view is: ", 
v.viewNormal = (0.571619, -0.405393, -0.713378)
v.viewUp = (-0.608049, -0.211853, 0.271346)
visit.SetView3D(v)
visit.SaveWindow()


