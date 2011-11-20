import sys
import pygame

import Render
import Scenario
import Menu
import GameElements
import Widgets
import Game

class Engine():
    def __init__(self, screen):
        self.screen = screen
        self.pointer = GameElements.Pointer()
        self.pointergroup = pygame.sprite.RenderPlain(self.pointer)
        
        #self.menu = Menu.Menu()
        
    def run(self):
        
        #self.menu.run(self.screen,self.pointergroup)
        #Game.run(self.screen,self.pointergroup)
        
        clock = pygame.time.Clock()
        scenario = Scenario.Menu()
        scenario.load()
        
        #loop principale
        while True:
            for event in pygame.event.get():
                if event.type == (pygame.QUIT):
                    print "fine"
                    sys.exit()
                    
                if event.type == (pygame.KEYDOWN):
                    print event.dict
                    if event.dict['key'] == 27:
                        print "fine"
                        Menu.run(screen,pointergroup)
                        #sys.exit()
            if scenario.running == True:    
                scenario.Update(self.pointergroup,clock,event)
                scenario.Render(self.screen)
            if scenario.change == True:
                scenario = scenario.load()
            
            #Render.render(self.screen,scenario,self.pointergroup)
            clock.tick()
        return 0