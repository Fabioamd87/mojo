import pygame

#from ConfigParser import RawConfigParser

import Functions
import Inventory
import GameElements

BLACK = (10,10,10)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
YELLOW = (255, 255, 10)

class TextOnScreen(pygame.sprite.Sprite):
    """
        classe che contiene tutti gli elementi di *testo* del gioco.

        Questa classe e' istanziata col nome di textbox nel file scenario,

        migliorare questa cosa
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #menu di interazione, appare al click destro
        self.menu = self.ActionMenu()
        
        #parlato personaggio, appare in un box a posizione variabile
        self.speak = self.SpeakBox()
        
        #gestione dialoghi, appare in basso
        self.line1 = self.DialogueBox()
        
        #descrozione oggetti, in alto al centro
        self.toptext = self.DescriptionBox()
        
        self.info = self.InfoBox()
        
        #controller, per ora inutile
        self.con = self.Controller()
    
    #compito da controller?    
    def update(self,pointergroup,game_elements):
        
        #sprite collidente, lo deve conoscere DescriptionBox e ActionMenu
        """questa funzione e' importante perche cattura l'oggetto
        che verra utilizzato nel menu, """
        
        self.menu.aggiorna_posizione_box()
            
        pointer = pointergroup.sprites()[0]
        self.sprite = pygame.sprite.spritecollideany(pointer,game_elements)
        
        if self.sprite:
            self.toptext.set_text(self.sprite)
            self.toptext.set_visible(True)
        else:
            self.toptext.set_visible(False)
        
        self.menu.update(pointergroup,game_elements)
                
        #dove appare cio che viene detto dal personaggio
        #self.speak.rect.topleft = player_pos[0]+50,player_pos[1]-30 #raffinare
    
    class ActionMenu():
        def __init__(self):
            self.examine = self.Action('esamina')
            self.take = self.Action('prendi')
            self.talk = self.Action('parla')
            
            self.visible = False
            self.moveable = True
            
            self.sprite = None #lo chiede all'inizio, per aprire il menu
                
        def hide(self):
            for i in self.examine,self.take,self.talk:
                i.visible=False
            self.visible = False

        def show(self):
            for i in self.examine,self.take,self.talk:
                i.visible=True
            self.visible = True
        
        def aggiorna_posizione_box(self):
            """questo metodo calcola la posizione del menu delle azioni"""
            if self.moveable: #ovvero abbiamo rilasciato il mouse
                pos = pygame.mouse.get_pos()
                self.examine.rect.topleft=pos[0]-25,pos[1]+30
                self.take.rect.topleft=pos[0]+30,pos[1]-30
                self.talk.rect.topleft=pos[0]-50,pos[1]-30
    
        def update(self,pointergroup, sprite):

            if sprite:
                self.sprite = sprite
            if self.visible == True:
                self.examine.update()
                self.take.update()
                self.talk.update()
                
            """controlla se selezioniamo un azione
                mostra in alto la descrizione
             secondo l'approccio MVC questo va nella view
            
            if self.examine.highlited:
                self.write("esamina " + name)
                
            if self.take.highlited:
                self.write("prendi " + name)
                
            if self.talk.highlited:
                self.write("parla con " + name)
            """
        class Action(pygame.sprite.Sprite):
            def __init__(self,name):
                pygame.sprite.Sprite.__init__(self)
                self.font = pygame.font.Font(None, 25)
                
                self.visible = False
                self.highlited = False
                
                self.label = name
                
                self.rect = pygame.Rect((0,0),self.font.size(name))
                self.text = self.font.render(name, 1, BLACK)
            
            def update(self):
                #controlla, ma solo se il menu è stato aperto
                print 'controllo' , self.label
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.select()
                else:
                    self.unselect()
            
            def select(self):
                """evidenzia l'opzione scelta"""
                print 'seleziono'
                self.highlited = True
                self.text = self.font.render(self.label, 1, YELLOW)
                self.font.set_italic(1)
                
                
            def unselect(self):
                """annulla la selezione"""
                self.highlited = False
                self.font.set_italic(0)
                self.text = self.font.render(self.label, 1, BLACK)
                
    class SpeakBox(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.font = pygame.font.Font(None, 25)
            self.visible = False
            self.rect = pygame.Rect(0,0,0,0)
            self.text = self.font.render('', 1, (10, 10, 10))
                        
        def write(self,text):
            self.rect = pygame.Rect((0,0),self.font.size(text))
            self.text = self.font.render(text, 1, (10, 10, 10))
    
    class DialogueBox(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)            
            self.font = pygame.font.Font(None, 25)
            
            self.highlited = False
            self.visible = False
            self.rect = pygame.Rect(20,400,0,0)
            self.text = self.font.render('Segnaposto per dialoghi', 1, (10, 10, 10))
            
        def write(self,text):
            self.rect = pygame.Rect((0,0),self.font.size(text))
            self.text = self.font.render(text, 1, (10, 10, 10))
            
    class DescriptionBox(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            
            #testo in alto
            self.rect = pygame.Rect(256,0,0,0)
            self.font = pygame.font.Font(None, 25)            
            self.visible = True
        
        def set_text(self,sprite):
            self.text = self.font.render(sprite.name, 1, BLACK)
            
        def set_visible(self,x):
            if x == True:
                self.visible = True
            else:
                self.visible = False

            
    class InfoBox(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            
            #testo in alto
            self.rect = pygame.Rect(768,0,0,0)
            self.font = pygame.font.Font(None, 25)
            self.text = self.font.render("prova", 1, (10, 10, 10))
            self.visible = True
            
        def write(self,text):
            self.text = self.font.render(text, 1, BLACK)
            
    class Controller():
        def getMenuVisible(self):
            return self.visible
            
class Button(pygame.sprite.Sprite):
    def __init__(self,label=None,pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.label = label
        self.font = pygame.font.Font(None, 36)
        #rect a dimensione del testo
        self.rect = pygame.Rect(pos,self.font.size(self.label))
        self.image = self.font.render(label, 1, GRAY)
        
        self.highlited = False
        self.sound = False
        
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.select()
        else:
            self.unselect()
    
    def select(self):
        self.highlited = True
        self.image = self.font.render(self.label, 1, RED)
        if self.sound == False:
            Functions.play_audio('sound','tick.ogg')
            self.sound = True
            
    def unselect(self):
        self.highlited = False
        self.sound = False
        self.image = self.font.render(self.label, 1, GRAY)
        
    def set_label(label):
        self.image = self.font.render(label, 1, GRAY)
    
    def set_pos(x,y):
        self.rect.move(x,y)
class MenuBox(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        
        #i bottoni vengono inseriti con le coordinate
        self.new_game = Button('New Game',(300,200))
        self.exit_game = Button('Exit Game',(300,250))
        self.continue_game = Button('Continue Game',(300,300))
        
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.new_game)
        self.buttons.add(self.exit_game)
        self.buttons.add(self.continue_game)
        
    def update(self):
        #chiama a sua volta il metodo update di "Widget.Button"
        self.new_game.update()
        self.exit_game.update()
        self.continue_game.update()
