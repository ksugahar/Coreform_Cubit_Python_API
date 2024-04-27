import os, sys
import re

print(os.getcwd())
FileName = 'pmpol.geo'
cubit.reset()
with  open(FileName, 'r', encoding="utf8") as fid:
  strLines = fid.readlines()

#for n in range(len(strLines)):
for n in range(77):
  strLine = strLines[n]
  if len(strLine)==0:
    print("")
  elif strLine[:2]=='//':
    print("")
  elif strLine[:4]=='Mesh':
    print(strLines[n])
  elif strLine[:5]=='Point':
    pattern = r"Point\((?P<id>\d+)\) = \{(?P<x>[+-]?0|[+-]?\d+\.?\d*(?:[Ee][+-]?\d+)),(?P<y>[+-]?0|[+-]?\d+\.?\d*(?:[Ee][+-]?\d+)),(?P<z>[+-]?0|[+-]?\d+\.?\d*(?:[Ee][+-]?\d+)),hmesh\};"
    match = re.match(pattern, strLine)
    vertex = cubit.create_vertex(float(match.group('x')), float(match.group('y')), float(match.group('z')))
    vertex.set_entity_name('Point_' + match.group('id'))
  elif strLine[:4]=='Line':
    pattern = r"Line\((?P<id>\d+)\) = \{(?P<p1>\d+),(?P<p2>\d+)\};"
    match = re.match(pattern, strLine)
    curve = cubit.create_curve(cubit.vertex(int(match.group('p1'))), cubit.vertex(int(match.group('p2'))))
    curve.set_entity_name('Line_' + match.group('id'))
  elif strLine[:6]=='Circle':
    pattern = r"Circle\((?P<id>\d+)\) = \{(?P<p1>\d+),(?P<p2>\d+),(?P<p3>\d+)\};"
    match = re.match(pattern, strLine)
    cubit.cmd(f'create curve arc center vertex {int(match.group("p2"))} {int(match.group("p1"))} {int(match.group("p3"))}')
    curve.set_entity_name('Circle_' + match.group('id'))
  elif strLine[:10]=='Curve Loop':
    print(strLine[0:20])
#   pattern = r"Curve Loop\((?P<id>\d+)\) = \{(?P<p1>\d+),(?P<p2>\d+),(?P<p3>\d+),(?P<p4>\d+)\};"
    pattern = r"Curve Loop\((?P<id>\d+)\) = \{(?P<pp>.*?)\}(?=(?:\s+|=))"
    match = re.match(pattern, strLine)
    print(match.group('id'))



