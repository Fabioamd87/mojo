import pygame
import pygame.gfxdraw
import sys
import math

def main():
    screen = pygame.display.set_mode((1024, 480))
    b = Background()
    
    textbox = TextOnScreen(screen,b)
    t = Tizio("img",150,50,screen,1,b)

    movimento = pygame.sprite.Group()
    
    #animazione iniziale
    t.walkto((300,250))
    t.say("mmm...")
    t.say("quel bar sembra invitante...")
    
    #loop principale
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                print "fine"
                sys.exit()
            if pygame.mouse.get_pressed()==(1,0,0):
                click_pos=pygame.mouse.get_pos()
                t.walkto(click_pos)
                if t.pos.colliderect(b.porta):
                    print "collidono"
                    b.load_scene("bar")
                    t.position(100,250)
                    
        screen.blit(b.image,(0,0))
        t.render()
        pygame.display.update()
    return 0

class Background:
    def __init__(self):
        self.image = pygame.image.load('background1.jpg').convert()        
        self.porta = pygame.Rect(732,245,100,100)
    def load_scene(self,scene):
        self.image = pygame.image.load(scene+'.jpg').convert()
        
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
        
        self.immagini = carica_imm_sprite(nome,altezza,larghezza,num)
        self.immagine = self.immagini[0]
        self.pos = self.immagine.get_rect()
        self.pos = self.pos.move(200, 250)
        self.rect = self.pos #per il controllo collide
        self.maxframe = len(self.immagini)
        self.screen = screen
        self.background = background
        self.frame_corrente = 0        
        self.width=50
        self.height=150
        
        if pygame.font:
            pygame.font.init()
            self.font = pygame.font.Font(None, 36)
            self.text1 = self.font.render("", 1, (10, 10, 10))
        
    def render(self):
        self.screen.blit(self.background.image,(0,0))
        self.screen.blit(self.immagine, self.pos)
        pygame.display.update()
    
    def collide(self, sprite):
        if self.rect.colliderect(sprite.rect):
            print "collidono"
            return true
    def position(self,x,y):
        self.pos.topleft = (x, y)
        print self.pos.topleft
    
    def movedx(self):
        #attualmente il numero massimo di frame e' specificato manualmente
        self.pos = self.pos.move(10, 0)
        
        if self.frame_corrente < 2:
            self.frame_corrente += 1
            self.immagine=self.immagini[self.frame_corrente]
        else:
            self.frame_corrente = 0
            self.immagine=self.immagini[self.frame_corrente]
                            
        self.render()
        pygame.time.delay(100)
    
    def movesx(self):
        #attualmente il numero massimo di frame e' specificato manualmente
        self.pos = self.pos.move(-10, 0)
        
        if self.frame_corrente < 5:
            self.frame_corrente += 1
            self.immagine=self.immagini[self.frame_corrente]
        else:
            self.frame_corrente = 3
            self.immagine=self.immagini[self.frame_corrente]
                            
        self.render()
        pygame.time.delay(100)
        
    def walkto(self, pos):
        print pos[0]
        if self.pos[0]<pos[0]:
            print "move to dx"
            while (self.pos[0]+self.width/2)<pos[0]:
                self.movedx()

        else:
            print "move to sx"
            while (self.pos[0]+self.width/2)>pos[0]:
                self.movesx()
    def say(self,text):
        """say e' una specie di self.render solo che aspetta un po'
        e il testo non viene salvato"""
        self.text1 = self.font.render(text, 1, (10, 10, 10))
        self.screen.blit(self.background.image,(0,0))
        self.screen.blit(self.immagine, self.pos)
        self.screen.blit(self.text1,(0,0))
        pygame.display.update()
        pygame.time.delay(1000)
        
class TextOnScreen:
    """per adesso ci sono solo 3 righe di testo fisse, in futuro dovrebbe essere scorribile
    con la (tastiera freccia su e giu)
    """
    def __init__(self,screen,background):
        self.screen=screen
        self.background=background
        if pygame.font:
            pygame.font.init()
            self.font = pygame.font.Font(None, 36)
    def write(self,text1):
            self.text1 = self.font.render(text1, 1, (10, 10, 10))
        
"""
class Human:
    def __init__(self,screen,image,background):
        self.image = image
        self.screen = screen
        self.background = background
        self.pos = image.get_rect()
        self.width = image.get_width()
        self.height = image.get_height()
        
    def movedx(self):
        self.pos = self.pos.move(2, 0)
    def movesx(self):
        self.pos = self.pos.move(-2, 0)
    def walkto(self, pos):
        print pos[0]
        if self.pos[0]<pos[0]:
            print "move to dx"
            while (self.pos[0]+self.width/2)<pos[0]:
                self.movedx()
                self.screen.blit(self.background, self.pos, self.pos)
                self.screen.blit(self.image, self.pos)
                pygame.display.update()
        else:
            print "move to sx"
            while (self.pos[0]+self.width/2)>pos[0]:
                self.movesx()
                self.screen.blit(self.background, self.pos, self.pos)
                self.screen.blit(self.image, self.pos)
                pygame.display.update()
                
class Box(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):

        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
      
        # Create the image that will be displayed and fill it with the
        # right color.
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
"""                      
if __name__ == '__main__':
	main()
