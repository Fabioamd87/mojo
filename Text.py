import pygame

#from ConfigParser import RawConfigParser

import Functions
import Inventory
import GameElements

BLACK = (10,10,10)
YELLOW = (255, 255, 10)

class TextOnScreen(pygame.sprite.Sprite):
    """
        classe che contiene tutti gli elementi di testo del gioco.

        Questa classe e' istanziata col nome di textbox nel file scenario,

        migliorare questa cosa
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #testo in alto
        #self.rect = pygame.Rect(512,0,0,0)
        #self.font = pygame.font.Font(None, 25)
        #self.text = self.font.render("", 1, (10, 10, 10))
        
        #self.name_settable = True
        #self.item = False # True se il mouse collide con un oggetto
        #self.visible = False #lo stato del testo descrittivo in alto
        #self.calcolable = True #la posizione non e' piu' calcolabile quando teniamo premuto il destro
        #self.menuVisible = False #la visibilita' del menu delle azioni
        
        """        
        #texto del box di interazione
        #(in precedenza chiamati self.e, self.p, self.t)
        self.examine = self.Action("esamina")
        self.take = self.Action("prendi")
        self.talk = self.Action("parla")   
        """
        
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
            
        pointer = pointergroup.sprites()[0]
        self.sprite = pygame.sprite.spritecollideany(pointer,game_elements)
        
        self.menu.calcola_posizione_box()

        if self.sprite:
            self.toptext.show_name(self.sprite)
            
        else: self.toptext.visible = False
        
        self.menu.update(pointergroup,self.sprite)
        
        #self.toptext.show_name(pointergroup,game_elements,self.menu.visible)
        
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
            self.menuVisible = False

        def show(self):
            for i in self.examine,self.take,self.talk:
                i.visible=True
            self.menuVisible = True
        
        def calcola_posizione_box(self):
            """questo metodo calcola la posizione del menu delle azioni"""
            if self.moveable: #ovvero abbiamo rilasciato il mouse
                pos = pygame.mouse.get_pos()
                self.examine.rect.topleft=pos[0]-25,pos[1]+30
                self.take.rect.topleft=pos[0]+30,pos[1]-30
                self.talk.rect.topleft=pos[0]-50,pos[1]-30
    
        def update(self,pointergroup, sprite):
            """controlla se selezioniamo un azione
                mostra in alto la descrizione"""
            if sprite:
                self.sprite = sprite
            if self.visible == True:
                self.examine.check_selection(pointergroup)
                self.take.check_selection(pointergroup)
                self.talk.check_selection(pointergroup)

            # secondo l'approccio MVC questo va nella view
            """
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
                
            def collide(self,pointergroup):
                #quando il mouse non collide con l'oggetto non viene piu fatto il controllo
                if pygame.sprite.pygame.sprite.spritecollideany(self,pointergroup):
                    return True
                else:
                    return False
            
            def check_selection(self,pointergroup):
                #controlla, ma solo se il menu è stato aperto
                
                if self.collide(pointergroup):
                    self.select()
                else:
                    self.unselect()
            
            def select(self):
                """evidenzia l'opzione scelta"""
                self.highlited = True
                self.font.set_italic(1)
                self.label = self.font.render(self.label, 1, YELLOW)
                
            def unselect(self):
                """annulla la selezione"""
                self.highlited = False
                self.font.set_italic(0)
                self.label = self.font.render(self.label, 1, BLACK)
                
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
            #self.text = self.font.render("prova", 1, (10, 10, 10))
            
            self.visible = True
        
        def show_name(self,sprite):
            """cattura l'oggetto con cui il mouse collide
           scrive in alto il nome, rendendo visibile il testo
           imposta la presenza di un oggetto che collide"""        
                                    
            
            #lo sprite catturato, dove va?
            #sprite = pygame.sprite.spritecollideany(pointer,game_elements)
            
            #if sprite:
                #self.sprite = sprite
            self.write(sprite.name)
            self.visible = True
            #non deve essere mostrato se e' aperto il menu
            """
            elif menuVisible:
                self.visible = True
            else:
                self.visible = False
            """
        def write(self,text):
            self.text = self.font.render(text, 1, BLACK)
            
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
                
