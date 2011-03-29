import pygame
from ConfigParser import RawConfigParser
import Functions

class Scenario(pygame.sprite.Sprite):
    def __init__(self):

        self.objects = pygame.sprite.Group()
        self.areas = pygame.sprite.Group()
        self.people = pygame.sprite.Group()
        self.text_in_game = pygame.sprite.Group()

        self.background = Background()        
        self.textbox = TextOnScreen()
        
        self.text_in_game.add(self.textbox,self.textbox.e,self.textbox.p,self.textbox.t)

    def load_homemade(self,destination):
        with open(destination + '.txt') as f:
            for line in f:
                if line[0:10] == 'background':
                    background = line[13:len(line)-1]
                    print 'background: ' + background
                    self.background.image = Functions.load_image('background',background)
                if line[0:5] == 'music':
                    music = line[8:len(line)-1]
                    print 'music: ' + music
                    self.music = Functions.play_audio('music',music)
                if line[0:5] == '[rects]':
                    while line[0]=='[':
                        print line.readlines()
                    

    def load(self,destination):
        """ non adatto, lo usero per leggere un eventuale configurazione """
        self.objects.empty()
        self.areas.empty()
        self.people.empty()
        config = RawConfigParser()
        config.read(destination + '.txt')
        self.scene_name = config.get('Info', 'name')
        print 'scene name: ' + self.scene_name
        
        background = config.get('Info', 'background')
        self.background.image = Functions.load_image('background',background)
        print 'background: ' + background
        
        music = config.get('Info', 'music')
        self.music = Functions.play_audio('music',music)
        
        """ dovrebbe instanziare n_of_rect oggetti di tipo Scenario.Rect e inserirli nel gruppo rects"""
        #load rects
        for line in config.items('Areas'):
            name = line[0]
            values = line[1].split(' ')
            rect = values[0]
            destination = values[1]
            rect = Area(name,rect,destination)
            self.areas.add(rect)
        #load objects
        for line in config.items('Objects'):
            name = line[0]
            values = line[1].split(' ')
            rect = values[0]
            destination = values[1]
            rect = Area(name,rect,destination)
            self.areas.add(rect)
            

    def playmusic(self):
        """Stream music with mixer.music module in blocking manner.
        This will stream the sound from disk while playing.
        """

        clock = pygame.time.Clock()
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
        #   clock.tick(FRAMERATE)


class Area(pygame.sprite.Sprite):
    def __init__(self,name,rect,dest):
        pygame.sprite.Sprite.__init__(self)        
        self.name = name
        self.destination = dest
        
        lista = rect.split(',')
        # i suck in making for cicles
        lista[0]=int(lista[0])
        lista[1]=int(lista[1])
        lista[2]=int(lista[2])
        lista[3]=int(lista[3])
        self.rect = pygame.Rect(lista)
        
