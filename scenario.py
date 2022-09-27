import pygame
import sqlite3
from configparser import RawConfigParser

import functions
import inventory
import game_elements
import widgets
import state
import events

class Scenario(pygame.sprite.Sprite):
    def __init__(self):
        
        #object selected by the pointer
        self.seleted = False

        self.objects_in_game = pygame.sprite.Group()
        self.directions = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.text_in_game = pygame.sprite.Group()

        #insieme di tutti gli elementi dello scenario,
        #usata nelle funzioni di controllo collisione
        self.elements = pygame.sprite.Group()      

        #self.collideable = pygame.sprite.Group()
        #self.collideable.add(self.objects_in_game, self.directions, self.characters)

        self.background = game_elements.Background()
        self.toptext = widgets.TopText()
        self.inventory = inventory.Inventory()
        self.menu = widgets.ActionMenu()

    def update(self, screen, event, pointergroup):
        self.control_collision(self.player, event, pointergroup)
        self.event_controller(event)

        for i in self.characters:
            i.update(event)
         
        for i in self.objects_in_game:
            i.update(event)
        
        self.toptext.update(self.elements)
        self.inventory.update()
        
        #update mouse position
        pointergroup.update()

        #update menu position
        self.menu.update(event)
      
        self.render(screen, pointergroup)

    def render(self, screen, pointergroup):

        #prima lo sfondo
        screen.blit(self.background.image, self.background.rect)
        self.toptext.draw(screen)

        self.objects_in_game.draw(screen)
        #self.characters.draw(screen)
        
        for i in self.characters.sprites():
            i.draw(screen)
            
        for i in self.objects_in_game.sprites():
            i.draw(screen)

        screen.blit(self.player.image, self.player.rect)
        pointergroup.draw(screen)
        
        #inventory stuff
        self.inventory.draw(screen)

        #draw menu if opened
        if self.menu.visible == True:
            self.menu.sprites.draw(screen)        
         
    def control_collision(self, player, event, pointergroup):
        #method to move in different scenarios
        where = pygame.sprite.spritecollide(player, self.directions, 0)
        for w in where:
            if w and event.type == pygame.MOUSEBUTTONUP and event.__dict__['button'] == 1:
                if w.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.event.post(w.event)

        pointer = pointergroup.sprites()
        collision = pygame.sprite.spritecollide(pointer[0], self.elements, 0)

        if collision:
            #if mouse collide with one of game elements
            for c in collision:
                #for every element the mouse collide with
                if c.type == 'object' or c.type == 'character':
                    #we open the menu for this 2 kind of elements
                    self.selected = c
                    if pygame.mouse.get_pressed()==(0,0,1):
                        self.menu.open_menu(c.name)
                    else:
                        self.menu.close_menu(c.name)                                      
                if self.menu.visible:
                    #if the menu is open we don't show object name
                    self.toptext.hide()
                else:
                    self.toptext.set_label(c.name)
                    self.toptext.show()
        else:
            self.toptext.hide()
            if event.type == pygame.MOUSEBUTTONUP:
                #we close the menu if we loose focus on it
                self.menu.hide()

    def event_controller(self, event):
        #this code update top text based on selected action
        if event.type == pygame.USEREVENT+2:
            match event.__dict__['action']:
                case 'examine':
                    if event.__dict__['event'] == 'selected':
                        self.toptext.show()
                        self.toptext.text.set_label('examine ' + self.selected.name)
                    if event.__dict__['event'] == 'clicked':
                        print('examine clicked on', self.selected.name)
                case 'take':
                    if event.__dict__['event'] == 'selected':
                        self.toptext.show()
                        self.toptext.text.set_label('take ' + self.selected.name)
                    if event.__dict__['event'] == 'clicked':
                        print('take clicked on', self.selected.name)
                case 'talk':
                    if event.__dict__['event'] == 'selected':
                        self.toptext.show()
                        self.toptext.text.set_label('talk to ' + self.selected.name)
                    if event.__dict__['event'] == 'clicked':
                        print('talk clicked on', self.selected.name)

    def play_music(self):
        """ Stream music with mixer.music module in blocking manner.
        This will stream the sound from disk while playing. """
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()
    
class Menu(Scenario):
    def load(self):
        
        print('carico il menu')
        self.name = 'menu'
        self.background.image = functions.load_image('background','menu.png')
        
        self.new_game = widgets.Button('New Game',(300,200))
        self.exit_game = widgets.Button('Exit Game',(300,250))
        self.continue_game = widgets.Button('Continue Game',(300,300))
        
        self.new_game.OnLeftClick(events.START_GAME)
        self.exit_game.OnLeftClick(pygame.event.Event(pygame.QUIT))

        self.interface = widgets.Interface()
        self.interface.add_widget(self.new_game)
        self.interface.add_widget(self.exit_game)
        self.interface.add_widget(self.continue_game)

    def update(self, screen, event, pointergroup):
        """overloading of scenario class with simplified update method"""
        self.interface.update(event)
        pointergroup.update()

    def render(self,screen, pointergroup):
        
        screen.blit(self.background.image, self.background.rect)
        pointergroup.draw(screen)
        self.interface.draw(screen)

class Intro(Scenario):
    def load(self,player):
        self.name = 'intro'
        self.player = player
        if state.current_scenario == '':
            self.player.position(50,250)
        elif state.current_scenario == 'bar':
            self.player.position(700,250)

        self.background.image = functions.load_image('background','intro.jpg')
   
        porta = game_elements.Directions('door','bar',(732,245,100,100))
        spank = game_elements.Character('spank','spank.png',(680,300))
        
        self.directions.add(porta)
        self.characters.add(spank)

        self.elements.add(self.objects_in_game, self.directions, self.characters)

class Bar(Scenario):
    def load(self, player):
        self.name= 'bar'
        self.player = player
        self.player.position(50,250)
        self.background.image = functions.load_image('background','bar.jpg')
   
        porta = game_elements.Directions('back','intro',(0,245,100,200))
        birra = game_elements.Object('beer','beer.png',(532,245))
        
        self.directions.add(porta)
        self.objects_in_game.add(birra)

        self.elements.add(self.objects_in_game, self.directions, self.characters)

