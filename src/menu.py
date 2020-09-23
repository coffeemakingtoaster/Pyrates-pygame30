import pygame
import os
import math
import time
import pygame_menu
import game_ui

pygame.init()
# init size of the window. The background color is never visible
surface = pygame.display.set_mode((1600,900))
def set_difficulty(value, difficulty):
    # Do the job here !
    pass
def start_the_game():
    # Do the job here !
    game_ui.main()
menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)





menu.add_image("data/img/x_button.png", angle=10, scale=(1, 1))



menu.add_text_input('Name :', default='John Doe')
menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add_button('Play', start_the_game,)
menu.add_image("data/img/x_button.png", angle=10, scale=(1, 1),margin=(0,-75))
menu.add_button('   ', pygame_menu.events.EXIT)

menu.mainloop(surface)