import pygame
import sqlite3
from ConfigParser import RawConfigParser

import Functions
import Inventory
import GameElements
import Text
import Actions



class Scenario(pygame.sprite.Sprite):
    def __init__(self):

        self.objects = pygame.sprite.Group()
        self.directions = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.text_in_game = pygame.sprite.Group()
        
        self.collideable = pygame.sprite.Group()
        self.collideable.add(self.objects,self.directions,self.characters)

        self.background = GameElements.Background()        
        self.textbox = Text.TextOnScreen()
        self.inventario = Inventory.Inventory()
        
        self.text_in_game.add(self.textbox)
        self.text_in_game.add(self.textbox.e,self.textbox.p,self.textbox.t)
        self.text_in_game.add(self.textbox.speak)
        self.text_in_game.add(self.textbox.line1)

    def load(self,idscenario):
        
        self.objects.empty()
        self.directions.empty()
        self.characters.empty()
        
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
        print 'tupla con tutti gli id delle direzioni dello scenario:' , n
                
        if n:
            for i in n:
                rect_i = GameElements.Directions(i,idscenario)
                self.directions.add(rect_i)
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        #load objects
        n = c.execute('select idobject from objects where idscenario = ' + str(idscenario))
        n = n.fetchone()
        
        if n:
            for i in n:
                print 'loading objects'
                obj_i = GameElements.Object(i,idscenario,c)
                self.objects.add(obj_i)
        
        #load characters
        n = c.execute('select idCharacter from characters where idscenario = ' + str(idscenario))
        n = n.fetchone()
        
        if n:
            for i in n:
                print 'loading characters'
                character_i = GameElements.Character(i,idscenario,c)
                self.characters.add(character_i)
        c.close()
        
    def Update(self,pointergroup, player):
        
        group = pygame.sprite.Group(self.objects,self.directions,self.characters)
        
        if pygame.mouse.get_pressed()==(1,0,0):
            if not player.talking:
                player.walkto(pygame.mouse.get_pos())
        
        if pygame.mouse.get_pressed()==(0,0,1):
            self.OpenActionMenu(pointergroup,group)
            
        for i in self.characters:
			i.update()

        self.textbox.show_name(pointergroup,group)
        self.textbox.calcola_posizione_box(player.rect.topleft)
        if self.textbox.menuVisible:
            self.textbox.select(pointergroup,self.textbox.sprite.name)
        
        self.ControlCollision(player)
        
        if pygame.sprite.spritecollide(self.inventario, pointergroup, 0):
            self.inventario.box.increase_y()
        elif pygame.sprite.spritecollide(self.inventario.box, pointergroup, 0) == []:            
            self.inventario.close()
          
    def playmusic(self):
        """Stream music with mixer.music module in blocking manner.
        This will stream the sound from disk while playing.
        """
        
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()
        
    def MouseCollide(self,pointergroup):
        if pygame.sprite.groupcollide(pointergroup,self.objects,0,0):
            return True
        else:
            return False

    def OnClickReleased(self,event):
        if event.dict['button'] == 3:
            #self.textbox.DoThings() #evito questo metodo
            Actions.DoThings(self.textbox)
        self.CloseActionMenu()
        
    def OpenActionMenu(self,pointergroup,group):
        self.textbox.calcolable = False
        
        pointer = pointergroup.sprites()[0]
        self.sprite = pygame.sprite.spritecollideany(pointer,group)
        
        if self.sprite:     
            self.textbox.show_menu()

    def CloseActionMenu(self):
        self.textbox.hide_menu()
        self.textbox.calcolable = True
            
    def ControlCollision(self,t):
        where = pygame.sprite.spritecollide(t,self.directions,0)
        if where:
            self.load(where[0].iddestination)                    
            t.position(100,250)
            t.is_moving = False
