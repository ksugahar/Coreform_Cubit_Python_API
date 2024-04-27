import os, sys
import numpy as np
sys.path.append("C:/Program Files/Coreform Cubit 2023.11/bin")

import cubit
cubit.init(["cubit","-nojournal"])

if len(sys.argv) > 1:
	FileName = sys.argv[1]
else:
	FileName = '2024_02_02_york_tetmesh'
with open(FileName + '.jou','r', encoding="utf8") as fid:
	strLines = fid.readlines()
	for n in range(len(strLines)):
		cubit.cmd(strLines[n])

from Cubit_Mesh_Export import *

export_3D_gmsh_ver2(cubit, FileName + '_v2.msh')
#export_3D_gmsh_ver4(cubit, FileName + '_v4.msh')
#export_3D_mesh(cubit, FileName + '.mesh')
#os.system("FreeFEM_mesh.edp")

if 1:
	os.system(f"gmsh {FileName + '_v2.msh'}")
#else:
#	import gmsh
#	gmsh.initialize()
#	gmsh.merge(FileName)
#	gmsh.fltk.run()
#	gmsh.finalize()
