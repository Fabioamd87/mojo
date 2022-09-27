import pygame

"l'inventario contiene icone 50x50"

class Inventory(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('data/imgs/inventory.png')
        self.rect = self.image.get_rect()     
        self.sensible_area = pygame.Rect(0,0,1024,10) #area sensibile
        
        self.objects = []
        
        self.visible = False

    def update(self):
        if self.sensible_area.collidepoint(pygame.mouse.get_pos()):
            self.visible = True
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.visible = False

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)

    def add(self,sprite):
        self.box.add(sprite)
        self.objects.append(sprite)
