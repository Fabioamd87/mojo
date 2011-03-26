import pygame
from ConfigParser import RawConfigParser

class Scenario(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('background1.jpg').convert()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.iniFile = ('data.ini')
        
        objects = pygame.sprite.Group()
        rects = pygame.sprite.Group()
        people = pygame.sprite.Group()
        
        self.load_data()
    
    def load_data(self):
        config = RawConfigParser()
        config.read('data.ini')
        self.scene_name = config.get('Info', 'name')
        self.background = config.get('Images', 'background')

    def load_scene(self,scene):
        self.image = pygame.image.load(scene+'.jpg').convert()
        
    def playmusic(self):
        """Stream music with mixer.music module in blocking manner.
        This will stream the sound from disk while playing.
        """

        clock = pygame.time.Clock()
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
        #   clock.tick(FRAMERATE)
               
class Rect(pygame.sprite.Sprite): #dovrebbe indicare anche dove porta
    def __init__(self,name,rect,dest):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)
        self.name = name
        self.destination=dest
        
class Object(pygame.sprite.Sprite):
    def __init__(self,name,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('beer.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft=pos
        self.name = name
        #self.raggiungibile #indica se raggiungibile quando clicco su esamina
    def on_view(self):
        print "e' un oggetto davvero bello"
        #pygame.mixer.Sound('beer_view.ogg').play
    def on_take(self):
        print "non posso prenderlo"
    def on_talk(self):
        print "ciao oggetto, come va?"
