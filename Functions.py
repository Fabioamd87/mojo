import os, sys
import pygame
from pygame.locals import *

"""
FUNZIONI DI BASE

"""

def load_image(imagetype, name, colorkey=None):
    if imagetype == 'pointer':
        fullname = os.path.join('data/imgs', name)
    if imagetype == 'character':
        fullname = os.path.join('data/imgs/characters', name)
    if imagetype == 'background':
        fullname = os.path.join('data/imgs/backgrounds', name)
    if imagetype == 'object':
        fullname = os.path.join('data/imgs/objects', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    if imagetype == 'pointer':
        return image, image.get_rect()
    else:
        return image

def play_audio(audiotype, name):
    if audiotype == 'music':
        fullname = os.path.join('data/audio/musics', name)
    if audiotype == 'voice':
        fullname = os.path.join('data/audio/voices', name)

    clock = pygame.time.Clock()
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.play()

#forse non dovrei usare questa funzione ma una built-in degli sprite
def collide(obj, objects):
    sprite=pygame.sprite.spritecollideany(obj,objects)
    if sprite:
        return sprite #ritorna uno sprite, forse.
    else:
        return False
