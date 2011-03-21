"""Welcome to mojo, music by Electric Zoom, Bang Bong """

import pygame
import pygame.gfxdraw
import sys
import math
import pygame.mixer, pygame.time

import Functions
import Render
import Actions

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

pygame.font.init()

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
    # initialize pygame.mixer module
    # if these setting do not work with your audio system
    # change the global constants accordingly
    try:
        pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
    except pygame.error, exc:
        print >>sys.stderr, "Could not initialize sound system: %s" % exc
        return 1
        
    run_game()
    
def run_game():
  
    playmusic('intro.ogg')
    
        
    screen = pygame.display.set_mode((1024, 480))
    pygame.mouse.set_visible(False)
    b = Background(screen)
    textbox = TextOnScreen()
    actions = ActionsBox()
    t = Tizio('img',150,50,screen,1,b)
    s = Tizio('spank',100,60,screen,1,b,"spank")
    
    movimento = pygame.sprite.Group()
    interazioni = pygame.sprite.Group()
    
    #creo il puntatore    
    pointer=Pointer()
    pointergroup = pygame.sprite.RenderPlain(pointer)
    
    text_in_game=pygame.sprite.Group()

    #creo gli oggetti del livello
    
    #primo livello
    porta=Rect("porta",(732,245,100,100),"bar")
    oggetti_primo_livello=pygame.sprite.Group()
    oggetti_primo_livello.add(s)
    
    rect_primo_livello=pygame.sprite.Group()
    rect_primo_livello.add(porta)
    
    #oggetti del bar
    birra=Object("birra",(450,250))
    oggetti_bar=pygame.sprite.Group()
    oggetti_bar.add(birra)
    
    #oggetti e rect scenario attuale
    oggetti_livello_attuale=oggetti_primo_livello
    rect_livello_attuale=rect_primo_livello
    
    #animazione iniziale
    Actions.walk(b,t,screen,(300,250),oggetti_livello_attuale)
    #talk("mmm...")
    #t.say("quel bar sembra invitante...")
    
    #loop principale
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN): # qualsiasi tasto premuto
                print "fine"
                sys.exit()
            if pygame.mouse.get_pressed()==(1,0,0): #click sinistro del mouse
                Actions.walk(b,t,screen,pygame.mouse.get_pos(),oggetti_livello_attuale)
                #text_in_game.empty() #dirty hack, non deve cancellare qui, non c'entra niente
            
            actions.calcola_posizione_box()
            if pygame.mouse.get_pressed()==(0,0,1) and collide(pointer,oggetti_livello_attuale):
                #obj=collide(pointer,oggetti_livello_attuale)
                #actions.calcola_posizione_box()
                actions.moveable=False
                text_in_game.add(actions.e,actions.p,actions.t) # dovrebbero esserci finche' si tiene il mouse premuto
                actions.select(pointer)
            else:
                text_in_game.remove(actions.e,actions.p,actions.t)
                
            if collide(pointer,text_in_game):
                act = collide(pointer,text_in_game)
                
            if collide(t,rect_livello_attuale): # tizio collide con una rect del livello
                where=collide(t,rect_livello_attuale)
                b.load_scene(where.destination)
                playmusic('bar.ogg')
                t.position(100,250)
                oggetti_livello_attuale=oggetti_bar

            if textbox.pointer_collide(pointer,oggetti_livello_attuale,rect_livello_attuale):
                text_in_game.add(textbox)
            else:
                text_in_game.remove(textbox)
        
        Render.render(screen,b,t,oggetti_livello_attuale,text_in_game,pointergroup)
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

def Bar(b,t):
    b.load_scene("bar")
    t.position(100,250)
    
def collide(obj, objects):
    sprite=pygame.sprite.spritecollideany(obj,objects)
    if sprite:
        return sprite #ritorna uno sprite, forse.
    else:
        return False
     
class Object(pygame.sprite.Sprite):
    def __init__(self,name,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('beer.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft=pos
        self.name = name

class Rect(pygame.sprite.Sprite): #dovrebbe indicare anche dove porta
    def __init__(self,name,rect,dest):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)
        self.name = name
        self.destination=dest
                    
class Background(pygame.sprite.Sprite):
    def __init__(self,screen):
        self.image = pygame.image.load('background1.jpg').convert()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 0, 0)
    def load_scene(self,scene):
        self.image = pygame.image.load(scene+'.jpg').convert()
        
