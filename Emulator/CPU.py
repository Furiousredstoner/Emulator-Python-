print("CPU Loaded")
from Component import *
from RAM import *
from GPU import *
import time
import glob
import os
import sys
import importlib
CPU = Component()
#           PCR  IST   1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
CPU.REGS = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]] 
# PCR = Program CounteR, IST = InSTruction
CPU.LREGActive = False
CPU.RREGActive = False
CPU.AREGADDR = 0 
CPU.BREGADDR = 0 
CPU.CREGADDR = 0
CPU.Delay = 0
CPU.Halt = True # Halt due to invalid instruction
CPU.PRNTDATA = False # Prints ROM Data
CPU.PRNTPC = False # Prints Program Counter - requires PRNTDATA to be True
CPU.PRNTREGS = False # Prints REG Data
CPU.NoRepeat = True #ROM halts at end of program
CPU.Debug = False # prints debug info
CPU.Loaded = True # CPU is loaded
CPU.ROMLoaded = False # if ROM is loaded
CPU.ListROMS = False # if ROM's should be listed
CPU.ROMsDir =  "/ROMS/" # Directory of ROM folder
CPU.EMUDir = "/Emulator/" # Directory of Emulator Folder 
CPU.ROMName = "" #Placeholder
CPU.ROMType = "" #Placeholder
CPU.ROMBytes = 11 # number of bytes of ROM length
 
def StringCut(char,str):
 if sys.platform.startswith("win32"):
  for i in range(len(str)):
   if str[0-i] == char:
    return str[0-i+1:]
 elif sys.platform.startswith("linux"):
  for i in range(1,len(str)):
   if str[len(str)-i] == char:
    return str[len(str)-i+1:]

# if sys.platform.startswith("win32"):
#  Windows related code here
# elif sys.platform.startswith("linux"):
#  Linux related code here

def CPU_LoadFile(filename):
 if sys.platform.startswith("win32"):
  #with open(os.getcwd() + CPU.EMUDir + CPU.ROMsDir + filename,"rb") as f:
  with open(os.getcwd() + CPU.ROMsDir + filename,"rb") as f:
   return f.read()
 elif sys.platform.startswith("linux"):
  with open(os.getcwd() + CPU.ROMsDir + filename,"rb") as f:
   return f.read()

def Require(FileName):
 return importlib.import_module(FileName)


def CPU_ListDir(Dir,FileType):
 CPU.ListROMS = False
 if sys.platform.startswith("win32"):
  #CPU.CurrentDir = os.getcwd() + CPU.EMUDir + Dir + "*" + FileType
  CPU.CurrentDir= os.getcwd()+CPU.ROMsDir+"*"+FileType
  CPU.ROMLIST = glob.glob(CPU.CurrentDir)
  for i in range(len(CPU.ROMLIST)):
   print(StringCut("/",CPU.ROMLIST[i]))
 elif sys.platform.startswith("linux"):
  CPU.CurrentDir = os.getcwd() + Dir + "*" + FileType
  CPU.ROMLIST = glob.glob(CPU.CurrentDir)
  for i in range(len(CPU.ROMLIST)):
   print(StringCut("/",CPU.ROMLIST[i]))

def CPU_LocateROM(ROMNAME):
 if sys.platform.startswith("win32"):
  #CPU.CurrentDir = os.getcwd() + CPU.EMUDir + CPU.ROMsDir
  CPU.CurrentDir = os.getcwd() + CPU.ROMsDir
  print("Scanning: " + CPU.CurrentDir)
  CPU.ROMLIST = glob.glob(CPU.CurrentDir + "*" )
  for i in range(len(CPU.ROMLIST)):
   if StringCut("/",CPU.ROMLIST[i]) == "ROMS\\" + ROMNAME:
    return i
   elif i == len(CPU.ROMLIST) and StringCut("/",CPU.ROMLIST[i]) != CPU.ROMsDir + ROMNAME:
    return None
 elif sys.platform.startswith("linux"):
  CPU.CurrentDir = os.getcwd() + CPU.ROMsDir
  print("Scanning: " + CPU.CurrentDir)
  CPU.ROMLIST = glob.glob(CPU.CurrentDir + "*" )
  for i in range(len(CPU.ROMLIST)):
   if StringCut("/",CPU.ROMLIST[i]) == ROMNAME:
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
     #print(CPU.ROMsDir[:-1]+"."+ROMNAME)
     if sys.platform.startswith("linux"):
      CPU.ROM = Require(CPU.ROMsDir[1:-1]+"."+ROMNAME) # Linux likes "folder.folder2.file
      CPU.ROMData = CPU.ROM.ROM
      Component.Dialog(CPU,None,"CPU","ROM Length: "+str(len(CPU.ROMData))+" Bytes")
      CPU.ROMLoaded = True
     else:
      CPU.ROM = Require(CPU.ROMsDir[:-1]+"."+ROMNAME) # Windows likes "/folder/folder2.file
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
 GPU_init()

