import pygame
import sqlite3
from ConfigParser import RawConfigParser

import Functions
import Inventory
import GameElements
import Widgets
import Player

class Scenario(pygame.sprite.Sprite):
    def __init__(self):
        
        self.objects_in_game = pygame.sprite.Group()
        self.directions = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.text_in_game = pygame.sprite.Group()
        
        self.collideable = pygame.sprite.Group()
        self.collideable.add(self.objects_in_game,self.directions,self.characters)

        self.background = GameElements.Background()        
        self.textbox = Widgets.TextOnScreen()
        self.inventory = Inventory.Inventory()
        
        self.text_in_game.add(self.textbox.menu.examine,self.textbox.menu.take,self.textbox.menu.talk) #metodo migliore?
        self.text_in_game.add(self.textbox.speak)
        self.text_in_game.add(self.textbox.line1)
        self.text_in_game.add(self.textbox.toptext)
        self.text_in_game.add(self.textbox.info)
        
        self.player = Player.Player('player.png',150,50,1)
        
        self.characters.add(self.player)
        
        self.running = True
        self.change = False
        
    """
    def load(self,idscenario): #invece dell'id potrei passare un nome "univoco"
        #carica tutti i dati dello scenario, funzione generica
        
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
    """    
    def Update(self,pointergroup, clock, event):
        """il menu ha un update tutto suo"""
        if event.type == pygame.MOUSEBUTTONUP:
            self.OnClickReleased(event)
                
        if pygame.mouse.get_pressed()==(1,0,0):
            if not self.player.talking:
                self.player.walkto(pygame.mouse.get_pos())
                
        if pygame.mouse.get_pressed()==(0,0,1):
            self.OnRightClick(pointergroup)
                    
        for i in self.characters:
            i.update()
            
        self.textbox.update(pointergroup,self.game_elements)
        #self.textbox.show_name(pointergroup,self.game_elements)
                
        #se il menu e' aperto controllo se seleziono un'azione
        #if self.textbox.menu.visible:
        #    self.textbox.update(pointergroup,self.textbox.sprite.name)
        
        self.ControlCollision(self.player)
        self.inventory.Update(pointergroup)
        
        #show FPS
        self.textbox.info.write('FPS:' + str(int(clock.get_fps())))        
        
        player.Update()
        
    def Render(self):
        pass
    
    def Change(self, name):
        scenario = scenario.name
        return scenario
        pass
        
    def MouseCollide(self,pointergroup):
        if pygame.sprite.groupcollide(pointergroup,self.objects_in_game,0,0):
            return True
        else:
            return False

    def OnClickReleased(self,event):
        """ controlla se al rilascio del pulsante del mouse 
        uno psprite collide con un personaggio o oggetto
        e un'azione e' selezionata"""
        
        if event.dict['button'] == 3:
            #lo sprite andrebbe perso se il mouse non collide con l'oggetto
            #quindi faccio in modo che venga salvato nella classe menu
            
            #questa classe non deve accedere direttamente ai dati
            #altrimenti un cambiamento di struttura in text comporterebbe
            #un cambiamento qui
            if self.textbox.sprite is not None and (self.textbox.sprite.Type == 'character' or self.textbox.sprite.Type == 'object'):
                if self.textbox.menu.examine.highlited == True:
                    print 'esamino'
                    self.textbox.menu.talk.visible = True # voce talk del menu
                    self.textbox.speak.write('esamino') #speak del personaggio
                if self.textbox.menu.take.highlited == True:
                    print 'prendo'
                if self.textbox.menu.talk.highlited == True:
                    print 'parlo'
                for i in self.objects_in_game:
                    i.Update(self.inventory)
        self.CloseActionMenu()
    
    def OnRightClick(self,pointergroup):
        """ controlla se al click del pulsante destro del mouse 
        uno sprite collide con un personaggio o oggetto
        per decidere se aprire il menu"""

        if self.textbox.sprite is not None:
            if(self.textbox.sprite.Type == 'character' or self.textbox.sprite.Type == 'object'):
                self.OpenActionMenu(pointergroup)
        pass
        
    def OpenActionMenu(self,pointergroup):
        
        self.textbox.menu.moveable = False
        
        pointer = pointergroup.sprites()[0]
        self.sprite = pygame.sprite.spritecollideany(pointer,self.game_elements)
        
        if self.sprite:
            self.textbox.menu.show()

    def CloseActionMenu(self):
        self.textbox.menu.hide()
        self.textbox.calcolable = True
            
    def ControlCollision(self,t):
        where = pygame.sprite.spritecollide(t,self.directions,0)
        if where and pygame.mouse.get_pressed()==(1,0,0):
            # non puo caricare a "cascata" dovrebbe ritornare qualcosa
            self.load(where[0].destination)                    
            t.position(100,250)
            t.is_moving = False
            
    def playmusic(self):
        """ Stream music with mixer.music module in blocking manner.
        This will stream the sound from disk while playing. """
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()

