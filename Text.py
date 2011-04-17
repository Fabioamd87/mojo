import pygame

#from ConfigParser import RawConfigParser

import Functions
import Inventory
import GameElements

class TextOnScreen(pygame.sprite.Sprite):
    """riporta i nomi degli oggetti che collidono col puntatore"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.rect = pygame.Rect(512,0,0,0)
        self.font = pygame.font.Font(None, 24)
        self.text = self.font.render("", 1, (10, 10, 10))
        
        self.name_settable = True
        self.item = False # True se il mouse collide con un oggetto
        self.visible = False 
        self.calcolable = True #la posizione non e' piu' calcolabile quando teniamo premuto il destro
        self.menuVisible = False
        
        self.e = self.action("esamina")
        self.p = self.action("prendi")
        self.t = self.action("parla")
        
    def pointer_collide(self,pointergroup,objects,rects):

        pointer = pointergroup.sprites()[0]
        if self.name_settable:
            if Functions.collide(pointer,objects): #collide con un oggetto
                self.obj = Functions.collide(pointer,objects) #forse meglio non usare funzioni proprie
                self.write(self.obj.name)
                self.visible = True
                self.item = True                
            elif Functions.collide(pointer,rects): #collide con una rect
                rect=Functions.collide(pointer,rects)
                self.write(rect.name)
                self.visible = True
            else:
                self.write('')
                self.item = False
        elif self.menuVisible == False:
            self.visible = False
    
    def write(self,text):
        self.text = self.font.render(text, 1, (10, 10, 10))
            
    def hide(self):
        for i in self.e,self.p,self.t:
            i.visible=False
        self.menuVisible = False

    def show(self):
        for i in self.e,self.p,self.t:
            i.visible=True
        self.menuVisible = True
            
    def set_name(self,item):
        """associa le azioni al nome dell'oggetto"""
        self.item_name = item
        self.item = True
        
    def calcola_posizione_box(self):
        if self.calcolable: #ovvero abbiamo rilasciato il mouse
            pos = pygame.mouse.get_pos()
            self.e.rect.topleft=pos[0],pos[1]+40
            self.p.rect.topleft=pos[0]+40,pos[1]-40
            self.t.rect.topleft=pos[0]-40,pos[1]-40
    
    def select(self,pointergroup):
        """controlla se selezioniamo un azione"""
        
        if self.item and self.menuVisible: #esiste un oggetto che collide
            self.e.select(pointergroup,self.item_name)
            self.p.select(pointergroup,self.item_name)
            self.t.select(pointergroup,self.item_name)
            
            if self.e.highlited:
                self.write("esamina " + self.item_name)
            elif self.p.highlited:
                self.write("prendi " + self.item_name)
            elif self.t.highlited:
                self.write("parla con " + self.item_name)
            else:
                self.write(self.obj.name)
            
    def DoThings(self):
        if self.e.highlited == True:
            self.obj.on_view()#lo specifico sotto, ma va nell'apposito metodo
        if self.p.highlited == True:
            self.obj.on_take()
        if self.t.highlited == True:
            self.obj.on_talk()
    
    class action(pygame.sprite.Sprite):
        def __init__(self,name):
            pygame.sprite.Sprite.__init__(self)
            pygame.font.init()
            self.visible = False
            self.highlited = False
            self.font = pygame.font.Font(None, 36)
            self.ActionName = name
            
            self.rect = pygame.Rect((0,0),self.font.size(name))
            self.text = self.font.render(name, 1, (10, 10, 10))
        
        def select(self,pointergroup,item_name):
            if pygame.sprite.pygame.sprite.spritecollideany(self,pointergroup):
                self.highlited = True
                self.text = self.font.render(self.ActionName, 1, (255, 255, 10))
            else:
                self.highlited = False
                self.text = self.font.render(self.ActionName, 1, (10, 10, 10))
