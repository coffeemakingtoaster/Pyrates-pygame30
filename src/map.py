import json
import pygame
import math
import os
import ui_helper
import game_logic
import game_ui


asset_path = os.path.join(os.getcwd(), "data", "img")

img_grid = [
    ["small1.png","mid1.png","large1.png"],
    ["small2.png","mid2.png","large2.png"],
    ["small3.png","mid3.png","large3.png"],
    ["small4.png","mid4.png","large4.png"]
]

def mapdraw(ship_pos_x,ship_pos_y,screen):

    with open('data/savegame/map.json') as json_file:
        map = json.load(json_file)

    for island in map:
        if ship_pos_x-500 < island.get("x") < ship_pos_x+500 and  ship_pos_y-600 < island.get("y") < ship_pos_y+600:
            if(island.get("type")==1):
                current_island = pygame.image.load(os.path.join(asset_path, img_grid[island.get("type")-1][island.get("size")-1]))
                screen.blit(current_island, (1350 + (island.get("x") - ship_pos_x),
                                                                   (450 - (island.get("y") - ship_pos_y))))
            elif (island.get("type") == 2):
                pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(1350 + (island.get("x") - ship_pos_x),
                                                                   (450 - (island.get("y") - ship_pos_y)), 150,
                                                                   150))
            elif (island.get("type") == 3):
                pygame.draw.ellipse(screen, (255, 255, 0), pygame.Rect(1350 + (island.get("x") - ship_pos_x),
                                                                   (450 - (island.get("y") - ship_pos_y)), 150,
                                                                   150))
            elif (island.get("type") == 4):
                pygame.draw.ellipse(screen, (205, 133, 63), pygame.Rect(1350 + (island.get("x") - ship_pos_x),
                                                                   (450 - (island.get("y") - ship_pos_y)), 150,
                                                                   150))






