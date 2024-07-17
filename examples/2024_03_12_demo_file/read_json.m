clear all;
close all;

FileName = 'model.json';

jsonText = fileread(FileName);

data = jsondecode(jsonText);

disp('data -----------------')
disp(data)

disp('data.grid -----------------')
disp(data.grid);

disp('data.grid.cell_node_ids -----------------')
disp(data.grid.cell_node_ids);

disp('data.grid.reffes -----------------')
disp(data.grid.reffes );

disp('data.face_vertices_1 -----------------')
disp(data.face_vertices_1);
disp('data.face_vertices_2 -----------------')
disp(data.face_vertices_2);
disp('data.face_vertices_3 -----------------')
disp(data.face_vertices_3);


disp('data.labeling -----------------')
disp(data.labeling);

disp('data.labeling.names -----------------')
disp(data.labeling.names);
