import random
import json

island_count = 50
map_width = 150
map_length = 600
max_map_size = 4
map_types = 4



def mapgen():
    x_coordinates = random.sample(range(1, map_width), island_count)
    y_coordinates = random.sample(range(1, map_length), island_count)
    map_list = []
    for i in range(island_count):
        island = {
            "x": x_coordinates[i],
            "y": y_coordinates[i],
            "size": random.randint(1, max_map_size),
            "type": random.randint(1, map_types),
            "visited": False
        }
        map_list.append(island)

    print(map_list)
    mapfile = open("data/savegame/map.json", "w")
    mapfile.write(json.dumps(map_list))
    mapfile.close()

mapgen()


