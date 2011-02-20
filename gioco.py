import pygame
import pygame.gfxdraw
import sys
import math

def main():
    mixer = pygame.mixer
    screen = pygame.display.set_mode((1024, 480))
    player = pygame.image.load('player.gif').convert()
    background = Background()
    mojo = Human(screen,player,background.image)
    textbox = TextOnScreen(screen)
    screen.blit(background.image, (0, 0))
    screen.blit(mojo.image, mojo.pos)
    
    tizio = Scheletro()
    
    """
    mixer.init(11025)
    sound = mixer.Sound('music.mp3')
    channel = sound.play()
    """
    
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                print "fine"
                sys.exit()
            #if pygame.mouse.get_pressed()==(1,0,0):
            #   mojo.walkto(pygame.mouse.get_pos())
        screen.blit(textbox.text1, (0,400))
        
        screen.blit(tizio.testa, tizio.pos)
        screen.blit(tizio.corpo,tizio.corpo_pos)
        screen.blit(tizio.bracciodx, tizio.bracciodx_pos)
        screen.blit(tizio.bracciosx, tizio.bracciosx_pos)
        screen.blit(tizio.gambadx, tizio.gambadx_pos)
        screen.blit(tizio.gambasx, tizio.gambasx_pos)
        #finire il disegno del tizio
        
        tizio.movedx()
        pygame.display.update()
    print "fine loop"
    return 0

class Scheletro:
    busto=60
    braccio=30
    gamba=30
    
    def __init__(self):
        self.head=40
        self.pos=pygame.Rect(300, 100, 0, 0) # dove piazzare la testa (punto riferimento)
        
        #creo le superfici
        self.corpo = pygame.Surface((2, self.busto))
        self.gambasx = pygame.Surface((2, self.gamba),pygame.SRCALPHA)
        self.gambadx = pygame.Surface((2, self.gamba),pygame.SRCALPHA)
        self.bracciosx = pygame.Surface((2, self.braccio),pygame.SRCALPHA)
        self.bracciodx = pygame.Surface((2, self.braccio),pygame.SRCALPHA)
        self.testa = pygame.Surface((self.head, self.head),pygame.SRCALPHA)
        self.posiziona()
        self.disegna()
        
    def posiziona(self):
        #posiziono le superfici
        self.corpo_pos=self.pos.move(self.head/2,self.head)
        self.bracciodx_pos=self.pos.move(self.head/2,self.head)
        self.bracciosx_pos=self.pos.move(self.head/2,self.head)
        self.gambadx_pos=self.pos.move(self.head/2,self.head+self.busto)
        self.gambasx_pos=self.pos.move(self.head/2,self.head+self.busto)
        
    def disegna(self):
        
        #disegno i pezzi
        pygame.gfxdraw.aacircle(self.testa, self.head/2, self.head/2, self.head/2, (0, 0, 0))
        pygame.gfxdraw.vline(self.gambadx,0,0,self.busto,(0,255,0))
        pygame.gfxdraw.vline(self.gambasx,0,0,self.busto,(0,255,0))
        pygame.gfxdraw.vline(self.bracciodx,0,0,self.braccio,(255,0,0))
        pygame.gfxdraw.vline(self.bracciosx,0,0,self.braccio,(255,0,0))
        
        #ruoto i pezzi in posizione di default
        self.gambadx = pygame.transform.rotate(self.gambadx, 20)
        self.gambasx = pygame.transform.rotate(self.gambasx, -20)
        self.bracciodx = pygame.transform.rotate(self.bracciodx, 20)
        self.bracciosx = pygame.transform.rotate(self.bracciosx, -20)

        #(matematica)
        rad=math.radians(20)
        raggio=self.gambasx.get_height()
        offset=(math.sin(rad)*raggio)
        self.gambasx_pos = self.gambasx_pos.move(-offset,0)
        self.bracciosx_pos = self.bracciosx_pos.move(-offset,0)
        
    def assembla():
        null
                
    def movedx(self):
        self.pos = self.pos.move(2, 0)
        self.posiziona()
        
    def movesx(self):
        self.pos = self.pos.move(-2, 0)


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
                
if __name__ == '__main__':
	main()
