import pygame
import Render

def walk(b,t,screen,pos,oggetti):
    if t.rect[0]<pos[0]:
        print "move to dx"
        while (t.rect[0]+t.width/2)<pos[0]:
            t.movedx()
            Render.render(screen,b,t,oggetti)
    else:
        print "move to sx"
        while (t.rect[0]+t.width/2)>pos[0]:
            t.movesx()
            Render.render(screen,b,t,oggetti)

def talk(text):
        text1 = pygame.font.render("", 1, (10, 10, 10)) #What the fuck?!?
        screen.blit(text1,(0,0))
        pygame.time.delay(1000)
