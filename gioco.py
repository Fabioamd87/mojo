import pygame
import pygame.gfxdraw
import sys
import math
import pygame.mixer, pygame.time
import functions

import Actions

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

"""
nomi delle destinazioni:
    intro
    bar
    
"""

def main():
    screen = pygame.display.set_mode((1024, 480))
    pygame.mouse.set_visible(False)
    
    b = Background(screen)
    textbox = TextOnScreen(screen,b)
    t = Tizio('img',150,50,screen,1,b)
    s = Tizio('spank',100,60,screen,1,b)
    s.name = "spank"
    
    movimento = pygame.sprite.Group()
        
    pointer=Pointer()
    pointergroup = pygame.sprite.RenderPlain(pointer)
    
    #animazione iniziale
    Actions.walk(t,(300,250),b,s)
    #talk("mmm...")
    #t.say("quel bar sembra invitante...")
    
    #quando parla non blitta spank
    birra=Object("birra",(450,250))
    porta=Rect("porta",(732,245,100,100),"bar")
    
    oggetti_primo_livello=pygame.sprite.Group()
    oggetti_bar=pygame.sprite.Group()
    
    rect_primo_livello=pygame.sprite.Group()
    rect_primo_livello.add(porta)
    
    oggetti_primo_livello.add(s)
    oggetti_bar.add(birra)
    
    oggetti_livello_attuale=oggetti_primo_livello
    rect_livello_attuale=rect_primo_livello
    print rect_livello_attuale
    
    #loop principale
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN): # qualsiasi tasto premuto
                print "fine"
                sys.exit()
            if pygame.mouse.get_pressed()==(1,0,0): #click del mouse
                Actions.walk(t,pygame.mouse.get_pos(),b,s)
                
            if collide(t,rect_livello_attuale): # tizio collide con una rect del livello
                b.load_scene(collide(t,rect_livello_attuale).destination)
                t.position(100,250)
                    
            if collide(pointer,oggetti_livello_attuale):
                print collide(pointer,oggetti_livello_attuale).name
        
        b.render()
        s.render()
        t.render()
        pointergroup.update()
        pointergroup.draw(screen)
        pygame.display.update()
    return 0
    
class Pointer(pygame.sprite.Sprite):
    """puntatore del mouse grafico"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = functions.load_image('pointer.png', -1)         #carico l'immagine del puntatore

    def update(self):
        pos = pygame.mouse.get_pos()                                            #muove il puntatore in base al mouse
        self.rect.midtop = pos

def Bar(b,t):
    b.load_scene("bar")
    t.position(100,250)
    
def collide(obj, objects):
    if pygame.sprite.spritecollide(obj,objects,0) != []:
        return pygame.sprite.spritecollide(obj,objects,0)[0] #ritorna uno sprite, forse.
    else:
        return False
     
def mouse_collide_with(rect):
    #riferiment rect: pygame.Rect(left, top, width, height): return Rect
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0]>rect[0] and mouse_pos[0]<rect[0]+rect[2]: #raffinare
        if mouse_pos[1]>rect[1] and mouse_pos[1]<rect[1]+rect[3]:
            return True
                
class Object(pygame.sprite.Sprite):
    def __init__(self,name,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('beer.png').convert()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move
        self.name = name

class Rect(pygame.sprite.Sprite): #dovrebbe indicare anche dove porta
    def __init__(self,name,rect,dest):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)
        self.name = name
        self.destination=dest
                    
class Background():
    def __init__(self,screen):
        self.image = pygame.image.load('background1.jpg').convert()
        self.screen = screen
    def load_scene(self,scene):
        self.image = pygame.image.load(scene+'.jpg').convert()
    def render(self):
        self.screen.blit(self.image,(0,0))
        
def carica_imm_sprite(nome,h,w,num):
	immagini = []
	if num is None or num == 1:
		imm1 =  pygame.image.load(nome+".png").convert_alpha()
		imm1_w, imm1_h = imm1.get_size()
	
		for y in range(int(imm1_h/h)):
			for x in range(int(imm1_w/w)):
				immagini.append(imm1.subsurface((x*w,y*h,w,h)))
	
		return immagini
	else:
		for x in range(1,num):
			imm1 = pygame.image.load(nome+str(x)+".png").convert_alpha()
			immagini.append(imm1)
		return immagini
        
class Tizio(pygame.sprite.Sprite):
    def __init__(self,nome,altezza,larghezza,screen, num, background):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.background = background
        self.name = "" #nome dell'essere
        #definire colore del proprio testo
        self.immagini = carica_imm_sprite(nome,altezza,larghezza,num)
        self.immagine = self.immagini[0]
        self.rect = self.immagine.get_rect()
        self.rect = self.rect.move(200, 250)
        self.maxframe = len(self.immagini)

        self.frame_corrente = 0        
        self.width=50
        self.height=150
        
        if pygame.font:
            pygame.font.init()
            self.font = pygame.font.Font(None, 36)
            self.text1 = self.font.render("", 1, (10, 10, 10))
        
    def render(self):
        self.screen.blit(self.immagine, self.rect)
        
    def render_move(self):
        #self.screen.blit(self.background.image,(0,0))
        self.screen.blit(self.immagine, self.rect)
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
            self.immagine=self.immagini[self.frame_corrente]
        else:
            self.frame_corrente = 0
            self.immagine=self.immagini[self.frame_corrente]
        
        pygame.time.delay(100)
        
    
    def movesx(self):
        #attualmente il numero massimo di frame e' specificato manualmente
        self.rect = self.rect.move(-10, 0)
        
        if self.frame_corrente < 5:
            self.frame_corrente += 1
            self.immagine=self.immagini[self.frame_corrente]
        else:
            self.frame_corrente = 3
            self.immagine=self.immagini[self.frame_corrente]
        
        pygame.time.delay(100)
        
        
    def walkto(self, pos):
        print pos[0]
        if self.rect[0]<pos[0]:
            print "move to dx"
            while (self.rect[0]+self.width/2)<pos[0]:
                self.movedx()
        else:
            print "move to sx"
            while (self.rect[0]+self.width/2)>pos[0]:
                self.movesx()

    def say(self,text):
        """say e' una specie di self.render solo che aspetta un po'
        e il testo non viene salvato"""
        self.text1 = self.font.render(text, 1, (10, 10, 10))
        self.screen.blit(self.background.image,(0,0)) #eventualmente togliere
        self.screen.blit(self.immagine, self.pos) #eventualmente togliere
        self.screen.blit(self.text1,(0,0))
        pygame.display.update() #eventualmente togliere
        pygame.time.delay(1000)
        
class TextOnScreen:
    """per adesso ci sono solo 3 righe di testo fisse, in futuro dovrebbe essere scorribile
    con la (tastiera freccia su e giu)
    """
    def __init__(self,screen,background):
        self.screen=screen
        self.background=background
        self.pos = (512,0)
        if pygame.font:
            pygame.font.init()
            self.font = pygame.font.Font(None, 36)
        self.text1 = self.font.render("", 1, (10, 10, 10))
    def write(self,text1):
        self.text1 = self.font.render(text1, 1, (10, 10, 10))
    def render(self):
        self.screen.blit(self.text1, self.pos)
                            
if __name__ == '__main__':
	main()
