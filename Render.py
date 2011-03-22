"""disegna la scena"""
import pygame

def render(screen,b,t,oggetti,text=pygame.sprite.Group(),pointergroup=pygame.sprite.Group()):
    screen.blit(b.image, b.rect)
    for i in oggetti:
        screen.blit(i.image, i.rect)
    screen.blit(t.image, t.rect)
    for i in text:
        if i.visible:
            screen.blit(i.text, i.rect)    
    pointergroup.update()
    pointergroup.draw(screen)
    pygame.display.update()
