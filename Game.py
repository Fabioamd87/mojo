"""Welcome to mojo, music by Frozen Silence, Electric Zoom, Bang Bong """

import sys
import os
import pygame
import string

#import pygame.gfxdraw

import Functions
import Render
import Scenario
import Menu


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
    pointer = Pointer()
    pointergroup = pygame.sprite.RenderPlain(pointer)
    
    #per adesso pointer lo identifico con pointergroup.sprites[0]
    Menu.run(screen,pointergroup)
    
def run(screen,pointergroup):
    
    t = Character('player',150,50,1)
    #s = Tizio('spank',100,60,1,"spank")
    
    scenario = Scenario.Scenario()
    
    
    scenario.load(0)
    t.walkto((300,100))

    #loop principale
    while True:
        for event in pygame.event.get():
            
            #gestione uscita
            if event.type == (pygame.QUIT):
                print "fine"
                sys.exit()
            if event.type == (pygame.KEYDOWN):
                if pygame.key.get_pressed()[27]:
                    print "fine"
                    sys.exit()
            
            #gestione movimento
            if pygame.mouse.get_pressed()==(1,0,0): #click sinistro del mouse
                t.walkto(pygame.mouse.get_pos())
                """se clicchiamo su un'area di transisione
                    tizio dovrebbe avere come proprieta' di destinazione
                    la locazione affine e quando collide con quest'area cambiare scenario"""
                
            #gestione oggetti
            if pygame.mouse.get_pressed()==(0,0,1):
                scenario.OpenActionMenu(pointergroup)
                
            if event.type == pygame.MOUSEBUTTONUP:
                scenario.OnClickReleased()

        scenario.Update(pointergroup,t)
        t.update()
        Render.render(screen,t,scenario,pointergroup)
    return 0
        
def carica_imm_sprite(imagetype,filename,h,w,num):
	immagini = []
	if num is None or num == 1:
		imm1 =  Functions.load_image(imagetype,filename+".png")
		imm1_w, imm1_h = imm1.get_size()
	
		for y in range(int(imm1_h/h)):
			for x in range(int(imm1_w/w)):
				immagini.append(imm1.subsurface((x*w,y*h,w,h)))
	
		return immagini
	else:
		for x in range(1,num):
			imm1 = pygame.image.load(filename+str(x)+".png").convert_alpha()
			immagini.append(imm1)
		return immagini
        
class Character(pygame.sprite.Sprite):
    def __init__(self,filename,altezza,larghezza, num,name="tizio"):
        pygame.sprite.Sprite.__init__(self)
        
        self.name = name
        #definire colore del proprio testo
        self.immagini = carica_imm_sprite('character',filename,altezza,larghezza,num)
        self.image = self.immagini[0]
        
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 250)
        
        self.maxframe = len(self.immagini)

        self.frame_corrente = 0        
        self.width=50
        self.height=150
        
        self.is_moving = False
        self.x_direction = 200
        
        self.time = 0
        
    def collide(self, sprite):
        if self.rect.colliderect(sprite.rect):
            print "collidono"
            return true
            
    def position(self,x,y):
        self.rect.topleft = (x, y)
        self.x_direction = x
        self.is_moving = False
        print self.rect.topleft
        
    def update(self):
        self.time += 1
        if self.time >8:
            if self.is_moving:
                if (self.rect[0]+self.width/2)<self.x_direction:
                    self.is_moving = True
                    self.movedx()

                if (self.rect[0]+self.width/2)>self.x_direction:
                    self.is_moving = True
                    self.movesx()        
            else:
                self.is_moving = False
            self.time = 0
            
    def movedx(self):
        #attualmente il numero massimo di frame e' specificato manualmente        
        if self.frame_corrente < 2:
            self.frame_corrente += 1
            self.image=self.immagini[self.frame_corrente]
        else:
            self.frame_corrente = 0
            self.image=self.immagini[self.frame_corrente]
        self.rect = self.rect.move(10, 0)
        
        if abs(self.x_direction - (self.rect[0]+self.width/2)) < 10:
            print "prissimi"
            print (self.rect[0]+self.width/2),self.x_direction
            self.turn_right()
            self.is_moving=False
        #pygame.time.delay(100)
        
    def movesx(self):
            #attualmente il numero massimo di frame e' specificato manualmente
            if self.frame_corrente < 5:
                self.frame_corrente += 1
                self.image=self.immagini[self.frame_corrente]
            else:
                self.frame_corrente = 3
                self.image=self.immagini[self.frame_corrente]
                
            self.rect = self.rect.move(-10, 0)
            
            if abs(self.x_direction - (self.rect[0]+self.width/2)) < 10:
                print "prissimi"
                self.is_moving=False
                self.turn_left()
            #pygame.time.delay(100)
    
    def walkto(self,direction):
        if self.x_direction != direction[0]:
            print "aggiorno la direzione"
            self.is_moving=True
            self.x_direction = direction[0]
            
    def turn_right(self):
        """volta a destra"""
        self.image=self.immagini[1] #il frame che guarda a destra
    
    def turn_left(self):
        """volta a sinistra"""
        self.image=self.immagini[5] #il frame che guarda a sinistra
   
    def say(self,text):
        """say e' una specie di self.render solo che aspetta un po'
        e il testo non viene salvato"""
        self.text1 = self.font.render(text, 1, (10, 10, 10))
        pygame.time.delay(1000)

class Pointer(pygame.sprite.Sprite):
    """puntatore del mouse grafico"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = Functions.load_image('pointer','pointer.png', -1)

    def update(self):                                          
        self.rect.midtop = pygame.mouse.get_pos()
        
if __name__ == '__main__':
	main()
