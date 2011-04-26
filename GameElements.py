import pygame
import sqlite3
from ConfigParser import RawConfigParser
import Functions
import Inventory

class Directions(pygame.sprite.Sprite):
    def __init__(self,iddirections,idscenario):
        pygame.sprite.Sprite.__init__(self)        
        self.load_data(iddirections,idscenario)
        
    def load_data(self,iddirection,idscenario):
        #se l'area sensibile non esiste non deve caricare niente.        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        c.execute('select left, top, width, height from rect where idrect = (select idrect from directions where iddirection = ' + str(iddirection) +' and idscenario = ' + str(idscenario) + ')')
        rect = c.fetchone()
        if rect:
            self.rect = pygame.Rect(rect)
        
        c.execute('select name from directions where iddirection = ' + str(iddirection) + ' and idscenario = ' + str(idscenario))
        self.name = c.fetchone()
        self.name = self.name[0]
        
        c.execute('select iddestination from directions where iddirection = ' + str(iddirection) + ' and idscenario = ' + str(idscenario))
        self.iddestination = c.fetchone()
        self.iddestination = self.iddestination[0]
        print 'destination= ' + str(self.iddestination)
        
        c.close()
        
        
class Object(pygame.sprite.Sprite):
    def __init__(self,idObject,idScenario,c):
        pygame.sprite.Sprite.__init__(self)
                
        self.load_data(idObject,idScenario,c)
        
    def on_view(self):
        return self.view_text
    def on_take(self):
        return self.take_text
    def on_talk(self):
        return self.talk_text
    
    def load_data(self,idObject,idScenario,c):
        
        c.execute('select Name from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        name = c.fetchone()
        self.name = name[0]
        
        c.execute('select Filename from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        filename = c.fetchone()
        self.image = Functions.load_image('object',filename[0]).convert_alpha()
        self.rect = self.image.get_rect()        
        
        c.execute('select top,left from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        pos = c.fetchone()
        self.rect.top,self.rect.left = pos
        
        c.execute('select onview, ontake, ontalk from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        actions = c.fetchone()
        self.view_text,self.take_text,self.talk_text = actions
        
        c.execute('select Takeable from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        self.takeable = c.fetchone()
        self.takeable = self.takeable[0]
        
        #self.raggiungibile, indica se raggiungibile quando clicco su esamina
        
class Background(pygame.sprite.Sprite):
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        
class Character(pygame.sprite.Sprite):
    def __init__(self,idCharacter,idScenario,c):
        pygame.sprite.Sprite.__init__(self)
        self.load_data(idCharacter,idScenario,c)
        
    def load_data(self,idCharacter,idScenario,c):
        c.execute('select filename, frameheight, framewidth, name, top, left from Characters where idCharacter = ' + str(idCharacter) + ' and idscenario = ' + str(idScenario))        
        data = c.fetchone()
        self.immagini = Functions.carica_imm_sprite('character',data[0],data[1],data[2],1)
        self.image = self.immagini[0]
        #self.image = Functions.load_image('character',data[0]).convert_alpha()
        self.rect = pygame.Rect((data[4],data[5]),self.image.get_size())
        self.name = data[3]
    #def move_lips(self)
        

class Pointer(pygame.sprite.Sprite):
    """puntatore del mouse grafico"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = Functions.load_image('pointer','pointer.png', -1)

    def update(self):                                          
        self.rect.midtop = pygame.mouse.get_pos()
