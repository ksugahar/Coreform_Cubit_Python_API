clear all;
close all;

FileName = 'model_reference.msh';
fid = fopen(FileName, 'r');
	strLine = "";
	while contains(strLine, '$PhysicalNames')~=1
		strLine = fgetl(fid);
	end
	N = fscanf(fid,'%d\n',[1,1]);
	C = textscan(fid,'%d %d %s\n',N);
	PhysicalNames.dimension= C{1};
	PhysicalNames.Tag = C{2};
	PhysicalNames.name = replace(C{3},'"','');
	while contains(strLine, '$Entities')~=1
		strLine = fgetl(fid);
	end
	N = fscanf(fid,'%d\n',[1,4]);
	Entities.numPoints = N(1);
	Entities.numCurves = N(2);
	Entities.numSurfaces = N(3);
	Entities.numVolumes = N(4);
	for n = [1:Entities.numPoints]
		C = textscan(fid,'%d %f %f %f %d ',1, 'Delimiter', ' ');
		Entitties.points(n).pointTag = C{1};
		Entitties.points(n).X = C{2};
		Entitties.points(n).Y = C{3};
		Entitties.points(n).Z = C{4};
		Entitties.points(n).numPhysicalTags = C{5};
		C = textscan(fid,'%d ',Entitties.points(n).numPhysicalTags, 'Delimiter', ' ');
	end
	for n = [1:Entities.numCurves]
		C = textscan(fid,'%d %f %f %f %f %f %f %d ',1, 'Delimiter', ' ');
		Entitties.curves(n).curveTag = C{1};
		Entitties.curves(n).minX = C{2};
		Entitties.curves(n).minY = C{3};
		Entitties.curves(n).minZ = C{4};
		Entitties.curves(n).maxX = C{5};
		Entitties.curves(n).maxY = C{6};
		Entitties.curves(n).maxZ = C{7};
		Entitties.curves(n).numPhysicalTags = C{8};
		C = textscan(fid,'%d ',Entitties.curves(n).numPhysicalTags, 'Delimiter', ' ');
		Entitties.curves(n).PhysicalTag = transpose(cell2mat(C));
		C = textscan(fid,'%d ',1, 'Delimiter', ' ');
		Entitties.curves(n).numBoundaryPoints = C{1};
		C = textscan(fid,'%d ',Entitties.curves(n).numBoundaryPoints, 'Delimiter', ' ');
		Entitties.curves(n).pointTag = transpose(cell2mat(C));
	end
	for n = [1:Entities.numSurfaces]
		C = textscan(fid,'%d %f %f %f %f %f %f %d ',1, 'Delimiter', ' ');
		Entitties.surfaces(n).surfaceTag = C{1};
		Entitties.surfaces(n).minX = C{2};
		Entitties.surfaces(n).minY = C{3};
		Entitties.surfaces(n).minZ = C{4};
		Entitties.surfaces(n).maxX = C{5};
		Entitties.surfaces(n).maxY = C{6};
		Entitties.surfaces(n).maxZ = C{7};
		Entitties.surfaces(n).numPhysicalTags = C{8};
		C = textscan(fid,'%d ',Entitties.surfaces(n).numPhysicalTags, 'Delimiter', ' ');
		Entitties.surfaces(n).PhysicalTag = transpose(cell2mat(C));
		C = textscan(fid,'%d ',1, 'Delimiter', ' ');
		Entitties.surfaces(n).numBoundaryCurves = C{1};
		C = textscan(fid,'%d ',Entitties.surfaces(n).numBoundaryCurves, 'Delimiter', ' ');
		Entitties.surfaces(n).curveTag = transpose(cell2mat(C));
	end
	for n = [1:Entities.numVolumes]
		C = textscan(fid,'%d %f %f %f %f %f %f %d ',1, 'Delimiter', ' ');
		Entitties.volumes(n).volumeTag = C{1};
		Entitties.volumes(n).minX = C{2};
		Entitties.volumes(n).minY = C{3};
		Entitties.volumes(n).minZ = C{4};
		Entitties.volumes(n).maxX = C{5};
		Entitties.volumes(n).maxY = C{6};
		Entitties.volumes(n).maxZ = C{7};
		Entitties.volumes(n).numPhysicalTags = C{8};
		C = textscan(fid,'%d ',Entitties.volumes(n).numPhysicalTags, 'Delimiter', ' ');
		Entitties.volumes(n).PhysicalTag = transpose(cell2mat(C));
		C = textscan(fid,'%d ',1, 'Delimiter', ' ');
		Entitties.volumes(n).numBoundarySurfaces = C{1};
		C = textscan(fid,'%d ',Entitties.volumes(n).numBoundarySurfaces, 'Delimiter', ' ');
		Entitties.volumes(n).surfaceTag = transpose(cell2mat(C));
	end
	while contains(strLine, '$Nodes')~=1
		strLine = fgetl(fid);
	end
	C = textscan(fid,'%d %d %d %d\n',1, 'Delimiter', ' ');
	Nodes.numEntityBlocks = C{1};
	Nodes.numNodes = C{2};
	Nodes.minNodeTag = C{3};
	Nodes.maxNodeTag = C{4};
	for n = [1:Nodes.numEntityBlocks]
		C = textscan(fid,'%d %d %d %d ',1, 'Delimiter', ' ');
		Nodes.EntityBlock(n).entityDim = C{1};
		Nodes.EntityBlock(n).entityTag = C{2};
		Nodes.EntityBlock(n).parametric = C{3};
		Nodes.EntityBlock(n).numNodesInBlock = C{4};
		C = textscan(fid,'%d ',Nodes.EntityBlock(n).numNodesInBlock, 'Delimiter', ' ');
		Nodes.EntityBlock(n).nodeTag = transpose(cell2mat(C));
		C = textscan(fid,'%f %f %f\n',Nodes.EntityBlock(n).numNodesInBlock, 'Delimiter', ' ');
		Nodes.EntityBlock(n).nodeTag = transpose(cell2mat(C));
	end
	while contains(strLine, '$Elements')~=1
		strLine = fgetl(fid);
	end
	C = textscan(fid,'%d %d %d %d\n',1, 'Delimiter', ' ');
	Elements.numEntityBlocks = C{1};
	Elements.numElements = C{2};
	Elements.minElementTag = C{3};
	Elements.maxElementTag = C{4};
	for n = [1:Elements.numEntityBlocks]
		C = textscan(fid,'%d %d %d %d ',1, 'Delimiter', ' ');
		Elements.EntityBlock(n).entityDim = C{1};
		Elements.EntityBlock(n).entityTag = C{2};
		Elements.EntityBlock(n).elementType = C{3};
		Elements.EntityBlock(n).numElementBlock = C{4};
		switch Elements.EntityBlock(n).entityTag
		case 1 %	segm
			C = textscan(fid,'%d %d %d\n',Elements.EntityBlock(n).numElementBlock, 'Delimiter', ' ');
			C = transpose(cell2mat(C));
			Elements.EntityBlock(n).elementTag = C(1,:);
			Elements.EntityBlock(n).nodeTag = C(2:3,:);
		case 2 %	trig
			C = textscan(fid,'%d %d %d %d\n',Elements.EntityBlock(n).numElementBlock, 'Delimiter', ' ');
			C = transpose(cell2mat(C));
			Elements.EntityBlock(n).elementTag = C(1,:);
			Elements.EntityBlock(n).nodeTag = C(2:4,:);
		case 3 %	quad
			C = textscan(fid,'%d %d %d %d %d\n',Elements.EntityBlock(n).numElementBlock, 'Delimiter', ' ');
			C = transpose(cell2mat(C));
			Elements.EntityBlock(n).elementTag = C(1,:);
			Elements.EntityBlock(n).nodeTag = C(2:5,:);
		case 4 %	tet
			C = textscan(fid,'%d %d %d %d %d\n',Elements.EntityBlock(n).numElementBlock, 'Delimiter', ' ');
			C = transpose(cell2mat(C));
			Elements.EntityBlock(n).elementTag = C(1,:);
			Elements.EntityBlock(n).nodeTag = C(2:5,:);
		case 5 %	hex
			C = textscan(fid,'%d %d %d %d %d %d %d %d %d\n',Elements.EntityBlock(n).numElementBlock, 'Delimiter', ' ');
			C = transpose(cell2mat(C));
			Elements.EntityBlock(n).elementTag = C(1,:);
			Elements.EntityBlock(n).nodeTag = C(2:9,:);
		case 6 %	prism
			C = textscan(fid,'%d %d %d %d %d %d %d\n',Elements.EntityBlock(n).numElementBlock, 'Delimiter', ' ');
			C = transpose(cell2mat(C));
			Elements.EntityBlock(n).elementTag = C(1,:);
			Elements.EntityBlock(n).nodeTag = C(2:7,:);
		case 7 %	pyramid
			C = textscan(fid,'%d %d %d %d %d %d %d %d\n',Elements.EntityBlock(n).numElementBlock, 'Delimiter', ' ');
			C = transpose(cell2mat(C));
			Elements.EntityBlock(n).elementTag = C(1,:);
			Elements.EntityBlock(n).nodeTag = C(2:6,:);
		case 15 %	point
			C = textscan(fid,'%d %d\n',Elements.EntityBlock(n).numElementBlock, 'Delimiter', ' ');
			C = transpose(cell2mat(C));
			Elements.EntityBlock(n).elementTag = C(1,:);
			Elements.EntityBlock(n).nodeTag = C(2,:);
		end
	end
fclose(fid);

[filepath, name, ext] = fileparts(mfilename());
FileName = [name, '.mat'];

save(FileName, 'PhysicalNames', 'Entities', 'Nodes', 'Elements');

