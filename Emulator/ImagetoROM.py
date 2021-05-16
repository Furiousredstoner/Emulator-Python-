import os,sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
#Main Code
type = "" # placeholder
Images = [] # images go here

def SetXY(x,y):
####[x-value]#############
 if x <= 255:
  xHex = [x,0,0,0]
 elif x > 255 and x <= 510:
  xHex = [255,(x-255),0,0]
 elif x > 510 and x <= 765:
  xHex = [255,255,(x-510),0]
 elif x > 765 and x <= 1020:
  xHex = [255,255,255,(x-765)]
####[y-value]############## 
 if y <= 255:
  yHex = [y,0,0]
 elif y > 255 and y <= 510:
  yHex = [255,(y-255),0]
 elif y > 510 and y <= 765:
  yHex = [255,255,(y-510)]
####[Output]###############
 out.write(bytes([0x18,0x00,0x00,0x00]+xHex+yHex)) # DVCSND SETXY


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
    if ImageWidth > 1020 or ImageHeight > 765:
     if   i == 0:
      print("Ouch your "+str(i+1)+"st Image is too big , maximum size is (1020 x 765), the width and/or height of your image exceeds this")
     elif i == 1:
      print("Ouch your "+str(i+1)+"nd Image is too big , maximum size is (1020 x 765), the width and/or height of your image exceeds this")
     elif i == 2:
      print("Ouch your "+str(i+1)+"rd Image is too big , maximum size is (1020 x 765), the width and/or height of your image exceeds this")
     else:
      print("Ouch your "+str(i+1)+"th Image is too big , maximum size is (1020 x 765), the width and/or height of your image exceeds this")
     sys.exit() 
    for y in range(ImageHeight):
     for x in range(ImageWidth):
      position = (x,y)
      Color = Images[i].get_at(position)
      SetXY(x,y) # SETXY
      out.write(bytes([0x18,0x00,0x00,0x02,Color[0],Color[1],Color[2],Color[3],0x00,0x00,0x00])) # SETRGB
      out.write(bytes([0x18,0x00,0x00,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # Plot
    out.write(bytes([0x18,0x00,0x00,0x05,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # Plot
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
    if ImageWidth > 1020 or ImageHeight > 765:
     if   i == 1:
      print("Ouch your "+str(i)+"st Image is too big , maximum size is (1020 x 765), the width and/or height of your image exceeds this")
     elif i == 2:
      print("Ouch your "+str(i)+"nd Image is too big , maximum size is (1020 x 765), the width and/or height of your image exceeds this")
     elif i == 3:
      print("Ouch your "+str(i)+"rd Image is too big , maximum size is (1020 x 765), the width and/or height of your image exceeds this")
     else:
      print("Ouch your "+str(i)+"th Image is too big , maximum size is (1020 x 765), the width and/or height of your image exceeds this")
     sys.exit() 
    for y in range(ImageHeight):
     for x in range(ImageWidth):
      position = (x,y)
      Color = Images[i].get_at(position)
      SetXY(x,y) # SETXY
      out.write(bytes([0x18,0x00,0x00,0x02,Color[0],Color[1],Color[2],Color[3],0x00,0x00,0x00])) # SETRGB
      out.write(bytes([0x18,0x00,0x00,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # Plot
    out.write(bytes([0x18,0x00,0x00,0x05,0x00,0x00,0x00,0x00,0x00,0x00,0x00])) # Plot
    print("Done!")
    sys.exit()     
  elif type == ".py":
   print("")
   
else:
 print("invalid arguments expected: ImageToROM.py <Inputfile>")
 sys.exit()
 