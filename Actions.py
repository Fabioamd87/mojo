import pygame
import Render

def walk(b,t,screen,pos,oggetti):
    if t.rect[0]<pos[0]:
        print "move to dx"
        while (t.rect[0]+t.width/2)<pos[0]:
            t.movedx()
            Render.render(screen,b,t,oggetti)
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN): # qualsiasi tasto premuto
                    print "fine"
                    sys.exit()
                if pygame.mouse.get_pressed()==(1,0,0): #click sinistro del mouse
                    walk(b,t,screen,pygame.mouse.get_pos(),oggetti)
    else:
        print "move to sx"
        while (t.rect[0]+t.width/2)>pos[0]:
            t.movesx()
            Render.render(screen,b,t,oggetti)
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN): # qualsiasi tasto premuto
                    print "fine"
                    sys.exit()
                if pygame.mouse.get_pressed()==(1,0,0): #click sinistro del mouse
                    walk(b,t,screen,pygame.mouse.get_pos(),oggetti)

def talk(text):
        text1 = pygame.font.render("", 1, (10, 10, 10)) #What the fuck?!?
        screen.blit(text1,(0,0))
        pygame.time.delay(1000)
