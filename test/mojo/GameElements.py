import pygame
import sqlite3
from ConfigParser import RawConfigParser

import Functions
import Inventory

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
        self.Type = 'direction'            
        
        #self.load_data(iddirections,idscenario)
        self.rect = pygame.Rect(rect)
        self.name = name
        self.destination = destination
        
    def load_data(self,iddirection,idscenario):
        #se l'area sensibile non esiste non deve caricare niente.      
        #evito i database  
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
        self.Type = 'object'
        self.load_data(idObject,idScenario,c)
        self.visible = True
    
    def load_data(self,idObject,idScenario,c):
        
        c.execute('select Name from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        name = c.fetchone()
        self.name = name[0]
        
        c.execute('select Filename from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        filename = c.fetchone()
        self.image = Functions.load_image('object',filename[0]).convert_alpha()
        self.rect = self.image.get_rect()        
        
        c.execute('select top, left from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        pos = c.fetchone()
        self.rect.top, self.rect.left = pos
        
        c.execute('select onview, ontake, ontalk from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        actions = c.fetchone()
        self.view_text,self.take_text,self.talk_text = actions
        
        c.execute('select Takeable from Objects where idObject = ' + str(idObject) + ' and idscenario = ' + str(idScenario))
        self.takeable = c.fetchone()
        self.takeable = self.takeable[0]
        
        #self.raggiungibile, indica se bisogna avvicinarsi quando clicco su esamina
        
    def Update(self,inventory):
        if self.name in inventory.Objects:
            print 'nascondo'
            self.visible = False
        
class Background(pygame.sprite.Sprite):
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        
class Character(pygame.sprite.Sprite):
    def __init__(self,image,pos,name):
        pygame.sprite.Sprite.__init__(self)
        self.Type = 'character'
        
        self.images = Functions.carica_imm_sprite('character',image,100,60,1)
        
        #carico il primo frame come immagine
        self.image = self.images[0]
        self.rect = pygame.Rect(pos,self.image.get_size())
        self.name = name
        
        #self.load_from_db(idCharacter,idScenario,c)
        self.frame_corrente = 0
        self.clock = pygame.time.Clock()
        
        self.time = 1000 #variabile
        self.slowliness = 120 #fisso, nel gioco usare 60
        
        self.talking = False
        
    def load_from_db(self,idCharacter,idScenario,c):
        c.execute('select filename, frameheight, framewidth, name, top, left from Characters where idCharacter = ' + str(idCharacter) + ' and idscenario = ' + str(idScenario))        
        data = c.fetchone()
        self.immagini = Functions.carica_imm_sprite('character',data[0],data[1],data[2],1)
        self.image = self.immagini[0]
        self.rect = pygame.Rect((data[5],data[4]),self.image.get_size())
        self.name = data[3]
        
    def update(self):
        if pygame.time.get_ticks() < self.time:
            return
            
        self.time=self.time+self.slowliness
		
        if self.talking:
            self.move_lips()
    
    def move_lips(self):
        if self.frame_corrente < 2:
            self.frame_corrente += 1
        if self.frame_corrente == 2:
            self.frame_corrente = 0
        self.image=self.immagini[self.frame_corrente]

class Pointer(pygame.sprite.Sprite):
    """puntatore del mouse grafico"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = Functions.load_image('pointer','pointer.png', -1)

    def update(self):                                          
        self.rect.midtop = pygame.mouse.get_pos()
