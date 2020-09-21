import random
import json

island_count = 50
map_width = 150
map_length = 600
max_map_size = 4
map_types = 4

crew_count = 8
attribute_types = 8
max_starting_level = 3
name_count = 8

roledic = {
    0:"Helmsman",
    1:"Navigator",
    2:"look out",
    3:"Doctor",
    4:"Carpenter",
    5:"Cook",
    6:"Brute",
    7:"Brute"

}

attributedic = {
    0:"Giant",
    1:"Zen",
}



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

def crewgen():

    with open('data/other/names.json') as json_file:
        name_list = json.load(json_file)#
    crew = []
    for i in range(crew_count):
        crew_member = {
         "name" : name_list[random.randint(0,name_count-1)],
         "attribute" : random.randint(1,attribute_types),
         "injured" : False,
         "level" : random.randint(1,max_starting_level),
         "role" : roledic.get(i)
         }
        crew.append(crew_member)

    crewfile = open("data/savegame/crew.json", "w")
    crewfile.write(json.dumps(crew))
    crewfile.close()





