clear all;
close all;

FileName = 'pmpol.geo';
strLines = readlines(FileName);

FileName = replace(FileName,'.geo','.jpu');
fid = fopen(FileName,'w');
fprintf(fid,'reset\n');

for n = [1:length(strLines)]
	disp(sprintf('line %d',n));
	if startsWith(strLines(n), 'Point')
		data = sscanf(strLines(n),'Point(%d) = {%e,%e,%e,hmesh};',4);
		fprintf(fid,'create vertex %e %e %e\n',data(2:4));
	end
end
for n = [1:length(strLines)]
	if startsWith(strLines(n), 'Line')
		data = sscanf(strLines(n),'Line(%d) = {%d,%d};',3);
		fprintf(fid,'create curve vertex %d %d\n',data(2:3));
	elseif startsWith(strLines(n), 'Circle')
		data = sscanf(strLines(n),'Circle(%d) = {%d,%d,%d};',4);
		fprintf(fid,'create curve arc center vertex %d %d %d\n',data([3,2,4]));
	end
end
for n = [1:length(strLines)]
	if startsWith(strLines(n), 'Curve Loop')
		id = sscanf(strLines(n),'Curve Loop(%d) = ',1);
		Loop{id} = replace(char(regexp(strLines(n), '{(.*?)}', 'match')), {',','-','{','}'}, {' ','','',''});
	end
end
for n = [1:length(strLines)]
	if startsWith(strLines(n), 'Plane Surface')
		id = sscanf(strLines(n),'Plane Surface(%d) = ',1);
		matches = replace(char(regexp(strLines(n), '{(.*?)}', 'match')), {',','{','}'}, {' ','',''});
		ids = sscanf(matches, '%d');
		if length(ids)==1
			fprintf(fid,'create surface curve %s\n',char(Loop(ids)));
		elseif length(ids)==2
			fprintf(fid,'create surface curve %s\n',char(Loop(ids(1))));
			fprintf(fid,'#{id1=Id("surface")}\n');
			fprintf(fid,'create surface curve %s\n',char(Loop(ids(2))));
			fprintf(fid,'#{id2=Id("surface")}\n');
			fprintf(fid,'subtract surface {id2} from surface {id1} imprint\n');
		end
	end
end
nodesets = 0;
for n = [1:length(strLines)]
	if startsWith(strLines(n), 'Physical Surface')
		nodesets = nodesets + 1;
		name = replace(char(regexp(strLines(n), '("(.*?)")', 'match')), {'(',')','"'}, {'','',''});;
		matches = replace(char(regexp(strLines(n), '{(.*?)}', 'match')), {',','{','}'}, {' ','',''});
		ids = sscanf(matches, '%d');
		nodeset_list = "";
		for m = 1:length(ids)
			id = ids(m);
			nodeset_list = strcat(nodeset_list, char(Loop(id)), " ");
		end
		fprintf(fid,'nodeset %d add curve %s\n',nodesets, nodeset_list);
		fprintf(fid,'nodeset %d name "%s"\n',nodesets, name);
	end
end
fclose(fid);

strLines = readlines(FileName);
clipboard('copy', strjoin(strLines, char(10)));
