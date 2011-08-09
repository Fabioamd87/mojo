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
        Questa classe è istanziata col nome di textbox nel file scenario,
        migliorare questa cosa
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #testo in alto
        self.rect = pygame.Rect(512,0,0,0)
        self.font = pygame.font.Font(None, 25)
        self.text = self.font.render("", 1, (10, 10, 10))
        
        """il testo in alto dovrebbe essere una classe separata come le altre"""
        #self.name_settable = True
        self.item = False # True se il mouse collide con un oggetto
        self.visible = False #lo stato del testo descrittivo in alto
        self.calcolable = True #la posizione non e' piu' calcolabile quando teniamo premuto il destro
        self.menuVisible = False #la visibilita' del menu delle azioni
                
        #texto del box di interazione
        #(in precedenza chiamati self.e, self.p, self.t)
        self.examine = self.Action("esamina")
        self.take = self.Action("prendi")
        self.talk = self.Action("parla")   
        
        #parlato personaggio
        self.speak = self.SpeakBox()
        
        #gestione dialoghi
        self.line1 = self.DialogueBox()
        
        #descrozopme oggetti
        self.toptext = self.DescriptionBox()
        
    def update(self,pointergroup,game_elements):
        self.toptext.show_name(pointergroup,game_elements,self.menuVisible)
    
    def show_name(self,pointergroup,group):
        """cattura l'oggetto con cui il mouse collide
           scrive in alto il nome, rendendo visibile il testo
           imposta la presenza di un oggetto che collide"""        
        pointer = pointergroup.sprites()[0]                        
        sprite = pygame.sprite.spritecollideany(pointer,group)
        
        if sprite:
            self.sprite = sprite
            self.write(self.sprite.name)
            self.visible = True

        elif self.menuVisible == True:
            self.visible = True
        else:
            self.visible = False
        
    def write(self,text):
        self.text = self.font.render(text, 1, BLACK)
            
    def hide_menu(self):
        for i in self.examine,self.take,self.talk:
            i.visible=False
        self.menuVisible = False

    def show_menu(self):
        for i in self.examine,self.take,self.talk:
            i.visible=True
        self.menuVisible = True
        
    def calcola_posizione_box(self,player_pos):
        """questo metodo calcola la posizione del menu delle azioni"""
        if self.calcolable: #ovvero abbiamo rilasciato il mouse
            pos = pygame.mouse.get_pos()
            self.examine.rect.topleft=pos[0]-25,pos[1]+30
            self.take.rect.topleft=pos[0]+30,pos[1]-30
            self.talk.rect.topleft=pos[0]-50,pos[1]-30
        #dove appare cio che viene detto dal personaggio
        self.speak.rect.topleft = player_pos[0]+50,player_pos[1]-30 #raffinare
    
    def select(self,pointergroup,name):
        """controlla se selezioniamo un azione
            mostra in alto la descrizione"""
        self.examine.select(pointergroup)
        self.take.select(pointergroup)
        self.talk.select(pointergroup)

        if self.examine.highlited:
            self.write("esamina " + name)
            
        if self.take.highlited:
            self.write("prendi " + name)
            
        if self.talk.highlited:
            self.write("parla con " + name)
    
    class Action(pygame.sprite.Sprite):
        def __init__(self,name):
            pygame.sprite.Sprite.__init__(self)
            self.font = pygame.font.Font(None, 25)
            
            self.visible = False
            self.highlited = False
            
            self.ActionName = name
            
            self.rect = pygame.Rect((0,0),self.font.size(name))
            self.text = self.font.render(name, 1, BLACK)
            
        def collide(self,pointergroup):
            if pygame.sprite.pygame.sprite.spritecollideany(self,pointergroup):
                return True
            else:
                return False
        
        def select(self,pointergroup):
            """evidenzia l'opzione scelta"""            
            if self.collide(pointergroup):
                self.highlited = True
                self.font.set_italic(1)
                self.text = self.font.render(self.ActionName, 1, YELLOW)
            else:
                self.highlited = False
                self.font.set_italic(0)
                self.text = self.font.render(self.ActionName, 1, BLACK)
                
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
            self.text = self.font.render("prova", 1, (10, 10, 10))
            
            self.visible = True
        
        def show_name(self,pointergroup,game_elements,menuVisible):
            """cattura l'oggetto con cui il mouse collide
           scrive in alto il nome, rendendo visibile il testo
           imposta la presenza di un oggetto che collide"""        
            pointer = pointergroup.sprites()[0]                        
            sprite = pygame.sprite.spritecollideany(pointer,game_elements)
            
            if sprite:
                self.sprite = sprite
                self.write(self.sprite.name)
                self.visible = True
            #non deve essere mostrato se e' aperto il menu
            elif menuVisible == True:
                self.visible = True
            else:
                self.visible = False
            
        def write(self,text):
                self.text = self.font.render(text, 1, BLACK)
