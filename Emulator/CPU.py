print("CPU Loaded")
from Component import *
from RAM import *
import time
import glob
import os
import sys
import importlib
CPU = Component() 
 #          PCR  IST   1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
CPU.REGS = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]] 
# PCR = Program CounteR, IST = InSTruction
CPU.LREGActive = False
CPU.RREGActive = False
CPU.LREGADDR = 0 
CPU.RREGADDR = 0 
CPU.Delay = 0.05
CPU.Halt = False
CPU.PRNTDATA = False
CPU.PRNTPC = False
CPU.NoRepeat = True
CPU.Debug = True
CPU.Loaded = True
CPU.ROMLoaded = False 
CPU.ListROMS = False
CPU.ROMsDir =  "ROMS/"
CPU.ROMName = ""
CPU.ROMType = ""
CPU.ROMBytes = 11

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
    Component.Dialog(CPU,"Error","CPU","Check if Location/Spelling is correct")
  else:
    Component.Dialog(CPU,None,"CPU","Valid ROM")
    if ROMNAME[-2] == "p":
     ROMNAME = ROMNAME[:-3]
     Component.Dialog(CPU,None,"CPU","ROM TYPE: .py")
     CPU.ROMType = "py"
     CPU.ROM = Require(CPU.ROMsDir[:-1]+"."+ROMNAME)
     CPU.ROMData = CPU.ROM.ROM
     Component.Dialog(CPU,None,"CPU","ROM Length: "+str(len(CPU.ROMData))+" Bytes")
     CPU.ROMLoaded = True
    elif ROMNAME[-2] == "O":
     Component.Dialog(CPU,None,"CPU","ROM TYPE: .ROM")
     CPU.ROMType = "ROM"
     CPU.ROM = CPU_LoadFile(ROMNAME)
     CPU.ROMData = CPU.ROM
     Component.Dialog(CPU,None,"CPU","ROM Length: "+str(len(CPU.ROMData))+" Bytes")
     CPU.ROMLoaded = True
    else:
       CPU.ROMType = StringCut(".",ROMNAME)
       Component.Dialog(CPU,"Error","CPU","Invalid ROM Format")
       Component.Dialog(CPU,"Error","CPU","Got ."+CPU.ROMType+" Expected .py or .ROM")

def CPU_init():
  RAM_init()

def ToHex(num,prefix):
 if prefix == True:
  if num <= 0x0F:
   return "0x0"+hex(num).upper()[2:]
  else:
   return "0x"+hex(num).upper()[2:]
 elif prefix == False:
  if num <= 0x0F:
    return "0"+hex(num).upper()[2:]
  else:
   return hex(num).upper()[2:]


def CPU_Halt(reason):
 Component.Dialog(CPU,"Error","CPU","CPU HALTED:")
 Component.Dialog(CPU,"Error","CPU","CAUSE OF HALT: "+ reason)
 CPU.ROMLoaded = False 

def CPU_ActiveREGS(REGS):
 LREG = int(ToHex(REGS,False)[0],16)
 RREG = int(ToHex(REGS,False)[1],16)
 if LREG > 0 and RREG == 0:
   CPU.LREGActive = True
   CPU.RREGActive = False
 elif RREG > 0 and LREG == 0:
   CPU.RREGActive = True
   CPU.LREGActive = False
 elif RREG > 0 and LREG > 0:
   CPU.RREGActive = True
   CPU.LREGActive = True
 else:
   CPU.LREGActive = False
   CPU.RREGActive = False
 if   CPU.LREGActive is True and CPU.RREGActive is False:
  return LREG + 1, None
 elif CPU.LREGActive is False and CPU.RREGActive is True:
  return None, RREG + 1
 elif CPU.LREGActive is True and CPU.RREGActive is True:
  return LREG + 1 ,RREG + 1
 else:
  return None,None
     
