print("CPU Loaded")
from Component import *
from RAM import *
import time
import glob
import os
import importlib
CPU = Component() 
 #          PCR  IST   1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
CPU.REGS = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]
# PCR = Program CounteR , IST = InSTruction
CPU.Delay = 1
CPU.Loaded = True
CPU.ROMLoaded = False 
CPU.ListROMS = False
CPU.ROMsDir =  "ROMS/"
CPU.ROMName = ""
CPU.ROMType = ""

def StringCut(char,str):
 for i in range(len(str)):
  if str[0-i] == char:
   return str[0-i+1:]

def CPU_LoadFile(filename):
 with open(os.getcwd() + "/Emulator/" + CPU.ROMsDir + filename,"rb") as f:
  return f.read()


def Require(FileName):
 return importlib.import_module(FileName)

def CPU_ListDir(Dir,FileType):
   CPU.ListROMS = False
   CPU.CurrentDir = os.getcwd() + "/Emulator/" + Dir + "*" + FileType
   CPU.ROMLIST = glob.glob(CPU.CurrentDir)
   for i in range(len(CPU.ROMLIST)):
    print(StringCut("/",CPU.ROMLIST[i]))

def CPU_LocateROM(ROMNAME):
 CPU.CurrentDir = os.getcwd() + "/Emulator/" + CPU.ROMsDir
 CPU.ROMLIST = glob.glob(CPU.CurrentDir + "*" )
 for i in range(len(CPU.ROMLIST)):
  if StringCut("/",CPU.ROMLIST[i]) == "ROMS\\" + ROMNAME:
    return i
  elif i == len(CPU.ROMLIST) and StringCut("/",CPU.ROMLIST[i]) != CPU.ROMsDir + ROMNAME:
    return None

def CPU_LoadROM(ROMNAME):
  CPU.ROMLocation = CPU_LocateROM(ROMNAME)
  if CPU.ROMLocation == None:
    Component.Dialog(CPU,"Error","CPU","Invalid ROM")
  else:
    Component.Dialog(CPU,None,"CPU","Valid ROM")
    if ROMNAME[-2] == "p":
     ROMNAME = ROMNAME[:-3]
     Component.Dialog(CPU,None,"CPU","ROM TYPE: .py")
     CPU.ROMType = "py"
     CPU.ROM = Require(CPU.ROMsDir[:-1]+"."+ROMNAME)
     CPU.ROMLoaded = True
    elif ROMNAME[-2] == "O":
     Component.Dialog(CPU,None,"CPU","ROM TYPE: .ROM")
     CPU.ROMType = "ROM"
     CPU.ROM = CPU_LoadFile(ROMNAME)
     CPU.ROMLoaded = True

def CPU_tick():

  if CPU.ROMLoaded is True:
   time.sleep(CPU.Delay)
   #TICK
   #print(CPU.REGS[0][0])
   #CPU.REGS[0][0] += 1
   if CPU.ROMType == "py":
    CPU.ROMData = CPU.ROM.ROM
    print(CPU.ROMData[0])
   elif CPU.ROMType == "ROM":
    CPU.ROMData = CPU.ROM
    print(CPU.ROMData[0])
  else: #ROM is not loaded
   CPU.List = input("[CPU]: List All ROMS?: ")
   if CPU.List.upper() == "Y":
    CPU.ListROMS = True
   elif CPU.List.upper() == "N":
    CPU.RomName = input("[CPU]: Please Load A ROM: ")
    CPU_LoadROM(CPU.RomName)
   if CPU.ListROMS == True:
     CPU_ListDir(CPU.ROMsDir,".py")
     CPU_ListDir(CPU.ROMsDir,".ROM")

def CPU_init():
  RAM_init()