class Object(pygame.sprite.Sprite):
    def __init__(self,name,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('beer.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.name = name
        
        self.view_text = ''
        self.take_text = ''
        self.talk_text = ''
        
        #self.raggiungibile #indica se raggiungibile quando clicco su esamina
    def on_view(self):
        print self.view_text
    def on_take(self):
        print self.take_text
    def on_talk(self):
        print self.talk_text
        
class Background(pygame.sprite.Sprite):
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        
    def load(self,actual):
        with open("intro.txt") as f:
            for line in f:
                print line[0:10]
                if line[0:10] == 'background':
                    background = line[13:len(line)-1]
                    self.image = Functions.load_image('background',background)
                    print 'background: ' + background

class TextOnScreen(pygame.sprite.Sprite):
    """riporta i nomi degli oggetti che collidono col puntatore"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(512,0,0,0)
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("", 1, (10, 10, 10))
        self.item = False
        self.visible = False
        self.name_settable = True
        self.calcolable = True
        self.e = self.action("esamina")
        self.p = self.action("prendi")
        self.t = self.action("parla")
        
    def pointer_collide(self,pointergroup,objects,rects):
        pointer = pointergroup.sprites()[0]
        if self.name_settable:
            if Functions.collide(pointer,objects): #collide con un oggetto 
                obj=Functions.collide(pointer,objects) #forse meglio non usare funzioni proprie
                self.text = self.font.render(obj.name, 1, (10, 10, 10))
                self.visible = True
            elif Functions.collide(pointer,rects): #collide con una rect
                rect=Functions.collide(pointer,rects)
                self.text = self.font.render(rect.name, 1, (10, 10, 10))
                self.visible = True
            else:
                self.text = self.font.render("", 1, (10, 10, 10))
                self.visible = False
        else:
            return False
            
    def set_name(self,item):
        """associa le azioni al nome dell'oggetto"""
        self.item = item
        
    def calcola_posizione_box(self):
        if self.calcolable: #ovvero abbiamo rilasciato il mouse
            mouse_pos = pygame.mouse.get_pos()
            self.e.rect.topleft=mouse_pos[0],mouse_pos[1]+40
            self.p.rect.topleft=mouse_pos[0]+40,mouse_pos[1]-40
            self.t.rect.topleft=mouse_pos[0]-40,mouse_pos[1]-40
    
    def select(self,pointer):
        """controlla se selezioniamo un azione"""
        if self.item: #esiste un oggetto che collide
            if pygame.sprite.collide_rect(pointer, self.e):
                self.visible = True
                self.e.highlited = True
                self.e.text = self.e.font.render("esamina", 1, (255, 255, 10))
                self.text = self.font.render("esamina " + self.item.name, 1, (10, 10, 10))
            else:
                self.e.highlited = False
                self.e.text = self.e.font.render("esamina", 1, (10, 10, 10))
            if pygame.sprite.collide_rect(pointer, self.p):
                self.visible=True
                self.p.highlited = True
                self.p.text = self.p.font.render("prendi", 1, (255, 255, 10))
                self.text = self.font.render("prendi " + self.item.name, 1, (10, 10, 10))
            else:
                self.p.highlited = False
                self.p.text = self.p.font.render("prendi", 1, (10, 10, 10))    
            if pygame.sprite.collide_rect(pointer, self.t):
                self.visible=True
                self.t.highlited = True
                self.t.text = self.t.font.render("parla", 1, (255, 255, 10))
                self.text = self.font.render("parla con " + self.item.name, 1, (10, 10, 10))
            else:
                self.t.highlited = False
                self.t.text = self.t.font.render("parla", 1, (10, 10, 10))
            
    def on_click_released(self):
        if self.e.highlited == True:
            self.item.on_view()#lo specifico sotto, ma va nell'apposito metodo
            birra = pygame.mixer.Sound('beer_view.ogg')
            birra.play()
        if self.p.highlited == True:
            self.item.on_take()
            birra = pygame.mixer.Sound('beer_take.ogg')
            birra.play()
        if self.t.highlited == True:
            self.item.on_talk()
            birra = pygame.mixer.Sound('beer_talk.ogg')
            birra.play()
    
    def hide(self):
        for i in self.e,self.p,self.t:
            i.visible=False

    def show(self):
        for i in self.e,self.p,self.t:
            i.visible=True
    
    class action(pygame.sprite.Sprite):
        def __init__(self,name):
            pygame.sprite.Sprite.__init__(self)
            pygame.font.init()
            self.visible = False
            self.highlited = False
            
            #pygame.font.Font.size(name): return (width, height)
            self.rect = pygame.Rect(0, 0, 50, 20)
            self.font = pygame.font.Font(None, 36)
            self.text = pygame.Surface(self.font.size(name))
            self.text.fill((0,0,0))#
            pygame.gfxdraw.rectangle(self.text, self.rect, (10,10,10))#
            self.text = self.font.render(name, 1, (10, 10, 10))
            #il codice su dovrebbe fare un box, colorarlo contornarlo e scriverci, ma non lo fa'!