def CPU_tick():
 if CPU.ROMLoaded is False: #ROM is not loaded
  CPU.List = input("[CPU]: List All ROMS?: ")
  if CPU.List.upper() == "Y":
   CPU.ListROMS = True
  elif CPU.List.upper() == "N":
   CPU.RomName = input("[CPU]: Please Load A ROM: ")
   CPU_LoadROM(CPU.RomName)
  if CPU.ListROMS == True:
   CPU_ListDir(CPU.ROMsDir,".py")
   CPU_ListDir(CPU.ROMsDir,".ROM")
 if CPU.ROMLoaded is True:
  time.sleep(CPU.Delay)
  #FETCH
  CPU.REGS[1][0]  = CPU.ROMData[CPU.REGS[0][0]+0]  #INST
  CPU.SLOT1       = CPU.ROMData[CPU.REGS[0][0]+1]  #REGS AB
  CPU.SLOT2       = CPU.ROMData[CPU.REGS[0][0]+2]  #REG C
  CPU.SLOT3       = CPU.ROMData[CPU.REGS[0][0]+3]  #IMM 1
  CPU.SLOT4       = CPU.ROMData[CPU.REGS[0][0]+4]  #IMM 2
  CPU.SLOT5       = CPU.ROMData[CPU.REGS[0][0]+5]  #IMM 3
  CPU.SLOT6       = CPU.ROMData[CPU.REGS[0][0]+6]  #IMM 4
  CPU.SLOT7       = CPU.ROMData[CPU.REGS[0][0]+7]  #IMM 5
  CPU.SLOT8       = CPU.ROMData[CPU.REGS[0][0]+8]  #IMM 6
  CPU.SLOT9       = CPU.ROMData[CPU.REGS[0][0]+9]  #IMM 7
  CPU.SLOTA       = CPU.ROMData[CPU.REGS[0][0]+10] #IMM 8
  if CPU.PRNTDATA == True:
   if CPU.PRNTPC == True:
    print(" "+ToHex(CPU.REGS[0][0],False), ToHex(CPU.REGS[1][0],False), ToHex(CPU.SLOT1,False), ToHex(CPU.SLOT2,False), ToHex(CPU.SLOT3,False), ToHex(CPU.SLOT4,False), ToHex(CPU.SLOT5,False), ToHex(CPU.SLOT6,False), ToHex(CPU.SLOT7,False), ToHex(CPU.SLOT8,False), ToHex(CPU.SLOT9,False), ToHex(CPU.SLOTA,False)+" ")
   else:
    print(ToHex(CPU.REGS[1][0],False), ToHex(CPU.SLOT1,False), ToHex(CPU.SLOT2,False), ToHex(CPU.SLOT3,False), ToHex(CPU.SLOT4,False), ToHex(CPU.SLOT5,False), ToHex(CPU.SLOT6,False), ToHex(CPU.SLOT7,False), ToHex(CPU.SLOT8,False), ToHex(CPU.SLOT9,False), ToHex(CPU.SLOTA,False)+" ")
  #DECODE
  if   CPU.REGS[1][0] == 0x00: #NOP
   if CPU.Debug == True:
    Component.Dialog(CPU,None,"CPU","Executing Instruction [NOP]") #EXECUTE
  elif CPU.REGS[1][0] == 0x01: #LOAD                               #\/
   if CPU.Debug == True:
    Component.Dialog(CPU,None,"CPU","Executing Instruction [LOAD]")
   CPU.LREGADDR, CPU.RREGADDR = CPU_ActiveREGS(CPU.SLOT1)
   if CPU.LREGADDR is not None:
    CPU.REGS[CPU.LREGADDR][0] = (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA)
   if CPU.RREGADDR is not None:
    CPU.REGS[CPU.RREGADDR][0] = (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA)
   _,CPU.RREGADDR = CPU_ActiveREGS(CPU.SLOT2)
   if CPU.RREGADDR is not None:
    CPU.REGS[CPU.RREGADDR][0] = (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA)
  else:
   if CPU.Halt == True:
    if CPU.Debug == True:
     Component.Dialog(CPU,None,"CPU","INVALID INSTRUCTION:  ["+ToHex(CPU.REGS[1][0],True)+"]")
    CPU_Halt("INVALID INSTRUCTION:" + "["+ToHex(CPU.REGS[1][0],True)+"]"+" AT PC: "+ToHex(CPU.REGS[0][0],True))
  #Increment PC
  if CPU.REGS[0][0] != len(CPU.ROMData)-CPU.ROMBytes:
   CPU.REGS[0][0] += CPU.ROMBytes
  else:
   if CPU.NoRepeat == True:
    CPU_Halt("END OF PROGRAM")
   CPU.REGS[0][0] = 0