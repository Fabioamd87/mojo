import pygame
import sqlite3
from ConfigParser import RawConfigParser

import Functions
import Inventory
import GameElements
import Text

class Scenario(pygame.sprite.Sprite):
    def __init__(self):

        self.objects = pygame.sprite.Group()
        self.directions = pygame.sprite.Group()
        self.people = pygame.sprite.Group()
        self.text_in_game = pygame.sprite.Group()

        self.background = GameElements.Background()        
        self.textbox = Text.TextOnScreen()
        self.inventario = Inventory.Inventory()
        
        self.text_in_game.add(self.textbox,self.textbox.e,self.textbox.p,self.textbox.t)
        
    """
    def load_homemade(self,destination):
        with open(destination + '.txt') as f:
            for line in f:
                if line[0:10] == 'background':
                    background = line[13:len(line)-1]
                    print 'background: ' + background
                    self.background.image = Functions.load_image('background',background)
                if line[0:5] == 'music':
                    music = line[8:len(line)-1]
                    print 'music: ' + music
                    self.music = Functions.play_audio('music',music)
                if line[0:5] == '[rects]':
                    while line[0]=='[':
                        print line.readlines()
    """               

    def load(self,idscenario):
        
        self.objects.empty()
        self.directions.empty()
        self.people.empty()
        
        #dovrebbe eseguire un particolare script per ogni scenario
        """
        config = RawConfigParser()
        config.read(destination + '.txt')
        self.scene_name = config.get('Info', 'name')
        print 'scene name: ' + self.scene_name
        
        background = config.get('Info', 'background')
        self.background.image = Functions.load_image('background',background)
        print 'background: ' + background
        
        music = config.get('Info', 'music')
        self.music = Functions.play_audio('music',music)
        """
        # dovrebbe instanziare n_of_rect oggetti di tipo Scenario.Rect e inserirli nel gruppo rects
        
        """
        #load rects
        for line in config.items('Areas'):
            name = line[0]
            values = line[1].split(' ')
            rect_string = values[0]
            destination = values[1]
            rect = rect_string.split(',')
            for i in range(len(rect)): #convertion from str to int
                rect[i]=int(rect[i])
            rect = GameElements.Directions(name,rect,destination)
            self.directions.add(rect)
        """
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        #set background
        
        c.execute('select background from scenario where idscenario = ' + str(idscenario))
        background = c.fetchone()   
        self.background.image = Functions.load_image('background',background[0])
        
        #load directions
        
        n = c.execute('select iddirection from directions where idscenario = ' + str(idscenario))
        n = n.fetchone()
        c.close()
        print 'tupla con tutti gli id delle direzioni dello scenario' , n
                
        if n:
            for i in n:
                rect_i = GameElements.Directions(i,idscenario)
                self.directions.add(rect_i)
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #load objects
        n = c.execute('select idobject from objects where idscenario = ' + str(idscenario))
        n = n.fetchone()
        c.close()
        
        if n:
            for i in n:
                print 'loading objects'
                obj_i = GameElements.Object(i,idscenario)
                self.objects.add(obj_i)
        
        """
        for line in config.items('Objects'):
            carica solo i nomi e il percorso dei file, ogni oggetto avra il suo file 
            name = line[0]
            pos_string = line[1]
            position = pos_string.split(',')
            position[0] = int(position[0])
            position[1] = int(position[1])
            obj = Object(name,position)
            self.objects.add(obj)
         """   
    def playmusic(self):
        """Stream music with mixer.music module in blocking manner.
        This will stream the sound from disk while playing.
        """

        clock = pygame.time.Clock()
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
        #   clock.tick(FRAMERATE)
        
    def MouseCollide(self,pointergroup):
        if pygame.sprite.groupcollide(pointergroup,self.objects,0,0):
            return True
        else:
            return False

    def OnClickReleased(self):
        self.textbox.DoThings()
        self.CloseActionMenu()
        
    def OpenActionMenu(self,pointergroup):
        self.textbox.calcolable = False
        if self.textbox.name_settable:
            pointer = pointergroup.sprites()[0]
            obj = pygame.sprite.spritecollide(pointer,self.objects,0)
            if self.textbox.item:
                print 'show'
                self.textbox.set_name(obj[0].name)        
                self.textbox.show()
                self.textbox.name_settable = False
                
            
    def CloseActionMenu(self):
        self.textbox.hide()
        self.textbox.calcolable = True
        self.textbox.name_settable = True
        
    def Update(self,pointergroup, t):
        self.textbox.pointer_collide(pointergroup,self.objects,self.directions)
        self.textbox.calcola_posizione_box()
        self.textbox.select(pointergroup)
        
        self.ControlCollision(t)
        
        if pygame.sprite.spritecollide(self.inventario, pointergroup, 0):
            self.inventario.box.increase_y()
        elif pygame.sprite.spritecollide(self.inventario.box, pointergroup, 0) == []:            
            self.inventario.close()
            
    def ControlCollision(self,t):
        where = pygame.sprite.spritecollide(t,self.directions,0)
        if where:
            self.load(where[0].iddestination)                    
            t.position(100,250)
            t.is_moving = False
