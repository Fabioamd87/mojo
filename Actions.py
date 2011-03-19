import pygame

def walk(obj,pos,b,s):
    if obj.rect[0]<pos[0]:
        print "move to dx"
        while (obj.rect[0]+obj.width/2)<pos[0]:
            obj.movedx()
            b.render()
            s.render()
            obj.render()
                
            pygame.display.update()
                
    else:
        print "move to sx"
        while (obj.rect[0]+obj.width/2)>pos[0]:
            obj.movesx()
            b.render()
            s.render()
            obj.render()
            pygame.display.update()

def talk(text):
        text1 = pygame.font.render("", 1, (10, 10, 10)) #What the fuck?!?
        screen.blit(text1,(0,0))
        pygame.time.delay(1000)
