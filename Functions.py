import os, sys
import pygame
from pygame.locals import *

"""
FUNZIONI DI BASE

"""

def load_image(name, colorkey=None):                    # prende una stringa in input e carica un'immagine da
    fullname = os.path.join('data/imgs', name)            # data/imgs
    try:                                                 # restuisce un'immagine e un rect
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

#forse non dovrei usare questa funzione ma una built-in degli sprite
def collide(obj, objects):
    sprite=pygame.sprite.spritecollideany(obj,objects)
    if sprite:
        return sprite #ritorna uno sprite, forse.
    else:
        return False

"""
def draw_background(screen, img_filename):              #stampa un background utilizzando tiles se necessario
    tile_img, img_rect = load_image(img_filename)
    nrows = int(screen.get_height() / img_rect.height) + 1
    ncols = int(screen.get_width() / img_rect.width) + 1
    for y in range(nrows):
        for x in range(ncols):
            img_rect.topleft = (x * img_rect.width, y * img_rect.height)
            screen.blit(tile_img, img_rect)
"""
