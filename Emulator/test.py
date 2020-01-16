from Component import *
Component.Dialog(Component,None,"BITCH","I AM BITCH")

Main = Component()

Main.whatever = 54

Component.Dialog(Main,None,"Main",str(Main.whatever))


def ToHex(num,prefix):
  if prefix == True:
   return "0x"+hex(num).upper()[2:]
  elif prefix == False:
   return hex(num).upper()[2:]


def Main_testfunction():
  Main.new = (ToHex(0xFF-Main.whatever,True))
  print(Main.new)

Main_testfunction()

def Main_LoadFile(filename):
 with open(filename,"rb") as f:
  d = f.read()
  for i in range(len(d)):
   print(ToHex(d[i],False),end = " ")

Main_LoadFile("test.tgr")