class Scenario(pygame.sprite.Sprite):
    def __init__(self,screen):
        self.image = pygame.image.load('background1.jpg').convert()
        self.screen = screen
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
    def __init__(self,filename,altezza,larghezza,screen, num, background,name="tizio"):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.background = background
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
        print self.rect.topleft
    
    def movedx(self):
        #attualmente il numero massimo di frame e' specificato manualmente
        self.rect = self.rect.move(10, 0)
        
        if self.frame_corrente < 2:
            self.frame_corrente += 1
            self.image=self.immagini[self.frame_corrente]
        else:
            self.frame_corrente = 0
            self.image=self.immagini[self.frame_corrente]
        
        pygame.time.delay(100)
        
    def movesx(self):
        #attualmente il numero massimo di frame e' specificato manualmente
        self.rect = self.rect.move(-10, 0)
        
        if self.frame_corrente < 5:
            self.frame_corrente += 1
            self.image=self.immagini[self.frame_corrente]
        else:
            self.frame_corrente = 3
            self.image=self.immagini[self.frame_corrente]
        
        pygame.time.delay(100)

    def say(self,text):
        """say e' una specie di self.render solo che aspetta un po'
        e il testo non viene salvato"""
        self.text1 = self.font.render(text, 1, (10, 10, 10))
        pygame.time.delay(1000)
        
class TextOnScreen(pygame.sprite.Sprite):
    """riporta i nomi degli oggetti che collidono col puntatore"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(512,0,0,0)
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("", 1, (10, 10, 10))
    def pointer_collide(self,pointer,objects,rects):
        if collide(pointer,objects): #collide con un oggetto
            obj=collide(pointer,objects)
            self.text = self.font.render(obj.name, 1, (10, 10, 10))
            return True
        elif collide(pointer,rects): #collide con una rect
            rect=collide(pointer,rects)
            self.text = self.font.render(rect.name, 1, (10, 10, 10))
            return True            
        else:
            self.text = self.font.render("", 1, (10, 10, 10))
            return False
        
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

class ActionsBox(pygame.sprite.Sprite):
    """esamina, prendi, parla, appare quando facciamo click
    con il pulsante destro su un personaggio o un oggetto"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.moveable = True
        self.e = self.action("esamina")
        self.p = self.action("prendi")
        self.t = self.action("parla")
        
    class action(pygame.sprite.Sprite):
        def __init__(self,name):
            pygame.sprite.Sprite.__init__(self)
            pygame.font.init()
            self.font = pygame.font.Font(None, 36)
            self.rect = pygame.Rect(0, 0, 50, 20)
            self.text = self.font.render(name, 1, (10, 10, 10))
            #pgyame.gfxdraw.rectangle(self.text, self.rect, (10,10,10))
            
    def calcola_posizione_box(self):
        if self.moveable:
            mouse_pos = pygame.mouse.get_pos()
            self.e.rect.topleft=mouse_pos[0],mouse_pos[1]+40
            self.p.rect.topleft=mouse_pos[0]+40,mouse_pos[1]-40
            self.t.rect.topleft=mouse_pos[0]-40,mouse_pos[1]-40
    
    def empty(self):
        self.e = self.action("")
        self.p = self.action("")
        self.t = self.action("")
        
    def select(self,pointer):
        if pygame.sprite.collide_rect(pointer, self.e):
            self.e.text = self.e.font.render("esamina", 1, (10, 255, 10))
        else:
            self.e.text = self.e.font.render("esamina", 1, (10, 10, 10))
        if pygame.sprite.collide_rect(pointer, self.p):
            self.p.text = self.p.font.render("prendi", 1, (10, 255, 10))
        else:
            self.p.text = self.p.font.render("prendi", 1, (10, 10, 10))    
        if pygame.sprite.collide_rect(pointer, self.t):
            self.t.text = self.t.font.render("parla", 1, (10, 255, 10))
        else:
            self.t.text = self.t.font.render("parla", 1, (10, 10, 10))

def playmusic(soundfile):
    """Stream music with mixer.music module in blocking manner.
    
    This will stream the sound from disk while playing.
    """

    clock = pygame.time.Clock()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy():
     #   clock.tick(FRAMERATE)
        
if __name__ == '__main__':
	main()
