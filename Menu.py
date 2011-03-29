import pygame
import sys

import Game

def run():

    screen = pygame.display.set_mode((1024, 480))
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('A Dying Flowers')
    
    font = pygame.font.Font(None, 36)
    
    menu_item = pygame.sprite.Group()
    background = pygame.image.load('data/imgs/backgrounds/menu.png').convert()
    
    new_game=pygame.Surface((200, 50))
    new_game = font.render('new game', 1, (100, 100, 100))
    
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
                    Game.run(screen)
         
            screen.blit(background,(0,0))
            screen.blit(new_game,(300,200))
            pygame.display.update()
