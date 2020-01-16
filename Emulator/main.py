import importlib
def Require(FileName):
 return importlib.import_module(FileName)
CPU = Require("CPU")

if CPU.CPU.Loaded is True:
  CPU.CPU_init()
while CPU.CPU.Loaded is True:
 CPU.CPU_tick()
 