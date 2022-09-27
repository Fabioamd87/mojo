import pygame
from configparser import RawConfigParser

import functions
import widgets

class Element(pygame.sprite.Sprite):
    #generic class, overloaded in Object and Character
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)

        self.visible = True
        self.name = name        

    def draw(self,screen):
        screen.blit(self.image, self.rect)        

class Object(Element):
    #special kind of object class
    def __init__(self, name, image, pos):
        Element.__init__(self, name)
        self.type = 'object'
        self.pos = pos
        self.image = functions.load_image(self.type,image)
        self.rect = pygame.Rect(self.pos,self.image.get_size())

        self.in_inventory = False
        self.inventory_position = 0

        self.event_on_examine = None
        self.event_on_talk = None
        self.event_on_take = None

    def set_event_on_examine(self,event):
        self.event_on_examine = event
        self.menu.examine.event = event

    def set_event_on_take(self,event):
        self.event_on_take = event
        self.menu.take.event = event

    def set_event_on_talk(self,event):
        self.event_on_talk = event
        self.menu.talk.event = event


class Character(Element):
    def __init__(self,name, image, pos):
        Element.__init__(self, name)

        self.type = 'character'        
        self.pos = pos
        self.images = functions.carica_imm_sprite('character',image,100,60,1)
        
        #carico il primo frame come immagine
        self.image = self.images[0]
        self.rect = pygame.Rect(self.pos, self.image.get_size())

class Directions(pygame.sprite.Sprite):
    def __init__(self,name,destination,rect):
        """questa classe contiene le aree che permettono al personaggio
            se cliccate di cambiare scenario.
            la stessa classe si potrebbe usare per creare delle
            animazioni se li personaggio collide con quest'area.
            come attributo, oltre al nome dell'area, la destinazione e
            la posizione va specificato anche il punto dove posizionare
            il personaggio una volta cambiato lo scenario.
        """
        pygame.sprite.Sprite.__init__(self)
        self.type = 'direction'

        self.name = name
        self.destination = destination
        self.rect = pygame.Rect(rect)
        self.event = pygame.event.Event(pygame.USEREVENT+1,{'subcat':0,'destination':self.destination})

class Pointer(pygame.sprite.Sprite):
    """puntatore del mouse grafico"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = functions.load_image('pointer','pointer.png', -1)

    def update(self):                                          
        self.rect.midtop = pygame.mouse.get_pos()

class Background(pygame.sprite.Sprite):
    """il senso di creare una classe ancora non e' definito"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0,0,0,0)