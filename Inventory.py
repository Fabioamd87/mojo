import pygame

class Inventory(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)        
        self.rect = pygame.Rect(0,0,1024,10) #area sensibile
        self.box = Box()
        self.Objects = []
        
    def add(self,sprite):
        self.box.add(sprite)
        self.Objects.append(sprite.name)
        
    def Update(self,pointergroup):
        if pygame.sprite.spritecollide(self, pointergroup, 0):
            self.box.increase_y()
        elif pygame.sprite.spritecollide(self.box, pointergroup, 0) == []:            
            self.box.close()

class Box(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/imgs/inventory.png')
        self.rect = self.image.get_rect()
        self.opened = False
        
        self.Objects = []
        self.n = 0
        
    def increase_y(self):
        """ il metodo ad incrementi dipende molto dal pc e dal SO"""
        if self.rect.top < 0:
            self.rect.top += 2
        else:
            self.opened = True
    
    def close(self):
        self.rect.top = -80
        
    def add(self,sprite):
        self.n=+1
        self.image.blit(sprite.image,(self.n*50,0))