class Menu(Scenario):
    def load(self):
     
        self.background.image = Functions.load_image('background','menu.png')        
        #self.menubox = Widgets.MenuBox()
        
        self.new_game = Widgets.Button('New Game',(300,200))
        self.exit_game = Widgets.Button('Exit Game',(300,250))
        self.continue_game = Widgets.Button('Continue Game',(300,300))
        
        self.interface = Widgets.Interface()
        self.interface.add(self.new_game)
        self.interface.add(self.exit_game)
        self.interface.add(self.continue_game)
        
        self.bottoni = pygame.sprite.Group(self.new_game,self.exit_game,self.continue_game)
           
    def Update(self,pointergroup, clock, event):
        """e' un overloading perche' scenario gia' ha una classe update"""

        if pygame.mouse.get_pressed()==(1,0,0):
            #se e' premuto il pulsante fai partire change
            pass #gestisci il menu
            
        self.pointergroup = pointergroup
        self.pointergroup.update()
        #self.menubox.update()
        
        self.interface.update()
        
    def Render(self,screen):
        
        screen.blit(self.background.image, self.background.rect)
        #self.menubox.buttons.draw(screen)
        #attenzione! in Update la classe cattura il cursore e lo aggiorna, qui lo disegna
        self.pointergroup.draw(screen)
        
        self.bottoni.draw(screen)
        
        pygame.display.update()
        
class Intro(Scenario):
    def load(self):
                
        self.background.image = Functions.load_image('background','intro.jpg')
   
        porta = GameElements.Directions('porta','bar',(732,245,100,100))
        self.directions.add(porta)

        spank = GameElements.Character('spank.png',(0,0),'spank')
        self.characters.add(spank)
        
        #insieme di tutti gli elementi dello scenario, usata nelle funzioni di controllo collisione
        self.game_elements = pygame.sprite.Group(self.objects_in_game,self.directions,self.characters)
        
        #potrebbe caricare uno script di azioni da svolgere per ogni scenario
        #self.textbox.speak.visible = True
        #self.textbox.speak.write('ok, il debug lo faccio io')
    
    def add_object(self,obj):
        pass

class Bar(Scenario):
    def load(self):

        self.background.image = Functions.load_image('background','intro.jpg')
   
        porta = GameElements.Directions('porta','bar',(732,245,100,100))
        self.directions.add(porta)

        print 'loading characters'
        spank = GameElements.Character('spank.png',(0,0),'spank')
        self.characters.add(spank)

        #insieme di tutti gli elementi dello scenario, usata nelle funzioni di controllo collisione
        self.game_elements = pygame.sprite.Group(self.objects_in_game,self.directions,self.characters)
        
        #potrebbe caricare uno script di azioni da svolgere per ogni scenario
        self.textbox.speak.visible = True
        self.textbox.speak.write('ok, il debug lo faccio io')