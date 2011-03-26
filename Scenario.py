import pygame
from ConfigParser import RawConfigParser

class Scenario(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('background1.jpg').convert()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.iniFile = ('data.ini')
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
               

