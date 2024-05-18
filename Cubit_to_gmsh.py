import os, sys
import subprocess

if os.name == 'nt':
	sys.path.append("C:/Program Files/Coreform Cubit 2024.3/bin")
elif os.name == 'posix':
	sys.path.append("Coreform-Cubit-2024.3/bin")

import cubit
cubit.init(["cubit","-nographics","-nojournal","-noecho","-information","off","-warning","off"])

if len(sys.argv) > 1:
	FileName = sys.argv[1]
else:
	FileName = 'one_element'
with open(FileName + '.jou','r', encoding="utf8") as fid:
	strLines = fid.readlines()
	for n in range(len(strLines)):
		cubit.cmd(strLines[n])

from Cubit_Mesh_Export import *

export_3D_gmsh_ver4(cubit, FileName + '.msh')
#export_3D_gmsh_ver4(cubit, FileName + '_v4.msh')
#export_3D_mesh(cubit, FileName + '.mesh')

if 1:
	os.system(f'gmsh {FileName + ".msh"}')
#else:
#	import gmsh
#	gmsh.initialize()
#	gmsh.merge(FileName)
#	gmsh.fltk.run()
#	gmsh.finalize()
