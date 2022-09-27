"""Welcome to mojo, music by Frozen Silence, Electric Zoom, Bang Bong """

import os
import pygame #avvertire di installare python-pygame

#import pygame.gfxdraw

#import Functions
import engine

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

# global constants
FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples
FRAMERATE = 30 # how often to check if playback has finished

os.environ['SDL_VIDEO_CENTERED'] = '1'

def main():
    pygame.font.init()
    try:
        pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
    except pygame.error as exc:
        print("Could not initialize sound system: %s" % exc, file=sys.stderr)
        return 1
    
    #inizializzo la finestra
    screen = pygame.display.set_mode((1024, 480))    
    pygame.display.set_caption('A Dying Flowers')

    eng = engine.Engine(screen)
    eng.run()
 
if __name__ == '__main__':
	main()
