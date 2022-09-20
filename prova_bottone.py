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
b = Widgets.Button('exit',(0,0),pygame.QUIT)
interface.add(b)

bottoni = pygame.sprite.Group()
bottoni.add(b)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    interface.update()
    bottoni.draw(screen)
    pygame.display.update()