def ToHex(num,prefix=False):
 if prefix:
  if num <= 0x0F:
   return "0x0"+hex(num).upper()[2:]
  else:
   return "0x"+hex(num).upper()[2:]
 else:
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
 
def CPU_LOAD(): #LOAD
 if CPU.Debug:
  Component.Dialog(CPU,None,"CPU","Executing Instruction [LOAD]")
 CPU.AREGADDR, CPU.BREGADDR = CPU_ActiveREGS(CPU.SLOT1)
 if CPU.AREGADDR is not None:
  CPU.REGS[CPU.AREGADDR][0] = (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA) #LOAD A
 if CPU.BREGADDR is not None:
  CPU.REGS[CPU.BREGADDR][0] = (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA) #LOAD B
 _,CPU.CREGADDR = CPU_ActiveREGS(CPU.SLOT2)
 if CPU.CREGADDR is not None:
  CPU.REGS[CPU.CREGADDR][0] = (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA) #LOAD C
###########################################################################################################################
def CPU_ADD(): #ADD
 if CPU.Debug:
  Component.Dialog(CPU,None,"CPU","Executing Instruction [ADD]")
 CPU.AREGADDR, CPU.BREGADDR = CPU_ActiveREGS(CPU.SLOT1)
 _, CPU.CREGADDR = CPU_ActiveREGS(CPU.SLOT2)
 if CPU.AREGADDR is not None and CPU.BREGADDR is not None:  
  if (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA) > 0:
   if CPU.CREGADDR is not None:
    CPU.REGS[CPU.CREGADDR][0] = CPU.REGS[CPU.AREGADDR][0] + (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA)
   else:
    CPU_Halt("REG C is not defined")
  else:
   if CPU.CREGADDR is not None:
    CPU.REGS[CPU.CREGADDR][0] = CPU.REGS[CPU.AREGADDR][0] + CPU.REGS[CPU.BREGADDR][0] # A + B = C
   else:
    CPU_Halt("REG C is not defined")
###########################################################################################################################
def CPU_SUBT(): #SUBT
 if CPU.Debug:
  Component.Dialog(CPU,None,"CPU","Executing Instruction [SUBT]")
 CPU.AREGADDR, CPU.BREGADDR = CPU_ActiveREGS(CPU.SLOT1)
 _, CPU.CREGADDR = CPU_ActiveREGS(CPU.SLOT2)
 if CPU.AREGADDR is not None and CPU.BREGADDR is not None:  
  if (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA) > 0:
   if CPU.CREGADDR is not None:
    CPU.REGS[CPU.CREGADDR][0] = CPU.REGS[CPU.AREGADDR][0] - (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA)
   else:
    CPU_Halt("REG C is not defined")
  else:
   if CPU.CREGADDR is not None:
    CPU.REGS[CPU.CREGADDR][0] = CPU.REGS[CPU.AREGADDR][0] - CPU.REGS[CPU.BREGADDR][0] # A - B = C
   else:
    CPU_Halt("REG C is not defined")
###########################################################################################################################
def CPU_MULT(): #MULT
 if CPU.Debug:
  Component.Dialog(CPU,None,"CPU","Executing Instruction [MULT]")
 CPU.AREGADDR, CPU.BREGADDR = CPU_ActiveREGS(CPU.SLOT1)
 _, CPU.CREGADDR = CPU_ActiveREGS(CPU.SLOT2)
 if CPU.AREGADDR is not None and CPU.BREGADDR is not None:  
  if (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA) > 0:
   if CPU.CREGADDR is not None:
    CPU.REGS[CPU.CREGADDR][0] = CPU.REGS[CPU.AREGADDR][0] * (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA)
   else:
    CPU_Halt("REG C is not defined")
  else:
   if CPU.CREGADDR is not None:
    CPU.REGS[CPU.CREGADDR][0] = CPU.REGS[CPU.AREGADDR][0] * CPU.REGS[CPU.BREGADDR][0] # A * B = C
   else:
    CPU_Halt("REG C is not defined")
###########################################################################################################################
def CPU_DIV(): #DIV
 if CPU.Debug:
  Component.Dialog(CPU,None,"CPU","Executing Instruction [DIV]")
 CPU.AREGADDR, CPU.BREGADDR = CPU_ActiveREGS(CPU.SLOT1)
 _, CPU.CREGADDR = CPU_ActiveREGS(CPU.SLOT2)
 if CPU.AREGADDR is not None and CPU.BREGADDR is not None:  
  if (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA) > 0:
   if CPU.CREGADDR is not None:
    CPU.REGS[CPU.CREGADDR][0] = CPU.REGS[CPU.AREGADDR][0] / (CPU.SLOT3+CPU.SLOT4+CPU.SLOT5+CPU.SLOT6+CPU.SLOT7+CPU.SLOT8+CPU.SLOT9+CPU.SLOTA)
   else:
    CPU_Halt("REG C is not defined")
  else:
   if CPU.CREGADDR is not None:
    CPU.REGS[CPU.CREGADDR][0] = CPU.REGS[CPU.AREGADDR][0] / CPU.REGS[CPU.BREGADDR][0] # A / B = C
   else:
    CPU_Halt("REG C is not defined") 
