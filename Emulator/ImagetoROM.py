import os,sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
#Main Code
type = "" # placeholder
Images = [] # images go here

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
   
def XYIMMRange(t,v):
 if t == "x":
  if v <= 255:
   xHex = int(ToHex(v,True),16)
   out.write(bytes([0x01,0x00,0x0A,xHex,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # writes data to file buffer
  elif v > 255 and v <= 510:
   xHex = int(ToHex((v-255),True),16)
   out.write(bytes([0x01,0x00,0x0A,0xFF,xHex,0x00,0x00,0x00,0x00,0x00,0x00])) # writes data to file buffer
  elif v >= 510 and v <= 765:
   xHex = int(ToHex((v-510),True),16)
   out.write(bytes([0x01,0x00,0x0A,0xFF,0xFF,xHex,0x00,0x00,0x00,0x00,0x00])) # writes data to file buffer
  elif v >= 765 and v <= 1020:
   xHex = int(ToHex((v-765),True),16)
   out.write(bytes([0x01,0x00,0x0A,0xFF,0xFF,0xFF,xHex,0x00,0x00,0x00,0x00])) # writes data to file buffer
  elif v >= 1020 and v <= 1275:
   xHex = int(ToHex((v-1020),True),16)
   out.write(bytes([0x01,0x00,0x0A,0xFF,0xFF,0xFF,0xFF,xHex,0x00,0x00,0x00])) # writes data to file buffer
  elif v >= 1275 and v <= 1530:
   xHex = int(ToHex((v-1275),True),16)
   out.write(bytes([0x01,0x00,0x0A,0xFF,0xFF,0xFF,0xFF,0xFF,xHex,0x00,0x00])) # writes data to file buffer
  elif v >= 1530 and v <= 1785:
   xHex = int(ToHex((v-1530),True),16)
   out.write(bytes([0x01,0x00,0x0A,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,xHex,0x00])) # writes data to file buffer
  elif v >= 1785 and v <= 2040:
   xHex = int(ToHex((v-1785),True),16)
   out.write(bytes([0x01,0x00,0x0A,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,xHex])) # writes data to file buffer
 elif t == "y":
  if v <= 255:
   yHex = int(ToHex(v,True),16)
   out.write(bytes([0x01,0x00,0x0B,yHex,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # writes data to file buffer
  elif v > 255 and v <= 510:
   yHex = int(ToHex((v-255),True),16)
   out.write(bytes([0x01,0x00,0x0B,0xFF,yHex,0x00,0x00,0x00,0x00,0x00,0x00])) # writes data to file buffer
  elif v >= 510 and v <= 765:
   yHex = int(ToHex((v-510),True),16)
   out.write(bytes([0x01,0x00,0x0B,0xFF,0xFF,yHex,0x00,0x00,0x00,0x00,0x00])) # writes data to file buffer
  elif v >= 765 and v <= 1020:
   yHex = int(ToHex((v-765),True),16)
   out.write(bytes([0x01,0x00,0x0B,0xFF,0xFF,0xFF,yHex,0x00,0x00,0x00,0x00])) # writes data to file buffer
  elif v >= 1020 and v <= 1275:
   yHex = int(ToHex((v-1020),True),16)
   out.write(bytes([0x01,0x00,0x0B,0xFF,0xFF,0xFF,0xFF,yHex,0x00,0x00,0x00])) # writes data to file buffer
  elif v >= 1275 and v <= 1530:
   yHex = int(ToHex((v-1275),True),16)
   out.write(bytes([0x01,0x00,0x0B,0xFF,0xFF,0xFF,0xFF,0xFF,yHex,0x00,0x00])) # writes data to file buffer
  elif v >= 1530 and v <= 1785:
   yHex = int(ToHex((v-1530),True),16)
   out.write(bytes([0x01,0x00,0x0B,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,yHex,0x00])) # writes data to file buffer
  elif v >= 1785 and v <= 2040:
   yHex = int(ToHex((v-1785),True),16)
   out.write(bytes([0x01,0x00,0x0B,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,yHex])) # writes data to file buffer


if len(sys.argv) >= 2:
 while type != ".ROM" and type != ".py":
  type = input("Which file format to convert to (.ROM or .py): ")
  Filename = input("name of output file: ")
##################################################################
 if sys.platform.startswith("win32"):
  #  Windows related code here
  if len(sys.argv) > 2:
   for i in range(len(sys.argv)-1):
    Images.append(pygame.image.load_extended(sys.argv[i+1]))
  else:
    Images.append(pygame.image.load_extended(sys.argv[1]))
  if   type == ".ROM":
   out = open(Filename+type,"wb")
   for i in range(len(Images)):
    ImageWidth  = Images[i].get_width()
    ImageHeight = Images[i].get_height()
    print("Image is "+str(ImageWidth) +" x "+str(ImageHeight))
    if ImageWidth > 2040 or ImageHeight > 2040:
     if   i == 0:
      print("Ouch your "+str(i+1)+"st Image is too big , maximum size is (2040 x 2040), the width and/or height of your image exceeds this")
     elif i == 1:
      print("Ouch your "+str(i+1)+"nd Image is too big , maximum size is (2040 x 2040), the width and/or height of your image exceeds this")
     elif i == 2:
      print("Ouch your "+str(i+1)+"rd Image is too big , maximum size is (2040 x 2040), the width and/or height of your image exceeds this")
     else:
      print("Ouch your "+str(i+1)+"th Image is too big , maximum size is (2040 x 2040), the width and/or height of your image exceeds this")
     sys.exit() 
    for y in range(ImageHeight):
     for x in range(ImageWidth):
      position = (x,y)
      Color = Images[i].get_at(position)
      XYIMMRange("x",x)
      XYIMMRange("y",y)
      out.write(bytes([0x18,0x00,0x0A,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # setX
      out.write(bytes([0x18,0x01,0x0B,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # setY
      print(Color[0],Color[1],Color[2],Color[3])
      out.write(bytes([0x18,0x02,0x00,int(ToHex(Color[0],True),16),int(ToHex(Color[1],True),16),int(ToHex(Color[2],True),16),int(ToHex(Color[3],True),16),0x00,0x00,0x00,0x00])) # SETRGB
      out.write(bytes([0x18,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # Plot
    out.write(bytes([0x18,0x05,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # Update
    print("Done!")
    sys.exit()     
  elif type == ".py":
   print("")
#################################################################
 elif sys.platform.startswith("linux"):
  #  Linux related code here
  if len(sys.argv) > 2:
   for i in range(len(sys.argv)-1):
    Images.append(pygame.image.load_extended(sys.argv[i+1]))
  else:
    Images.append(pygame.image.load_extended(sys.argv[1]))
  if   type == ".ROM":
   out = open(Filename+type,"wb")
   for i in range(len(Images)):
    ImageWidth  = Images[i].get_width()
    ImageHeight = Images[i].get_height()
    print("Image is "+str(ImageWidth) +" x "+str(ImageHeight))
    if ImageWidth > 2040 or ImageHeight > 2040:
     if   i == 1:
      print("Ouch your "+str(i)+"st Image is too big , minimum size is (2040 x 2040), the width and/or height of your image exceeds this")
     elif i == 2:
      print("Ouch your "+str(i)+"nd Image is too big , minimum size is (2040 x 2040), the width and/or height of your image exceeds this")
     elif i == 3:
      print("Ouch your "+str(i)+"rd Image is too big , minimum size is (2040 x 2040), the width and/or height of your image exceeds this")
     else:
      print("Ouch your "+str(i)+"th Image is too big , minimum size is (2040 x 2040), the width and/or height of your image exceeds this")
     sys.exit() 
    for y in range(ImageHeight):
     for x in range(ImageWidth):
      position = (x,y)
      Color = Images[i].get_at(position)
      XYIMMRange("x",x)
      XYIMMRange("y",y)
      out.write(bytes([0x18,0x00,0x0A,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # setX
      out.write(bytes([0x18,0x01,0x0B,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # setY
      out.write(bytes([0x18,0x02,0x00,int(ToHex(Color[0],True),16),int(ToHex(Color[1],True),16),int(ToHex(Color[2],True),16),int(ToHex(Color[3],True),16),0x00,0x00,0x00,0x00])) # SETRGB
      out.write(bytes([0x18,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # Plot
    out.write(bytes([0x18,0x05,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # Update
    print("Done!")
    sys.exit()     
  elif type == ".py":
   print("")
   
else:
 print("invalid arguments expected: ImageToROM.py <Inputfile>")
 sys.exit()
 