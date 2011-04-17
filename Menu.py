import pygame
import sys

import Game
import Functions



def run(screen,pointergroup):
    
    font = pygame.font.Font(None, 36)

    """
    #intro
    text = font.render('Now there is', 1, (100, 100, 100))
    screen.blit(text,(300,200))
    pygame.display.update()
    pygame.time.delay(3000)
    
    text = font.render('My Fairtales', 1, (100, 100, 100))
    screen.fill((0,0,0))
    screen.blit(text,(300,200))
    pygame.display.update()    
    pygame.time.delay(3000)
    
    text = font.render('Of Dying Flowers...', 1, (100, 100, 100))
    screen.fill((0,0,0))
    screen.blit(text,(300,200))
    pygame.display.update()
    pygame.time.delay(3000)
    """
    
    menu = MenuBox()
    background = pygame.image.load('data/imgs/backgrounds/menu.png').convert()
    Functions.play_audio('music', 'Photograph.ogg')
    
    while True:
        for event in pygame.event.get():
        
            if event.type == (pygame.QUIT):
                print "fine"
                sys.exit()
            if event.type == (pygame.KEYDOWN):
                if pygame.key.get_pressed()[27]:
                    print "fine"
                    sys.exit()
                else:
                    print "inizio"
                    Game.run(screen,pointergroup)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()==(1,0,0):
                    if menu.new_game.highlited:
                        Game.run(screen,pointergroup)
                    if menu.exit_game.highlited:
                        print "fine"
                        sys.exit()
                    
        #non uso Render            
        screen.blit(background,(0,0))
        menu.update(pointergroup)
        pointergroup.update()
        screen.blit(menu.new_game.text,menu.new_game.rect)
        screen.blit(menu.exit_game.text,menu.exit_game.rect)
        pointergroup.draw(screen)
        pygame.display.update()
    
class MenuBox(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.new_game = self.Item('New Game',200)
        self.exit_game = self.Item('Exit Game',250)
        
    def update(self,pointergroup):
        self.new_game.update(pointergroup)
        self.exit_game.update(pointergroup)
            
    class Item(pygame.sprite.Sprite):
        def __init__(self,text,y):
            pygame.sprite.Sprite.__init__(self)
            self.name = text
            self.font = pygame.font.Font(None, 36)
            self.rect = pygame.Rect((300,y),self.font.size(text))
            self.text = self.font.render(self.name, 1, (100, 100, 100))
            self.highlited = False
            self.sound = False
            
        def update(self,pointergroup):
            if pygame.sprite.spritecollideany(self,pointergroup):
                self.text = self.font.render(self.name, 1, (255, 0, 0))
                self.highlited = True
                if self.sound == False:
                    Functions.play_audio('sound','tick.ogg')
                    self.sound = True
            else:
                self.text = self.font.render(self.name, 1, (100, 100, 100))
                self.highlited = False
                self.sound = False
