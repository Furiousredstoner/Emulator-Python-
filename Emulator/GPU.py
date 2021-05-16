#! /usr/bin/python3
print("GPU Loaded")
from Component import *
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
GPU = Component()

def GPU_init():
 pygame.init()
 pygame.display.set_caption("Emulator")
 GPU.WIDTH, GPU.HEIGHT = 1020, 765
 GPU.DIM = (GPU.WIDTH, GPU.HEIGHT)
 GPU.Screen = pygame.display.set_mode(GPU.DIM)
 GPU.Surface = pygame.Surface(GPU.DIM)
 GPU.PixelBuffer = pygame.PixelArray(GPU.Surface)
 GPU.X = 0
 GPU.Y = 0
 GPU.Update = False
 GPU.Clock = pygame.time.Clock()
 #                  
def GPU_DVCSND(Inst,Data1,Data2,Data3,Data4,Data5,Data6,Data7):
 if   Inst == 0x00: #SetXY
  GPU.X = (Data1+Data2+Data3+Data4)
  GPU.Y = (Data5+Data6+Data7)
 elif Inst == 0x02: #SetRGB
  GPU.R,GPU.G,GPU.B,GPU.A = Data1,Data2,Data3,Data4
 elif Inst == 0x04: #Plot
  GPU.PixelBuffer[GPU.X, GPU.Y] = (GPU.R,GPU.G,GPU.B,GPU.A)
  #print([GPU.X, GPU.Y])
  #GPU.Update = True # Pixel by pixel Rendering
 elif Inst == 0x05: #Update
  print("Plot Data done Rendering to screen")
  GPU.Update = True 
  
def Render(Object):
 screen = pygame.display.get_surface()
 screen.fill((255,255,255))
 screen.blit(Object,(0,0))
 pygame.display.flip()

def GPU_tick():
 pygame.event.get()
 if GPU.Update:
  GPU.Clock.tick()
  #print(GPU.Clock.get_fps())
  GPU.Update = False
  #Render(GPU.Surface)
  Render(GPU.PixelBuffer.make_surface())
  del GPU.PixelBuffer
  GPU.PixelBuffer = pygame.PixelArray(GPU.Surface)
