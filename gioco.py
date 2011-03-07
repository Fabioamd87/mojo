import pygame
import pygame.gfxdraw
import sys
import math

def main():
    screen = pygame.display.set_mode((1024, 480))
    #player = pygame.image.load('player.gif').convert_alpha()
    background = Background()
    #mojo = Human(screen,player,background.image)
    textbox = TextOnScreen(screen)

    
    #tizio = Scheletro(screen,background.image)
    t=tizio2("img",150,50,screen,1,background)
    """
    mixer.init(11025)
    sound = mixer.Sound('music.mp3')
    channel = sound.play()
    """
    movimento = pygame.sprite.Group()
        
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                print "fine"
                sys.exit()
            if pygame.mouse.get_pressed()==(1,0,0):
                t.walkto(pygame.mouse.get_pos())
        screen.blit(background.image,(0,0))
        t.render()
        pygame.display.update()
       
    print "fine loop"
    return 0
    
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
        
class tizio2(pygame.sprite.Sprite):
    def __init__(self,nome,altezza,larghezza,screen, num, background):
        pygame.sprite.Sprite.__init__(self)
        self.immagini = carica_imm_sprite(nome,altezza,larghezza,num)
        self.immagine = self.immagini[0]
        self.pos = self.immagine.get_rect()
        self.pos = self.pos.move(200, 250)
        self.maxframe = len(self.immagini)
        self.screen = screen
        self.background = background
        self.frame_corrente = 0
        self.tempo_anim = 0.0
        
        self.width=50
        self.height=150
        
    def render(self):
        self.screen.blit(self.background.image,(0,0))
        self.screen.blit(self.immagine, self.pos)
        pygame.display.update()
    
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
        
        
class Scheletro:
    busto=60
    braccio=30
    gamba=30
    
    def __init__(self,screen,background):
        self.head=35
        self.pos=pygame.Rect(300, 100, 0, 0) # dove piazzare la testa (punto riferimento)
        self.bdx_deg=20
        self.bsx_deg=20
        self.gdx_deg=20
        self.gsx_deg=20
        
        self.i=0
        self.j=0
        
        self.screen = screen
        self.background = background
        
        #creo le superfici
        self.corpo = pygame.Surface((10, self.busto),pygame.SRCALPHA)
        self.gambasx = pygame.Surface((2, self.gamba),pygame.SRCALPHA)
        self.gambadx = pygame.Surface((8, self.gamba),pygame.SRCALPHA)
        self.bracciosx = pygame.Surface((2, self.braccio),pygame.SRCALPHA)
        self.bracciodx = pygame.Surface((8, self.braccio),pygame.SRCALPHA)
        self.testa = pygame.Surface((self.head, self.head),pygame.SRCALPHA)
        
        self.disegna()
        
    def disegna(self):
        
        #disegno i pezzi
        pygame.gfxdraw.aacircle(self.testa, self.head/2, self.head/2, self.head/2, (0, 0, 0))
        pygame.gfxdraw.rectangle(self.corpo,self.corpo.get_rect(),(0,0,0))
        pygame.gfxdraw.rectangle(self.gambadx,self.gambadx.get_rect(),(0,255,0))
        pygame.gfxdraw.vline(self.gambasx,0,0,self.busto,(0,255,0))
        pygame.gfxdraw.rectangle(self.bracciodx,self.bracciodx.get_rect(),(0,0,0))
        pygame.gfxdraw.vline(self.bracciosx,0,0,self.braccio,(255,0,0))
        
        #posiziono le superfici la prima volta
        self.corpo_pos=self.pos.move(self.head/2,self.head)
        self.bracciodx_pos=self.pos.move(self.head/2,self.head)
        self.bracciosx_pos=self.pos.move(self.head/2,self.head)
        self.gambadx_pos=self.pos.move(self.head/2,self.head+self.busto)
        self.gambasx_pos=self.pos.move(self.head/2,self.head+self.busto)
           
    def movedx(self):
        self.pos = self.pos.move(10, 0)

        #ruoto i pezzi in posizione di default
        self.gambadx = pygame.transform.rotate(self.gambadx, self.i)
        self.gambasx = pygame.transform.rotate(self.gambasx, self.j)
        self.bracciodx = pygame.transform.rotate(self.bracciodx, self.i)
        self.bracciosx = pygame.transform.rotate(self.bracciosx, self.j)
        
        self.corpo_pos=self.pos.move(self.head/2,self.head)
        self.bracciodx_pos=self.pos.move(self.head/2,self.head)
        self.bracciosx_pos=self.pos.move(self.head/2,self.head)
        self.gambadx_pos = self.pos.move(self.head/2,self.head+self.busto)
        self.gambasx_pos = self.pos.move(self.head/2,self.head+self.busto)
        
        self.gambasx_pos = self.offset_rotazione(self.gambasx_pos,self.i)
        self.bracciosx_pos = self.offset_rotazione(self.bracciosx_pos,self.i)      
        pygame.time.delay(1000)
        
    def movesx(self):
        null
        
    def offset_rotazione(self,pos,gradi):
        #(matematica)
        raggio=self.gambasx.get_height()
        singrad=math.degrees(math.sin(math.radians(gradi)))
        offsetx=(singrad*raggio)
        cosgrad=math.degrees(math.cos(math.radians(gradi)))
        offsety = self.braccio-(cosgrad*raggio)
        print self.braccio
        print math.cos(gradi)*raggio
        pos = pos.move(-offsetx,-offsety)
        return pos
        
    def blit(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.testa, self.pos)
        self.screen.blit(self.corpo,self.corpo_pos)
        self.screen.blit(self.bracciodx, self.bracciodx_pos)
        self.screen.blit(self.bracciosx, self.bracciosx_pos)
        self.screen.blit(self.gambadx, self.gambadx_pos)
        self.screen.blit(self.gambasx, self.gambasx_pos)    

class Background:
    def __init__(self):
        self.image = pygame.image.load('background1.jpg').convert()        
    
class TextOnScreen:
    """per adesso ci sono solo 3 righe di testo fisse, in futuro dovrebbe essere scorribile
    con la (tastiera freccia su e giu)
    """
    def __init__(self,screen):
        if pygame.font:
            pygame.font.init()
            font = pygame.font.Font(None, 36)
            self.text1 = font.render("Ciao, sono mojo jojo", 1, (10, 10, 10))
        
	
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
                      
if __name__ == '__main__':
	main()
