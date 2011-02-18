import pygame
import sys

def main():
    screen = pygame.display.set_mode((1024, 480))
    player = pygame.image.load('player.gif').convert()
    background = Background()
    mojo=GameObject(screen,player,background.image)
    textbox=TextOnScreen(screen)
    screen.blit(background.image, (0, 0))
    screen.blit(mojo.image, mojo.pos)
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                print "fine"
                sys.exit()
            if pygame.mouse.get_pressed()==(1,0,0):
                mojo.walkto(pygame.mouse.get_pos())
        screen.blit(textbox.text1, (0,400))
        pygame.display.update()
    print "fine loop"
    return 0

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
        
	
class GameObject:
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
