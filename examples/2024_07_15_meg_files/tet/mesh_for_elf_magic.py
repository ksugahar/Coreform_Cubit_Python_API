#!python
import os, sys

sys.path.append("C:/Program Files/Coreform Cubit 2024.3/bin")

import cubit
cubit.init(['cubit','-nojournal','-batch','nographics','-nogui','-noecho'])
cubit.reset()

cubit.cmd('create Cylinder height 1 radius 3 ')
cubit.cmd('create Cylinder height 1 radius 2')
cubit.cmd('subtract volume 2 from volume 1 imprint ')
cubit.cmd('brick x 2 y 1 z 1')
cubit.cmd('move Volume 3 x 2 include_merged ')
cubit.cmd('subtract volume 3 from volume 1 imprint ')
cubit.cmd('volume 1 scheme tet')
cubit.cmd('mesh volume 1')
cubit.cmd('compress')

cubit.cmd('block 1 add volume 1 ')
cubit.cmd('block 1 name "coil"')

cubit.cmd('nodeset 1 add surface 2 ')
cubit.cmd('nodeset 1 name "in"')

FileName = 'Cubit.png'
cubit.cmd('graphics window create 2')
cubit.cmd('view from  0.0  0.0  15.0')
cubit.cmd('view at    0.0  0.0  0.0')
cubit.cmd('view up    0.0  1.0  0.0')
cubit.cmd(f'hardcopy "{FileName}" png window 2')
cubit.cmd('graphics window delete 2')
os.startfile(FileName)

FileName = 'Cubit.meg'
import cubit_mesh_export
cubit_mesh_export.export_3D_meg(cubit, FileName)

FileName = 'Cubit.gmsh'
import cubit_mesh_export
cubit_mesh_export.export_3D_gmsh_ver2(cubit, FileName)
