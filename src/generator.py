import random
import json
import os



save_path = os.path.join(os.getcwd(),"data","savegame")


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
    0:"Helmsman",                      #Speed (basespeed*level*x)
    1:"Navigator",                     #
    2:"look out",                      #Fog of war range
    3:"Doctor",                        #Heal injured teammate - 1 + level delta time to heal
    4:"Carpenter",                     #Repair ship (levelbased)
    5:"Cook",                          #decreases food consumption - but consumes gold per day with increasing level
    6:"Brute",                         # + x % battle win chance - reduces damage to ship but food consumption increases with level
    7:"Brute"                          # + x % battle win chance - reduces damage to ship but food consumption increases with level

}

attributedic = {
    0:"Giant",
    1:"Zen",
}

shop_items = {
    1:"Healing potion",                #Can heal one party member after a fight - at no cost
    2:"Safeguard",                     #Crewmember survives an otherwise deadly treasure hunt - but no loot
    3:"Treasure map",                  #Lowers chance of fatal injury during treasure hunt by 15% - raises chance to find the treasure by 15%
    4:"Fancy costumes"                 #Your crew puts on fancy costumes and therefore the marine can´t tell that you are pirates...lasts 2 days
}

# types:
# 1 - Shop
# 2 - Fortress
# 3 - Treasure
# 4 - normal
#
#

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
        name_list = json.load(json_file)
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


def island_eventgen(type,size):
    # if the island is a shop
    f = open(os.path.join(save_path,"crew.json"))
    crew_data = json.loads(f)
    f.close()
    if type == 1:
        supply_price = random.randint(1,3)
        supply_amount = random.randint(1,10)
        ammunition_price = random.randint(1,3)
        ammunition_amount = random.randint(1,10)
        x = random.randint(1,4)
        bonus_item = shop_items[x]
        bonus_price = random.randint(5,15)+x
        bonus_amount = random.randint(1,2)*(size/2)
        return {"supplies":
                    {"price":supply_price,
                     "amount":supply_amount},
                "ammunition":
                    {"price":ammunition_price,
                     "amount":ammunition_amount},
                str(bonus_item):
                    {"price":bonus_price,
                     "amount":bonus_amount}
                }
    elif type == 2:
        possible_loot = ["supplies","ammunition","gold"]
        victory_chances = random.randint(10,75)
        for member in crew_data:
            if member["role"] == "Brute":
                victory_chances+=member["level"]
                if victory_chances==100:
                    break
        defeat_chances = 100-victory_chances
        island_loot = random.choice(possible_loot)
        amount = random.randint(5,15)
        loot = {str(island_loot): int(amount)}
        if size>2:
            if island_loot == "gold":
                loot["gold"]+=5
            else:
                loot["gold"]=5
        return {"victory":int(victory_chances),"defeat":int(defeat_chances),"loot":loot}
    elif type==3:
        has_bonus_item = False
        if random.randint(1,5) == 2:
            has_bonus_item = True
        loot = random.randint(3,8)+size
        if not has_bonus_item:
            return {"gold":int(loot)}
        return {"gold":int(loot),"bonus":{"type":shop_items[random.randint(1,4)]}}
    elif type==4:
        event = random.randint(1,4)
        #found new crewmember
        if event == 1:
            with open('data/other/names.json') as json_file:
                name_list = json.load(json_file)
            castaway = {
                "name" : name_list[random.randint(0,name_count-1)],
                "attribute" : random.randint(1,attribute_types),
                "injured" : False,
                "level" : random.randint(1,max_starting_level),
                "role" : roledic.get(i)
                }
            return {"castaway":castaway}
        #found supplies
        elif event == 2:
            item = random.randint(1,2)
            if item == 1:
                item = "supplies"
            else:
                item = "ammunition"
            amount = random.randint(3,5)
            return {"loot":{"type":str(item),"amount":int(amount)}}
        #lost resources
        elif event == 3:
            item = random.randint(1, 2)
            if item == 1:
                item = "supplies"
            else:
                item = "ammunition"
            amount = random.randint(1, 4)
            return {"loss": {"type": str(item), "amount": int(amount)}}
        #nothing
        else:
            return None

    def ship_encounter(ship_HP):
        f = open(os.path.join(save_path, "crew.json"))
        crew_data = json.loads(f)
        f.close()
        victory_chances = random.randint(10,75)-((5-ship_HP)*3)
        for member in crew_data:
            if member["role"] == "Brute":
                victory_chances+=member["level"]
                if victory_chances==100:
                    break
        defeat_chances = 100-victory_chances
        hp_lost = random.randint(0,1)
        return {"victory":int(victory_chances),"defeat":int(defeat_chances),"damage":int(hp_lost)}


