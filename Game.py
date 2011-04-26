"""Welcome to mojo, music by Frozen Silence, Electric Zoom, Bang Bong """

import sys
import os
import string
import pygame #avvertire di installare python-pygame

#import pygame.gfxdraw

import Functions
import Render
import Scenario
import Menu
import Character
import GameElements

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

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
    except pygame.error, exc:
        print >>sys.stderr, "Could not initialize sound system: %s" % exc
        return 1
        
    screen = pygame.display.set_mode((1024, 480))
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('A Dying Flowers')
    
    
    #separare pointer come singolo file/oggetto?
    pointer = GameElements.Pointer()
    pointergroup = pygame.sprite.RenderPlain(pointer)
    
    #per adesso pointer lo identifico con pointergroup.sprites[0]
    Menu.run(screen,pointergroup)
    
def run(screen,pointergroup):
    
    player = Character.Player('player',150,50,1)
    #s = Tizio('spank',100,60,1,"spank")
    
    scenario = Scenario.Scenario()
    
    
    scenario.load(0)
    player.walkto((300,100))
    
    clock = pygame.time.Clock()

    #loop principale
    while True:
        for event in pygame.event.get():
            
            #gestione uscita
            if event.type == (pygame.QUIT):
                print "fine"
                sys.exit()
            if event.type == (pygame.KEYDOWN):
                print event.dict
                if event.dict['key'] == 27:
                    print "fine"
                    sys.exit()
            
            #gestione movimento
            if pygame.mouse.get_pressed()==(1,0,0):
                player.walkto(pygame.mouse.get_pos())
                
            if event.type == pygame.MOUSEBUTTONUP:
                scenario.OnClickReleased(event)

        scenario.Update(pointergroup,player)
        player.Update(clock)
        Render.render(screen,player,scenario,pointergroup)
        clock.tick()
    return 0
        
if __name__ == '__main__':
	main()
