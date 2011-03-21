"""disegna la scena"""
import pygame

def render(screen,b,t,oggetti_livello_attuale,interazioni=pygame.sprite.Group(),pointergroup=pygame.sprite.Group()):
    screen.blit(b.image, b.rect)
    for i in oggetti_livello_attuale:
        screen.blit(i.image, i.rect)
    for i in interazioni:
        screen.blit(i.text, i.rect)
    screen.blit(t.image, t.rect)
    pointergroup.update()
    pointergroup.draw(screen)
    pygame.display.update()
