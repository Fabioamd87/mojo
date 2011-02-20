import pygame
import pygame.gfxdraw
import sys

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
            if pygame.mouse.get_pressed()==(1,0,0):
                mojo.walkto(pygame.mouse.get_pos())
        screen.blit(textbox.text1, (0,400))
        
        screen.blit(tizio.testa, (300,100))
        screen.blit(tizio.corpo,(300+tizio.head/2,100+tizio.head))
        screen.blit(tizio.bracciodx, (300+tizio.head/2,100+tizio.head))
        screen.blit(tizio.gambadx, (300+tizio.head/2,100+tizio.head+tizio.busto))
                
        pygame.display.update()
    print "fine loop"
    return 0

class Scheletro:
    busto=60
    braccio=30
    gamba=30
    head=40
    pos=(300,100) #punto riferimento centro testa
    def __init__(self):
        self.corpo = pygame.Surface((2, self.busto))
        self.gambasx = pygame.Surface((2, self.gamba))
        self.gambadx = pygame.Surface((2, self.gamba))
        self.bracciosx = pygame.Surface((2, self.braccio))
        self.bracciodx = pygame.Surface((2, self.braccio))
        self.testa = pygame.Surface((self.head, self.head),pygame.SRCALPHA)
        self.disegna()
        self.colora()
    def disegna(self):
        print "disegno"
        pygame.gfxdraw.aacircle(self.testa, self.head/2, self.head/2, self.head/2, (0, 0, 0))
        pygame.transform.rotate(self.gambadx, 20)
        pygame.transform.rotate(self.bracciodx, 45)
    def assembla():
        null
    def colora(self):
        print "coloro"
        self.corpo.fill((0,0,0))
        self.gambadx.fill((0,255,0))
        self.gambasx.fill((0,0,0))
        self.bracciodx.fill((0,0,255))
        self.bracciosx.fill((0,0,0))
        #self.testa.fill((0,0,0))


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
