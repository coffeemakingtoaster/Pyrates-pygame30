import json
import pygame
import math
import os
import ui_helper
import game_logic
import game_ui
from pygame import gfxdraw

asset_path = os.path.join(os.getcwd(), "data", "img")

img_grid = [
    ["small1.png","mid1.jpg","large1.jpg"],
    ["small2.jpg","mid2.jpg","large2.jpg"],
    ["small3.jpg","mid3.jpg","large3.jpg"],
    ["small4.jpg","mid4.jpg","large4.jpg"],
    ["start.png"],
    ["end.png"]
]

size_dic = {
    0: 100,
    1: 175,
    2: 250
}
island_hitbox = pygame.Rect(0,0,0,0)
def mapdraw(ship_pos_x,ship_pos_y,screen):
    with open('data/savegame/map.json') as json_file:
        map = json.load(json_file)
        gfxdraw.pixel(screen, int((ship_pos_x / 25)) + 533, int(450 - (ship_pos_y / 25)), (255, 255, 255))
    i = 0
    for island in map:
        if ship_pos_x-500 < island.get("x") < ship_pos_x+500 and  ship_pos_y-600 < island.get("y") < ship_pos_y+600:
                current_island = pygame.image.load(os.path.join(asset_path, img_grid[island.get("type")][island.get("size")]))
                screen.blit(current_island, (1350 + (island.get("x") - ship_pos_x),(450 - (island.get("y") - ship_pos_y))))
                gfxdraw.pixel(screen, int((island.get("x") / 25)) + 533, int(450 - (island.get("y") / 25)), (0, 255, 0))



        i+=1
    pygame.draw.rect(screen, (0, 0, 0), (573, 0, 493, 450), 0)
    return None
def collisioncheck(ship_pos_x,ship_pos_y):
    with open('data/savegame/map.json') as json_file:
        map = json.load(json_file)
    i = 0
    for island in map:
        island_hitbox = pygame.Rect(1350 + (island.get("x") - ship_pos_x), (450 - (island.get("y") - ship_pos_y)),
                                    size_dic.get(island.get("size")), size_dic.get(island.get("size")))
        if island_hitbox.colliderect(1340,440,20,20):
            print("Collision with type: "+ str(island.get("type")))
            island["visited"] = True
            write_map(map)
            return {"island_id":i,"island_values":island}
    i+=1


def write_map(map):
    f = open(os.path.join(os.getcwd(),"data","savegame","map.json"),"w")
    f.write(json.dumps(map))
    f.close()