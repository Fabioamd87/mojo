import pygame
import sqlite3
from ConfigParser import RawConfigParser

import Functions
import Inventory
import GameElements
import Text

class Scenario(pygame.sprite.Sprite):
    def __init__(self):
        
        self.objects_in_game = pygame.sprite.Group()
        self.directions = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.text_in_game = pygame.sprite.Group()
        
        self.collideable = pygame.sprite.Group()
        self.collideable.add(self.objects_in_game,self.directions,self.characters)

        self.background = GameElements.Background()        
        self.textbox = Text.TextOnScreen()
        self.inventory = Inventory.Inventory()
        
        self.text_in_game.add(self.textbox)
        self.text_in_game.add(self.textbox.examine,self.textbox.take,self.textbox.talk) #metodo migliore?
        self.text_in_game.add(self.textbox.speak)
        self.text_in_game.add(self.textbox.line1)
        self.text_in_game.add(self.textbox.toptext)
        

    def load(self,idscenario): #invece dell'id potrei passare un nome "univoco"
        """carica tutti i dati dello scenario, funzione generica"""
        
        #svuoto gli oggetti/direzioni/personaggi dello scenario precedente
        self.objects_in_game.empty()
        self.directions.empty()
        self.characters.empty()
        
        #inizializzo il database
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
                self.objects_in_game.add(obj_i)
        
        #load characters
        n = c.execute('select idCharacter from characters where idscenario = ' + str(idscenario))
        n = n.fetchone()
        
        if n:
            for i in n:
                print 'loading characters'
                character_i = GameElements.Character(i,idscenario,c)
                self.characters.add(character_i)
        c.close()
        
        #insieme di tutti gli elementi dello scenario, usata nelle funzioni di controllo collisione
        self.game_elements = pygame.sprite.Group(self.objects_in_game,self.directions,self.characters)
        
        #potrebbe caricare uno script di azioni da svolgere per ogni scenario
        self.textbox.speak.visible = True
        self.textbox.speak.write('ok, il debug lo faccio io')
        
    def Update(self,pointergroup, player):
                    
        for i in self.characters:
			i.update()
            
        self.textbox.update(pointergroup,self.game_elements)
        self.textbox.show_name(pointergroup,self.game_elements)
        self.textbox.calcola_posizione_box(player.rect.topleft)
        
        #se il menu e' aperto controllo se seleziono un'azione
        if self.textbox.menuVisible:
            self.textbox.select(pointergroup,self.textbox.sprite.name)
        
        self.ControlCollision(player)
        self.inventory.Update(pointergroup)
        
    def MouseCollide(self,pointergroup):
        if pygame.sprite.groupcollide(pointergroup,self.objects_in_game,0,0):
            return True
        else:
            return False

    def OnClickReleased(self,event):
        """ controlla se al rilascio del pulsante del mouse un'azione e' selezionata"""
        if event.dict['button'] == 3:
            if self.textbox.sprite.Type == 'character' or self.textbox.sprite.Type == 'object':
                if self.textbox.examine.highlited == True:
                    print 'esamino'
                    self.textbox.speak.visible = True
                    self.textbox.speak.write('esamino')
                if self.textbox.take.highlited == True:
                    print 'prendo'
                if self.textbox.talk.highlited == True:
                    print 'parlo'
                for i in self.objects_in_game:
                    i.Update(self.inventory)
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
            
    def playmusic(self):
        """ Stream music with mixer.music module in blocking manner.
        This will stream the sound from disk while playing. """
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()