###########################################################################################################################
def CPU_DVCSND(): #DVCSND
 if CPU.Debug:
  Component.Dialog(CPU,None,"CPU","Executing Instruction [DVCSND]")
 GPU_DVCSND(CPU.SLOT3,CPU.SLOT4,CPU.SLOT5,CPU.SLOT6,CPU.SLOT7,CPU.SLOT8,CPU.SLOT9,CPU.SLOTA)
###########################################################################################################################
def CPU_PLCHDR():
 return True
#                             |INDX|  INST
CPU.OPCODELIST = [CPU_LOAD,   #0x00   0x01
                  CPU_ADD,    #0x01   0x02
                  CPU_SUBT,   #0x02   0x03
                  CPU_MULT,   #0x03   0x04
                  CPU_DIV,    #0x04   0x05
                  CPU_PLCHDR, #0x05   0x06
                  CPU_PLCHDR, #0x06   0x07
                  CPU_PLCHDR, #0x07   0x08
                  CPU_PLCHDR, #0x08   0x09
                  CPU_PLCHDR, #0x09   0x0A
                  CPU_PLCHDR, #0x0A   0x0B
                  CPU_PLCHDR, #0x0B   0x0C
                  CPU_PLCHDR, #0x0C   0x0D
                  CPU_PLCHDR, #0x0D   0x0E
                  CPU_PLCHDR, #0x0E   0x0F
                  CPU_PLCHDR, #0x0F   0x10
                  CPU_PLCHDR, #0x10   0x11
                  CPU_PLCHDR, #0x11   0x12
                  CPU_PLCHDR, #0x12   0x13
                  CPU_PLCHDR, #0x13   0x14
                  CPU_PLCHDR, #0x14   0x15
                  CPU_PLCHDR, #0x15   0x16
                  CPU_PLCHDR, #0x16   0x17
                  CPU_DVCSND] #0x17   0x18
def CPU_tick():
 GPU_tick()
 if CPU.ROMLoaded is False: #ROM is not loaded
  CPU.List = input("[CPU]: List All ROMS?: ")
  if CPU.List.upper() == "Y":
   CPU.ListROMS = True
  elif CPU.List.upper() == "N":
   CPU.RomName = input("[CPU]: Please Load A ROM: ")
   CPU_LoadROM(CPU.RomName)
  if CPU.ListROMS:
   CPU_ListDir(CPU.ROMsDir,".py")
   CPU_ListDir(CPU.ROMsDir,".ROM")
 if CPU.ROMLoaded is True:
  #time.sleep(CPU.Delay)
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
  if CPU.PRNTDATA:
   if CPU.PRNTPC:
    print(" "+ToHex(CPU.REGS[0][0],False), ToHex(CPU.REGS[1][0],False), ToHex(CPU.SLOT1,False), ToHex(CPU.SLOT2,False), ToHex(CPU.SLOT3,False), ToHex(CPU.SLOT4,False), ToHex(CPU.SLOT5,False), ToHex(CPU.SLOT6,False), ToHex(CPU.SLOT7,False), ToHex(CPU.SLOT8,False), ToHex(CPU.SLOT9,False), ToHex(CPU.SLOTA,False)+" ")
   else:
    print(ToHex(CPU.REGS[1][0],False), ToHex(CPU.SLOT1,False), ToHex(CPU.SLOT2,False), ToHex(CPU.SLOT3,False), ToHex(CPU.SLOT4,False), ToHex(CPU.SLOT5,False), ToHex(CPU.SLOT6,False), ToHex(CPU.SLOT7,False), ToHex(CPU.SLOT8,False), ToHex(CPU.SLOT9,False), ToHex(CPU.SLOTA,False)+" ")
########################################################################################
  #DECODE
  if CPU.REGS[1][0] > 0x00 and CPU.REGS[1][0] <= len(CPU.OPCODELIST) :
   CPU.OPCODELIST[CPU.REGS[1][0]-1]()
########################################################################################
  #Halt  
  else:
   if CPU.Halt:
    if CPU.Debug:
     Component.Dialog(CPU,None,"CPU","INVALID INSTRUCTION:  ["+ToHex(CPU.REGS[1][0],True)+"]")
     CPU_Halt("INVALID INSTRUCTION:" + "["+ToHex(CPU.REGS[1][0],True)+"]"+" AT PC: "+ToHex(CPU.REGS[0][0],True))
    else:
     CPU_Halt("Unknown , Enable Debug for logging (CPU.py , Line 24)")
    #Increment PC
  if CPU.PRNTREGS:
   print(CPU.REGS[2:])
  if CPU.REGS[0][0] != len(CPU.ROMData)-CPU.ROMBytes:
   CPU.REGS[0][0] += CPU.ROMBytes
  else:
   if CPU.NoRepeat:
    CPU_Halt("END OF PROGRAM")
    CPU.REGS[0][0] = 0
