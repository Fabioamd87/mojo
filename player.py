"""Welcome to mojo, music by Frozen Silence, Electric Zoom, Bang Bong """

import sys
import os
import pygame
import string

import functions

class Player(pygame.sprite.Sprite):
    def __init__(self, filename, altezza, larghezza, num):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = functions.carica_imm_sprite('character',filename,altezza,larghezza,num)
        self.image = self.images[0]
        
        self.rect = self.image.get_rect()
        #self.rect = self.rect.move(0, 280)
        
        self.maxframe = len(self.images)

        self.frame_corrente = 0        
        self.width=50
        self.height=150
        
        self.is_moving = False
        self.talking = False
        self.x_direction = 0
        
        self.clock = pygame.time.Clock()
        
        self.name = 'tu'
        
    def update(self):
        """gestisce la velocita di movimento"""
        if self.is_moving:
            if (self.rect[0]+self.width/2)<self.x_direction:
                self.is_moving = True
                self.movedx()

            if (self.rect[0]+self.width/2)>self.x_direction:
                self.is_moving = True
                self.movesx()
        else:
            self.is_moving = False
        
    def collide(self, sprite):
        if self.rect.colliderect(sprite.rect):
            return true
            
    def position(self,x,y):
        self.rect.topleft = (x, y)
        self.x_direction = x
        self.is_moving = False

    def walkto(self,direction):
        if self.x_direction != direction[0]:
            self.is_moving=True
            self.x_direction = direction[0]

    def movedx(self):
        #attualmente il numero massimo di frame e' specificato manualmente        
        self.animate()
        self.rect = self.rect.move(10, 0)
        
        if abs(self.x_direction - (self.rect[0]+self.width/2)) < 10:
            self.is_moving=False
            self.turn_right()

    def animate(self):
        if self.frame_corrente < 2:
            self.frame_corrente += 1
            self.image=self.images[self.frame_corrente]
        else:
            self.frame_corrente = 0
            self.image=self.images[self.frame_corrente]

    def movesx(self):
            #attualmente il numero massimo di frame e' specificato manualmente
            if self.frame_corrente < 5:
                self.frame_corrente += 1
                self.image=self.images[self.frame_corrente]
            else:
                self.frame_corrente = 3
                self.image=self.images[self.frame_corrente]                
            self.rect = self.rect.move(-10, 0)
            
            if abs(self.x_direction - (self.rect[0]+self.width/2)) < 10:
                self.is_moving=False
                self.turn_left()
   
    def turn_right(self):
        """volta a destra"""
        self.image=self.images[1] #il frame che guarda a destra
    
    def turn_left(self):
        """volta a sinistra"""
        self.image=self.images[5] #il frame che guarda a sinistra
