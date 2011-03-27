"""Welcome to mojo, music by Electric Zoom, Bang Bong """

import sys
import pygame
import string

import pygame.gfxdraw

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

"""
nomi delle destinazioni:
    intro
    bar
    
"""

def main():
    pygame.font.init()
    # initialize pygame.mixer module
    # if these setting do not work with your audio system
    # change the global constants accordingly
    try:
        pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
    except pygame.error, exc:
        print >>sys.stderr, "Could not initialize sound system: %s" % exc
        return 1
    Menu.run()
    
def run(screen):
  
    screen = pygame.display.set_mode((1024, 480))
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('A Dying Flowers')
    
    #b = Background()
    t = Tizio('player',150,50,1)
    s = Tizio('spank',100,60,1,"spank")
    #textbox = TextOnScreen()
    
    scenario = Scenario.Scenario()
    
    #movimento = pygame.sprite.Group()
    interazioni = pygame.sprite.Group()
    
    #creo il puntatore
    pointer=Pointer()
    pointergroup = pygame.sprite.RenderPlain(pointer)
    
    #text_in_game=pygame.sprite.Group()
    #text_in_game.add(textbox,textbox.e,textbox.p,textbox.t)

    #creo gli oggetti del livello
    
    #primo livello
    oggetti_primo_livello=pygame.sprite.Group()
    oggetti_primo_livello.add(s)
    
    rect_primo_livello=pygame.sprite.Group()
    porta=Scenario.Rect("porta",(732,245,100,100),"bar")
    rect_primo_livello.add(porta)
    
    #oggetti del bar
    birra=Scenario.Object("birra",(450,250))
    oggetti_bar=pygame.sprite.Group()
    oggetti_bar.add(birra)
    
    rect_bar=pygame.sprite.Group()
    
    #oggetti e rect scenario attuale
    oggetti_livello_attuale=oggetti_primo_livello
    rect_livello_attuale=rect_primo_livello
    
    #animazione iniziale
    #t.walkto((300,250))
    #t.say("quel bar sembra invitante...")
    
    playmusic('intro.ogg')
    act_mseconds = prev_mseconds = 0
    #loop principale
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN): # qualsiasi tasto premuto
                print "fine"
                sys.exit()
                
            #gestione movimento
            if pygame.mouse.get_pressed()==(1,0,0): #click sinistro del mouse
                t.walkto(pygame.mouse.get_pos())
                
            #gestione oggetti
            scenario.textbox.calcola_posizione_box()
            if pygame.mouse.get_pressed()==(0,0,1):
                scenario.textbox.calcolable = False
                if collide(pointer,oggetti_livello_attuale):
                    scenario.textbox.set_name(collide(pointer,oggetti_livello_attuale))
                    scenario.textbox.show()
                    scenario.textbox.name_settable = False
            else:
                scenario.textbox.hide()
                scenario.textbox.calcolable = True
                scenario.textbox.name_settable = True
            if event.type == pygame.MOUSEBUTTONUP:
                print "rilasciato"
                scenario.textbox.on_click_released()            
            scenario.textbox.select(pointer)
              
            if collide(pointer,scenario.text_in_game):
                act = collide(pointer,scenario.text_in_game)
                
            scenario.textbox.pointer_collide(pointer,oggetti_livello_attuale,rect_livello_attuale)
            
            #gestione cambio scenario: AGGIUSTARE
            if pygame.mouse.get_pressed()==(1,0,0) and collide(t,rect_livello_attuale): # tizio collide con una rect del livello
                where=collide(t,rect_livello_attuale)
                b.load_scene(where.destination)
                playmusic('bar.ogg')
                t.position(100,250)
                t.is_moving = False
                oggetti_livello_attuale = oggetti_bar
                rect_livello_attuale = rect_bar
                
        time = pygame.time.get_ticks()
        t.update(time)
        Render.render(screen,scenario.background,t,oggetti_livello_attuale,scenario.text_in_game,pointergroup)
        pygame.display.update()
    return 0
    
class Pointer(pygame.sprite.Sprite):
    """puntatore del mouse grafico"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = Functions.load_image('pointer.png', -1)         #carico l'immagine del puntatore

    def update(self):
        pos = pygame.mouse.get_pos()                                            #muove il puntatore in base al mouse
        self.rect.midtop = pos

#def Bar(b,t):
#    b.load_scene("bar")
#    t.position(100,250)
    
def collide(obj, objects):
    sprite=pygame.sprite.spritecollideany(obj,objects)
    if sprite:
        return sprite #ritorna uno sprite, forse.
    else:
        return False

class Background(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('background1.jpg').convert()
        self.rect = pygame.Rect(0, 0, 0, 0)
    def load_scene(self,scene):
        self.image = pygame.image.load(scene+'.jpg').convert()
        
def carica_imm_sprite(filename,h,w,num):
	immagini = []
	if num is None or num == 1:
		imm1 =  pygame.image.load(filename+".png").convert_alpha()
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
        
class Tizio(pygame.sprite.Sprite):
    def __init__(self,filename,altezza,larghezza, num,name="tizio"):
        pygame.sprite.Sprite.__init__(self)
        #self.screen = screen
        #self.background = background
        self.name = name
        #definire colore del proprio testo
        self.immagini = carica_imm_sprite(filename,altezza,larghezza,num)
        self.image = self.immagini[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(200, 250)
        self.maxframe = len(self.immagini)

        self.frame_corrente = 0        
        self.width=50
        self.height=150
        
        self.is_moving = False
        self.x_direction = 200
        
        self.font = pygame.font.Font(None, 36)
        self.text1 = self.font.render("", 1, (10, 10, 10))
        
    def render_move(self):
        #self.screen.blit(self.background.image,(0,0))
        self.screen.blit(self.image, self.rect)
        pygame.display.update()
    
    def collide(self, sprite):
        if self.rect.colliderect(sprite.rect):
            print "collidono"
            return true
            
    def position(self,x,y):
        self.rect.topleft = (x, y)
        self.x_direction = x
        self.is_moving = False
        print self.rect.topleft
        
    
    def movedx(self):
        print self.game_time
        #if self.game_time % 10 == 0:
        
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
    
    def update(self,time):
        self.game_time = time
        if self.is_moving:
            print "sto camminando"
            if (self.rect[0]+self.width/2)<self.x_direction:
                self.is_moving = True
                self.movedx()

            if (self.rect[0]+self.width/2)>self.x_direction:
                self.is_moving = True
                self.movesx()        
        else:
            self.is_moving = False
   
    def say(self,text):
        """say e' una specie di self.render solo che aspetta un po'
        e il testo non viene salvato"""
        self.text1 = self.font.render(text, 1, (10, 10, 10))
        pygame.time.delay(1000)
        
class DialogueBox:
    """per adesso ci sono solo 3 righe di testo fisse, in futuro dovrebbe essere scorribile
    con la (tastiera freccia su e giu)
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = (0,300)
        self.font = pygame.font.Font(None, 36)
        #self.text1 = self.font.render("", 1, (10, 10, 10))
    def write(self,text1):
        self.text1 = self.font.render(text1, 1, (10, 10, 10))
            
def playmusic(musicfile): # da includere in scenario
    """Stream music with mixer.music module in blocking manner.
    This will stream the sound from disk while playing.
    """

    clock = pygame.time.Clock()
    pygame.mixer.music.load(musicfile)
    pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy():
    #   clock.tick(FRAMERATE)
        
if __name__ == '__main__':
	main()
