import pygame
import Game

def run():

    screen = pygame.display.set_mode((1024, 480))
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('A Dying Flowers')
    
    menu_item = pygame.sprite.Group()
    background = pygame.image.load('menu.png').convert()
    
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN): # qualsiasi tasto premuto
                print "inizio"
                Game.run(screen)
        screen.blit(background,(0,0))
        pygame.display.update()
