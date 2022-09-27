import os, sys
import pygame
from pygame.locals import *


"""
FUNZIONI DI BASE

"""

def carica_imm_sprite(imagetype,filename,h,w,num):
	immagini = []
	if num is None or num == 1:
		imm1 =  load_image(imagetype,filename)
		imm1_w, imm1_h = imm1.get_size()
	
		for y in range(int(imm1_h/h)):
			for x in range(int(imm1_w/w)):
				immagini.append(imm1.subsurface((x*w,y*h,w,h)))	
		return immagini
	else:
		for x in range(1,num):
			imm1 = pygame.image.load(filename+str(x)+".png").convert_alpha()
			immagini.append(imm1)
		return immagini

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
        print('loading: ' + fullname)
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image: ', name)
        raise SystemExit(message)
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
    if audiotype == 'sound':
        fullname = os.path.join('data/audio/sounds', name)
    if audiotype == 'music':
        pygame.mixer.music.load(fullname)
        pygame.mixer.music.play()
    else:
        snd = pygame.mixer.Sound(fullname)
        snd.play()
