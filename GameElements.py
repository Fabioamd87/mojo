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
    def __init__(self,idObject,idScenario):
        pygame.sprite.Sprite.__init__(self)
        
        self.load_data(idObject,idScenario)
        
    def on_view(self):
        print self.view_text
    def on_take(self):
        print self.take_text
    def on_talk(self):
        print self.talk_text
    
    def load_data(self,idObject,idScenario):
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('select Name from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        name = c.fetchone()
        c.execute('select Filename from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        filename = c.fetchone()
        self.image = Functions.load_image('object',filename[0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.name = name[0]
        
        c.execute('select top,left from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        pos = c.fetchone()
        print 'pos', pos
        self.rect.top,self.rect.left = pos
        
        c.execute('select onview, ontake, ontalk from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        actions = c.fetchone()
        print 'actions', actions
        self.view_text = actions[0] #unico comando?
        self.take_text = actions[1]
        self.talk_text = actions[2]
        
        #self.raggiungibile, indica se raggiungibile quando clicco su esamina
        
        
        c.close()
        
class Background(pygame.sprite.Sprite):
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
