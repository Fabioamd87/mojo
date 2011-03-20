import pygame

def walk(b,t,screen,pos,oggetti):
    if t.rect[0]<pos[0]:
        print "move to dx"
        while (t.rect[0]+t.width/2)<pos[0]:
            t.movedx()
            b.render()  ##questo si ripete anche in sx, generalizzare!
            for i in oggetti:
                screen.blit(i.image, i.rect)
            t.render()
            pygame.display.update()
                
    else:
        print "move to sx"
        while (t.rect[0]+t.width/2)>pos[0]:
            t.movesx()
            b.render()
            for i in oggetti:
                screen.blit(i.image, i.rect)
            t.render()
            pygame.display.update()

def talk(text):
        text1 = pygame.font.render("", 1, (10, 10, 10)) #What the fuck?!?
        screen.blit(text1,(0,0))
        pygame.time.delay(1000)
