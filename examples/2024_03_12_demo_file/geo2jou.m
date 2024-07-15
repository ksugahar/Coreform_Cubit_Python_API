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
		matches = replace(replace(char(regexp(strLines(n), '{(.*?)}', 'match')), ',', ' '),'-','');
		fprintf(fid,'create surface curve %s\n', matches(2:end-1));
	end
end
fclose(fid);

strLines = readlines(FileName);
clipboard('copy', strjoin(strLines, char(10)));
