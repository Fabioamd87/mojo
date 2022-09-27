import sys
import pygame

import player
import scenario
import state
import events
import game_elements

"""
event table:
abbiamo a disposizione 8 categorie principali
pygame.USEREVENT+1) scenario change
pygame.USEREVENT+2) action menu event
...
"""
class Engine():
    def __init__(self, screen):
        self.screen = screen
        self.pointer = game_elements.Pointer()
        pygame.mouse.set_visible(False)
        self.pointergroup = pygame.sprite.RenderPlain(self.pointer)
        
    def run(self):
        
        clock = pygame.time.Clock()

        #Generating Player
        p = player.Player('player.png', 150, 50, 1)

        #carico e avvio lo scenario
        s = scenario.Menu()
        s.load()

        #loop principale
        while True:
            for event in pygame.event.get():
                if event.type == (pygame.USEREVENT+1):
                    if event.dict['destination'] == 'intro':
                        s = scenario.Intro()
                        s.load(p)
                        #s.update(self.screen, event, self.pointergroup)
                        state.current_scenario = 'intro'
                        pygame.display.update()

                if event.type == (pygame.USEREVENT+1):                
                    if event.dict['destination'] == 'bar':
                        s = scenario.Bar()
                        s.load(p)
                        #s.update(self.screen, event, self.pointergroup)
                        state.current_scenario = 'bar'
                        pygame.display.update()

                if event.type == (pygame.USEREVENT+1):
                    #continue button pressed
                    if event.dict['destination'] == 'continue':
                        pygame.event.Event(pygame.USEREVENT+1,{'subcat':0,'destination':state.current_scenario})

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.dict['button'] == 1 and s.name != 'menu':
                        if not s.player.talking:
                            print('walking')
                            s.player.walkto(pygame.mouse.get_pos())

                #Game Events
                if event.type == (pygame.QUIT):
                    print("fine")
                    sys.exit()
                    
                if event.type == (pygame.KEYDOWN):
                    if event.dict['key'] == 27:
                        s = scenario.Menu()
                        s.load()

                s.update(self.screen, event, self.pointergroup)
            p.update()
            s.render(self.screen, self.pointergroup)
            pygame.display.update()
            clock.tick(30)

        return 0
