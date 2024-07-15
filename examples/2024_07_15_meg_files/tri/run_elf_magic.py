import numpy, os, sys, shutil
from ctypes import *
from numpy.ctypeslib import ndpointer 

for p in os.environ['PATH'].split(os.pathsep):
	if os.path.isdir(p):
		os.add_dll_directory(p)

dll = cdll.LoadLibrary("../../magh1501.dll")

dll.START.restype = None
dll.START.argtypes = [c_char_p]

dll.SetHBID.restype = None
dll.SetHBID.argtypes = [numpy.ctypeslib.ndpointer(dtype = c_int)]

dll.SetHBCU.restype = None
dll.SetHBCU.argtypes = [numpy.ctypeslib.ndpointer(dtype = c_double), numpy.ctypeslib.ndpointer(dtype = c_double)]

ENAME = b'C:\\ELF500\\bin\\ELFERR.def/'
dll.SetELFERR(ENAME)

FILENAME = b"Cubit/"
mu0 = 4*numpy.pi*1e-7;
dll.START(FILENAME)

nCASE = 2
if nCASE==1:
	mu_s = [10,100,1000,10000,100000]
elif nCASE==2:
	mu_s = [100000]

for mu in mu_s:
	dll.SetHBID(numpy.array([1]))
	dll.SetHBCU(numpy.array([0.0]),numpy.array([0.0]))
	dll.SetHBCU(numpy.array([1.0]),numpy.array([mu*mu0]))
	dll.SetHBID(numpy.array([0]))
	dll.SolMOME()
shutil.copy("Cubit.mag",f"CASE_{nCASE}.mag")
shutil.copy("Cubit.mao",f"CASE_{nCASE}.mao")
dll.SolEND()

