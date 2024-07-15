import os, sys
from numpy import *
from scipy.io import savemat

sys.path.append("C:/Program Files/Coreform Cubit 2024.3/bin")
import cubit
cubit.init(["cubit","-nographics","-nojournal","-noecho","-information","off","-warning","off"])

x = 15
cubit.cmd(f'brick x 1 y 1 z 0.2')
cubit.cmd(f'brick x 0.6 y 0.6 z 0.2')
cubit.cmd(f'brick x 0.2 y 0.1 z 0.2')
cubit.cmd(f'move Volume 3 x 0.4 y 0.05 include_merged ')
cubit.cmd(f'brick x 3 y 3 z 2.6')
cubit.cmd(f'')
cubit.cmd(f'')
cubit.cmd(f'subtract volume 2 from volume 1  keep_tool')
cubit.cmd(f'subtract volume 3 from volume 1  keep_tool')
cubit.cmd(f'subtract volume 1 2  3 from volume 4  keep_tool ')
cubit.cmd(f'webcut volume 5 with plane zplane offset 0.4 ')
cubit.cmd(f'')
cubit.cmd(f'imprint all')
cubit.cmd(f'merge all')
cubit.cmd(f'compress')
cubit.cmd(f'')
cubit.cmd(f'block 1 add volume 2 4 5')
cubit.cmd(f'block 1 name "V_air"')
cubit.cmd(f'block 2 add volume 1')
cubit.cmd(f'block 2 name "V_coil"')
cubit.cmd(f'block 3 add volume 3')
cubit.cmd(f'block 3 name "V_coi2"')
cubit.cmd(f'')
cubit.cmd(f'volume 4 scheme map')
cubit.cmd(f'volume 4 size 0.3')
cubit.cmd(f'mesh volume 4')
cubit.cmd(f'')
cubit.cmd(f'volume 1 to 3 5 scheme tetmesh')
cubit.cmd(f'volume 1 to 3 size auto factor 7')
cubit.cmd(f'mesh volume 1 to 3')
cubit.cmd(f'volume 5 size 0.3')
cubit.cmd(f'mesh volume 5')
cubit.cmd(f'nodeset 1 add surface all')
cubit.cmd(f'nodeset 1 name "out"')

cubit.cmd(f'save cub5 "O:/cubit.cub5" overwrite journal')

FileName = 'O:/test.nas'
import cubit_mesh_export
cubit_mesh_export.export_3D_Nastran(cubit, FileName)
