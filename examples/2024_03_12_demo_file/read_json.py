import json
from numpy import *

FileName = 'model.json'
fid = open(FileName, "r")
functions = json.load(fid)
print(functions.keys())
print(functions["D"])
print(functions["version"])

print(functions["grid"].keys())


print(type(functions["labeling"]))
print(functions["labeling"].keys())

print(functions["labeling"]["tags"])
print(shape(functions["labeling"]["entities_0"]))
print(shape(functions["labeling"]["entities_1"]))
print(shape(functions["labeling"]["entities_2"]))
print(shape(functions["labeling"]["entities_3"]))
