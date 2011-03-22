import pygame
import Render

def walk(b,t,screen,text_in_game,pointergroup,oggetti,pos):
    while (t.rect[0]+t.width/2)<pos[0]:
        t.movedx()
        Render.render(screen,b,t,oggetti,text_in_game,pointergroup)
        for event in pygame.event.get(): #questo controllo interno rallenta molto
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                print "fine"
                sys.exit()
            if pygame.mouse.get_pressed()==(1,0,0):
                pos= pygame.mouse.get_pos()

    while (t.rect[0]+t.width/2)>pos[0]:
        t.movesx()
        Render.render(screen,b,t,oggetti,text_in_game,pointergroup)
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                print "fine"
                sys.exit()
            if pygame.mouse.get_pressed()==(1,0,0):
                pos= pygame.mouse.get_pos()

def talk(text):
        text1 = pygame.font.render("", 1, (10, 10, 10)) #What the fuck?!?
        screen.blit(text1,(0,0))
        pygame.time.delay(1000)
