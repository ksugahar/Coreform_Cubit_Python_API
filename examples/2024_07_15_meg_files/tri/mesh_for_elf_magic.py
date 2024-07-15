#!python
import os, sys

sys.path.append("C:/Program Files/Coreform Cubit 2024.3/bin")
import cubit
cubit.init(['cubit','-nojournal','-batch','nographics','-nogui','-noecho'])
cubit.reset()

cubit.silent_cmd('create surface circle radius 1 zplane ')
#cubit.silent_cmd('surface all scheme circle ')
cubit.silent_cmd('surface all scheme trimesh ')
cubit.silent_cmd('mesh surf all ')
cubit.silent_cmd('block 1 add surface 1 ')
cubit.silent_cmd('block 1 name "S_coil_top_p1" ')

print(cubit.get_surface_element_count(1));

FileName = 'Cubit.png'
cubit.cmd('graphics window create 2')
cubit.cmd('view from  0.0  0.0 -5.0')
cubit.cmd('view at    0.0  0.0  0.0')
cubit.cmd('view up    0.0  1.0  0.0')
cubit.cmd(f'hardcopy "{FileName}" png window 2')
cubit.cmd('graphics window delete 2')
os.startfile(FileName)

FileName = 'Cubit.meg'
import cubit_mesh_export
cubit_mesh_export.export_2D_meg(cubit, FileName)

