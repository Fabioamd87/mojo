import pygame

class Inventory(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)        
        self.rect = pygame.Rect(0,0,1024,10)
        self.box = Box()
    def close(self):
        self.box.rect.top = -80

class Box(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/imgs/inventory.png')
        self.rect = self.image.get_rect()
        self.rect.top = -80
        self.opened = False
        
    def increase_y(self):
        """ il metodo ad incrementi dipende molto dal pc e dal SO"""
        if self.rect.top < 0:
            self.rect.top += 2
        else:
            self.opened = True
