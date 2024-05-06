import os, sys
import numpy as np
sys.path.append("C:/Program Files/Coreform Cubit 2023.11/bin")

import cubit
cubit.init(['cubit','-nojournal','-batch','nographics','-nogui','-noecho'])

if len(sys.argv) > 1:
	FileName = sys.argv[1]
else:
	FileName = 'model'
with open(FileName + '.jou','r') as fid:
	strLines = fid.readlines()
	for n in range(len(strLines)):
		cubit.cmd(strLines[n])

from Cubit_Mesh_Export import *
export_3D_gmsh_ver4(cubit, FileName + '_v4.msh')

os.system(f"gmsh {FileName + '_v4.msh'}")

