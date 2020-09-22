import json
import pygame
import math
import ui_helper
import game_logic
import game_ui


def mapdraw(ship_pos_x,ship_pos_y,screen):
    with open('data/savegame/map.json') as json_file:
        map = json.load(json_file)

    for island in map:
        if ship_pos_x-500 < island.get("x") < ship_pos_x+500 and  ship_pos_y-600 < island.get("y") < ship_pos_y+600:
            pygame.draw.ellipse(screen, (237, 226, 197), pygame.Rect(1350+(island.get("x")-ship_pos_x),(450-(island.get("y")-ship_pos_y)), 150, 150))






