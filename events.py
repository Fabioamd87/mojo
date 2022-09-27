import pygame

a=3

START_GAME = pygame.event.Event(pygame.USEREVENT+1,{'subcat':0,'destination':'intro'})
CONTINUE_GAME = pygame.event.Event(pygame.USEREVENT+1,{'subcat':0,'destination':'continue'})

EXAMINE = pygame.event.Event(pygame.USEREVENT+2,{'action':'examine','event':'clicked'})
TAKE = pygame.event.Event(pygame.USEREVENT+2,{'action':'take','event':'clicked'})
TALK = pygame.event.Event(pygame.USEREVENT+2,{'action':'talk','event':'clicked'})

EXAMINE_SELECTED = pygame.event.Event(pygame.USEREVENT+2,{'action':'examine','event':'selected'})
TAKE_SELECTED = pygame.event.Event(pygame.USEREVENT+2,{'action':'take','event':'selected'})
TALK_SELECTED = pygame.event.Event(pygame.USEREVENT+2,{'action':'talk','event':'selected'})