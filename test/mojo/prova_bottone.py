import pygame
import sys

import Widgets


# global constants
FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples
FRAMERATE = 30 # how often to check if playback has finished

pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)

screen = pygame.display.set_mode((1024, 480))

interface = Widgets.Interface()
bott = Widgets.Button('prova')
bott.assign(exit)
interface.add(bott)

bottoni = pygame.sprite.Group()
bottoni.add(bott)

def exit():
    sys.exit()

#bott.assign('clicked',exit)

while True:
    pygame.event.get()
    interface.update()
    bottoni.draw(screen)
    pygame.display.update()