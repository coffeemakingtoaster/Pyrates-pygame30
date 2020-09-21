import random
import json

island_count = 50
map_width = 150
map_length = 600
max_map_size = 4
map_types = 4

x_coordinates = random.sample(range(1,map_width),island_count)
y_coordinates = random.sample(range(1,map_length),island_count)
map_list = []

class Islands:
    def __init__(self, x,y,size,typus,visited):
        self.x = x
        self.y = y
        self.size = size
        self.typus = typus
        self.visited = visited


for i in range(island_count):
    island = Islands(x_coordinates[i],y_coordinates[i],random.randint(1,max_map_size),random.randint(1,map_types),False)
    map_list.append(island)

json.dumps(map_list)
print(map_list)

