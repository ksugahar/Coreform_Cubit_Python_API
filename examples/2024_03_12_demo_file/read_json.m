clear all;
close all;

load('Gmsh2mat.mat')

FileName = 'model.json';

jsonText = fileread(FileName);

json = jsondecode(jsonText);

disp('json -----------------')
disp(json)

disp('json.grid -----------------')
disp(json.grid);

disp('json.grid.cell_node_ids -----------------')
disp(json.grid.cell_node_ids);

disp('json.grid.reffes -----------------')
disp(json.grid.reffes );

disp('json.face_vertices_1 -----------------')
disp(json.face_vertices_1);
disp('json.face_vertices_2 -----------------')
disp(json.face_vertices_2);
disp('json.face_vertices_3 -----------------')
disp(json.face_vertices_3);


disp('json.labeling -----------------')
disp(json.labeling);

for n = [1:length(Nodes.EntityBlock)]
	disp([n, Nodes.EntityBlock(n).entityTag])
end

for n = [1:length(Elements.EntityBlock)]
	disp([n, Elements.EntityBlock(n).entityTag])
end


gmsh.labeling.names = PhysicalNames.name(ismember(PhysicalNames.dimension, [0,2,3]));
gmsh.labeling.entities_0 = Elements.EntityBlock.entityTag;

%下記は間違い
%gmsh.labeling.tags = PhysicalNames.Tag(ismember(PhysicalNames.dimension, [0,2,3]));

switch 0
case 1
	disp('labeling.names -----------------')
	disp(json.labeling.names);
	disp(gmsh.labeling.names);
case 2
	disp('labeling.entities_0 -----------------')
	x = json.labeling.entities_0;
	disp(x');
	x = gmsh.labeling.entities_0;
	disp(x');
end
