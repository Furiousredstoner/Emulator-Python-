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
 GPU.WIDTH, GPU.HEIGHT = 1920, 1080
 GPU.DIM = (GPU.WIDTH, GPU.HEIGHT)
 GPU.Screen = pygame.display.set_mode(GPU.DIM,pygame.RESIZABLE)
 GPU.Surface = pygame.Surface(GPU.DIM)
 pygame.display.flip() 
 GPU.PixelBuffer = pygame.PixelArray(GPU.Surface)
 GPU.X = 0
 GPU.Y = 0
 GPU.Update = False
 GPU.Clock = pygame.time.Clock()
 
def GPU_DVCSND(Inst,Data1,Data2,Data3,Data4,Data5,Data6,Data7,Data8,Data9):
 if   Inst == 0x00: #SetX
  GPU.X = Data1
 elif Inst == 0x01: #SetY
  GPU.Y = Data1
 elif Inst == 0x02: #SetRGB
  GPU.R,GPU.G,GPU.B,GPU.A = Data2,Data3,Data4,Data5
 elif Inst == 0x04: #Plot
  GPU.PixelBuffer[GPU.X, GPU.Y] = (GPU.R,GPU.G,GPU.B,GPU.A)
  GPU.Update = True # Pixel by pixel Rendering
 elif Inst == 0x05: #Update
  print("Plot Data done Rendering to screen")
  GPU.Update = True 
  
def Render(Object):
 screen = pygame.display.get_surface()
 screen.fill((255,255,255))
 screen.blit(Object,(0,0))
 pygame.display.flip()
 
def GPU_tick():
 GPU.Clock.tick()
 print(GPU.Clock.get_fps())
 pygame.event.get()
 if GPU.Update:
  GPU.Update = False
  del GPU.PixelBuffer
  Render(GPU.Surface)
  GPU.PixelBuffer = pygame.PixelArray(GPU.Surface)
