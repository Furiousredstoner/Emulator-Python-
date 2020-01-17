print("RAM Loaded")
from Component import *
RAM = Component()           
RAM.RAM = []
RAM.Loaded = True

#def RAM_tick():
 #TICK

def RAM_init():
  RAM.bytes = 16
  for i in range(RAM.bytes):
    RAM.RAM.append(0)
