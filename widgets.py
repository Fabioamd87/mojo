import pygame

import functions
import game_elements
import events

BLACK = (10,10,10)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
YELLOW = (255, 255, 10)

class Interface(pygame.sprite.Sprite):
    """contenitore di tutti i widgets"""
    def __init__(self):
        pygame.font.init()
        self.widgets = []
        
    def add_widget(self, widget):
        "aggiunge un widget all'interfaccia"
        self.widgets.append(widget)
        
    def remove_widget(self, widget):
        pass

    def update(self,event):
        for i in self.widgets:
            i.update(event)

    def draw(self, screen):
        for i in self.widgets:
            i.draw(screen)

class Button(pygame.sprite.Sprite):
    """generico bottone"""
    def __init__(self,label='Button', pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)

        self.label = label
        self.font = pygame.font.Font(None, 36)
        #rect a dimensione del testo
        self.rect = pygame.Rect(pos,self.font.size(self.label))
        self.image = self.font.render(label, 1, GRAY)
        
        self.visible = True        
        self.highlited = False
        self.sound = False

        self.left_click_event = None
        self.right_click_event = None

    def OnLeftClick(self, event):
        self.left_click_event = event

    def OnRightClick(self, event):
        self.right_click_event = event

    def update(self,event):   
        #passing event is necessary for better handling mouse actions     
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.select()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.__dict__['button'] == 1:
                    if self.left_click_event:
                        pygame.event.post(self.left_click_event)
                if event.__dict__['button'] == 3:
                    if self.right_click_event:
                        pygame.event.post(self.right_click_event)
        else:
            self.unselect()
    
    def select(self):
        self.highlited = True
        self.font.set_italic(1)
        self.image = self.font.render(self.label, 1, RED)
        if self.sound == False:
            functions.play_audio('sound','tick.ogg')
            self.sound = True
        match self.label:
            case 'examine':
                pygame.event.post(events.EXAMINE_SELECTED)
            case 'take':
                pygame.event.post(events.TAKE_SELECTED)
            case 'talk':
                pygame.event.post(events.TALK_SELECTED)      

    def unselect(self):
        self.highlited = False
        self.font.set_italic(0) 
        self.image = self.font.render(self.label, 1, GRAY)
        self.sound = False
        
    def set_label(self,label):
        self.label = label
        self.image = self.font.render(self.label, 1, GRAY)
    
    def set_pos(self,x,y):
        self.rect.move(x,y)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
class Label(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #testo in alto
        self.font = pygame.font.Font(None, 36)        
        self.image = self.font.render('None', 1, BLACK)
        self.rect = pygame.Rect(256,0,0,0)
        self.font = pygame.font.Font(None, 25)            
        self.visible = False
    
    def set_label(self, label):
        self.label = label
        self.image = self.font.render(self.label, 1, GRAY)
        
    def set_visible(self):
        self.visible = True

    def set_invisible(self):
        self.visible = False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class TopText(pygame.sprite.Sprite):
    #highlated object description on top
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = Label()
    
    def draw(self, screen):
        if self.text.visible:
            self.text.draw(screen)

    def show(self):
        self.text.set_visible()

    def hide(self):
        self.text.set_invisible()

    def set_label(self, label):
        self.text.set_label(label)

class ActionMenu():
    #instanciated in Element class, init  method
    def __init__(self):
        self.examine = Button('examine')
        self.take = Button('take')
        self.talk = Button('talk')

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.examine, self.take, self.talk)
        
        self.visible = False
        self.moveable = True
        
        self.sprite_name = None #lo chiede all'inizio, per aprire il menu
    
    def update(self, event):
        self.update_position()
        if self.visible == True:
            self.examine.update(event)
            self.take.update(event)
            self.talk.update(event)   
    
    def open_menu(self, name):
        self.sprite_name = name
        self.show()
        self.moveable = False

    def close_menu(self, name):
        if self.visible:
            if self.examine.highlited:
                print('examine', name)
                pygame.event.post(events.EXAMINE)
            if self.take.highlited:
                print('take', name)
                pygame.event.post(events.TAKE)
            if self.talk.highlited:
                print('talk to', name)
                pygame.event.post(events.TALK)                   
        self.hide()
        self.moveable = True
    
    def hide(self):
        for i in self.examine, self.take, self.talk:
            i.visible = False
        self.visible = False

    def show(self):
        for i in self.examine,self.take,self.talk:
            i.visible=True
        self.visible = True
    
    def update_position(self):
        """questo metodo calcola la posizione del menu delle azioni"""
        if self.moveable:
            pos = pygame.mouse.get_pos()
            self.examine.rect.topleft = pos[0]-25, pos[1]+30
            self.take.rect.topleft = pos[0]+30, pos[1]-30
            self.talk.rect.topleft = pos[0]-50, pos[1]-30