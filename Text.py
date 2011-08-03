import pygame

#from ConfigParser import RawConfigParser

import Functions
import Inventory
import GameElements

BLACK = (10,10,10)
YELLOW = (255, 255, 10)

class TextOnScreen(pygame.sprite.Sprite):
    """
        riporta i nomi degli oggetti che collidono col puntatore
        questa classe è istanziata col nome di textbox nel file scenario,
        migliorare questa cosa
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #testo in alto
        self.rect = pygame.Rect(512,0,0,0)
        self.font = pygame.font.Font(None, 25)
        self.text = self.font.render("", 1, (10, 10, 10))
        
        #self.name_settable = True
        self.item = False # True se il mouse collide con un oggetto
        self.visible = False #lo stato del testo descrittivo in alto
        self.calcolable = True #la posizione non e' piu' calcolabile quando teniamo premuto il destro
        self.menuVisible = False #la visibilita' del menu delle azioni
                
        #texto del box di interazione
        #(in precedenza chiamati self.e, self.p, self.t)
        self.examine = self.action("esamina")
        self.take = self.action("prendi")
        self.talk = self.action("parla")   
        
        #parlato personaggio
        self.speak = self.SpeakBox()
        
        #gestione dialoghi
        self.line1 = self.DialogueBox()
        
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
            
            """debug sul tipo di oggetto collidente
            if sprite.Type == 'object':
                print 'oggetto'
            if sprite.Type == 'direction':                
                print 'direzione'
            if sprite.Type == 'character':
                print 'personaggio'
            """
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
        """controlla se selezioniamo un azione"""
        self.examine.select(pointergroup)
        self.take.select(pointergroup)
        self.talk.select(pointergroup)

        if self.examine.highlited:
            self.write("esamina " + name)
            
        if self.take.highlited:
            self.write("prendi " + name)
            
        if self.talk.highlited:
            self.write("parla con " + name)
        
        if self.examine.highlited == self.take.highlited == self.talk.highlited == False:
            self.write(name)
    
    class action(pygame.sprite.Sprite):
        def __init__(self,name):
            pygame.sprite.Sprite.__init__(self)
            self.font = pygame.font.Font(None, 25)
            
            self.visible = False
            self.highlited = False
            
            self.ActionName = name
            
            self.rect = pygame.Rect((0,0),self.font.size(name))
            self.text = self.font.render(name, 1, BLACK)
        
        def select(self,pointergroup):
            """evidenzia l'opzione scelta"""            
            if pygame.sprite.pygame.sprite.spritecollideany(self,pointergroup):
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
            
        def Write(self,text):
            self.rect = pygame.Rect((0,0),self.font.size(text))
            self.text = self.font.render(text, 1, (10, 10, 10))
