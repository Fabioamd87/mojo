import pygame

#from ConfigParser import RawConfigParser

import Functions
import Inventory
import GameElements

BLACK = (10,10,10)
YELLOW = (255, 255, 10)

class TextOnScreen(pygame.sprite.Sprite):
    """riporta i nomi degli oggetti che collidono col puntatore"""
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
        self.e = self.action("esamina")
        self.p = self.action("prendi")
        self.t = self.action("parla")
        
        #parlato personaggio
        self.speak = self.SpeakBox()
        
        #gestione dialoghi
        self.line1 = self.DialogueBox()
        
    def show_name(self,pointergroup,group):
        """salva l'oggetto con cui il mouse collide
           scrive in alto il nome, rendendo visibile il testo
           imposta la presenza di un oggetto che collide"""
        
        pointer = pointergroup.sprites()[0]
                        
        sprite = pygame.sprite.spritecollideany(pointer,group)
        
        if sprite:
            self.sprite = sprite
            self.write(self.sprite.name)
            self.visible = True
            if sprite.Type == 'object':
                print 'oggetto'
            if sprite.Type == 'direction':                
                print 'direzione'
            if sprite.Type == 'character':
                print 'personaggio'
                
        elif self.menuVisible == True:
            self.visible = True
        
        else:
            self.visible = False
        
    def write(self,text):
        self.text = self.font.render(text, 1, BLACK)
            
    def hide_menu(self):
        for i in self.e,self.p,self.t:
            i.visible=False
        self.menuVisible = False

    def show_menu(self):
        for i in self.e,self.p,self.t:
            i.visible=True
        self.menuVisible = True
        
    def calcola_posizione_box(self,player_pos):
        """questo metodo calcola la posizione del menu delle azioni"""
        if self.calcolable: #ovvero abbiamo rilasciato il mouse
            pos = pygame.mouse.get_pos()
            self.e.rect.topleft=pos[0]-25,pos[1]+30
            self.p.rect.topleft=pos[0]+30,pos[1]-30
            self.t.rect.topleft=pos[0]-50,pos[1]-30
        #dove appare cio che viene detto dal personaggio
        self.speak.rect.topleft = player_pos[0]+50,player_pos[1]-30 #raffinare
    
    def select(self,pointergroup,name):
        """controlla se selezioniamo un azione"""
        self.e.select(pointergroup)
        self.p.select(pointergroup)
        self.t.select(pointergroup)

        if self.e.highlited:
            self.write("esamina " + name)
            
        if self.p.highlited:
            self.write("prendi " + name)
            
        if self.t.highlited:
            self.write("parla con " + name)
        
        if self.e.highlited == self.p.highlited == self.t.highlited == False:
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
                        
        def Write(self,text):
            self.rect = pygame.Rect((0,0),self.font.size(text))
            self.text = self.font.render(text, 1, (10, 10, 10))
    
    class DialogueBox(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)            
            self.font = pygame.font.Font(None, 25)
            
            self.highlited = False
            self.visible = False
            self.rect = pygame.Rect(20,400,0,0)
            self.text = self.font.render('aaaa', 1, (10, 10, 10))
            
        def Write(self,text):
            self.rect = pygame.Rect((0,0),self.font.size(text))
            self.text = self.font.render(text, 1, (10, 10, 10))
