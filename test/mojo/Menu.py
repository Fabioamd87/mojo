import pygame
import sys

import Game
import Functions
import Widgets


class Menu():
    def __init__(self):
        
        #self.font = pygame.font.Font(None, 36)
        self.menubox = Widgets.MenuBox()
        self.background = pygame.image.load('data/imgs/backgrounds/menu.png').convert()
        #Functions.play_audio('music', 'Photograph.ogg')
        
    def run(self,screen,pointergroup):
        
        

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
        
        
        
        while True:
            for event in pygame.event.get():
            
                #questo dovrebbe essere la pressione sulla X della finestra?
                if event.type == (pygame.QUIT):
                    print "fine"
                    sys.exit()
                    
                if event.type == (pygame.KEYDOWN):
                    if pygame.key.get_pressed()[27]:
                        print "fine"
                        sys.exit()
                    else:
                        print "inizio"
                        pygame.time.wait(250)
                        Game.run(screen,pointergroup) #!!!!!
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()==(1,0,0):
                        if self.menubox.new_game.highlited:
                            print "inizio"
                            #rallento altrimenti interpreta subito il click come uno spostamento del personaggio
                            pygame.time.wait(250)
                            Game.run(screen,pointergroup) #!!!!!
                        if self.menubox.exit_game.highlited:
                            print "fine"
                            sys.exit()
                        if self.menubox.continue_game.highlited:
                            pass
                        
            #non uso Render            
            self.menubox.update()
            
            screen.blit(self.background,(0,0))
            pointergroup.update()
            self.menubox.buttons.draw(screen)
            pointergroup.draw(screen)
            pygame.display.update()
"""
class MenuBox(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        
        #i bottoni vengono inseriti con le coordinate
        self.new_game = Widgets.Button('New Game',(300,200))
        self.exit_game = Widgets.Button('Exit Game',(300,250))
        self.continue_game = Widgets.Button('Continue Game',(300,300))
        
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.new_game)
        self.buttons.add(self.exit_game)
        self.buttons.add(self.continue_game)
        
    def update(self):
        #chiama a sua volta il metodo update di "Widget.Button"
        self.new_game.update()
        self.exit_game.update()
        self.continue_game.update()
"""
