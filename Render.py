"""disegna la scena"""
import pygame

def render(screen,t,scenario,pointergroup):
    
    bg = scenario.background
    oggetti = scenario.objects_in_game
    text = scenario.text_in_game
    inventory = scenario.inventory
    characters = scenario.characters
    
    screen.blit(bg.image, bg.rect)
    for i in oggetti:
        if i.visible:
            screen.blit(i.image, i.rect)
        
    for i in characters:
        screen.blit(i.image, i.rect)
        
    screen.blit(t.image, t.rect)
    
    for i in text:
        if i.visible:
            screen.blit(i.text, i.rect)
              
    screen.blit(inventory.box.image, inventory.box.rect)
    #inventario.Objects.draw(screen)
    for i in inventory.box.Objects:
        print 'disegno', i.name
        screen.blit(i.image, i.rect)
    pointergroup.update()
    pointergroup.draw(screen)
    pygame.display.update()
    
    if scenario.textbox.speak.visible == True:
        pygame.time.delay(1000)
    scenario.textbox.speak.visible = False
