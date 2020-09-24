import random
import json
import os
import string
from PIL import Image



save_path = os.path.join(os.getcwd(),"data","savegame")
f = open(os.path.join(os.getcwd(),"data","balancing.json"))
settings = json.load(f)
f.close()


roledic = {
    0:"Helmsman",                      #Speed (basespeed*level*x)
    1:"Fattie",                        #HighScore - high food consumption - no direct buffs
    2:"Adventurer",                    #Higher chance to get treasure without casulties
    3:"Doctor",                        #Heal injured teammate - 1 + level delta time to heal
    4:"Carpenter",                     #Repair ship (levelbased)
    5:"Cook",                          #decreases food consumption - but consumes gold per day with increasing level
    6:"Brute",                         # + lvl % battle win chance - reduces damage to ship but food consumption increases with level
    7:"Brute"                          # + lvl % battle win chance - reduces damage to ship but food consumption increases with level

}
#currently unused
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
# 0 - normal
# 1 - Shop
# 2 - Fortress
# 3 - Treasure
# 4 - start
# 5 - end
#

def start_state_gen():
    f = open(os.path.join(os.getcwd(),"data","savegame","savegame.json"),"w")
    f.write(json.dumps({"gold": 15, "supplies": 50, "ammunition": 50, "game_tick": 0, "ship_HP": 5}))
    f.close()

def mapgen():

    x_coordinates = random.sample(range(1, settings["map_width"]), settings["island_count"])
    y_coordinates = random.sample(range(3, settings["map_length"]), settings["island_count"])
    map_list = []
    for i in range(settings["island_count"]):
        island = {
            "x": x_coordinates[i],
            "y": y_coordinates[i]*settings["island_distancing"],
            "size": random.randint(0, settings["max_map_size"]),
            "type": random.randint(0, settings["map_types"]),
            "visited": False
        }
        map_list.append(island)
    map_list.append({"x": 600, "y": 100, "size": 0, "type": 4, "visited": True})
    map_list.append({"x": 600, "y": 20000, "size": 0, "type": 5, "visited": False})


    print(map_list)
    mapfile = open("data/savegame/map.json", "w")
    mapfile.write(json.dumps(map_list))
    mapfile.close()



crew_img_list = [["beige_base.png","brown_base.png","invis_base.png","pink_base.png"],
                 ["ascended_face.png","baby_face.png","blind_face.png","creepy_face.png","protagonist_face.png","scared_face.png","sleepy_face.png","smart_face.png","twoface_face.png","weird_face.png","twoface_face.png"],
                 ["blonde_head.png","brown_head.png","crown_head.png","flamingo_head.png","pink_head.png","pirate_head.png","princess_head.png","protagonist_head.png"]
                 ]


def crewgen():
    img_path = os.path.join(os.getcwd(),"data","img")
    with open('data/other/names.json') as json_file:
        name_list = json.load(json_file)
    crew = []
    for i in range(settings["crew_count"]):
        crew_member = {
         "name" : name_list[random.randint(0,settings["name_count"]-1)],
         "attribute" : random.randint(1,settings["attribute_types"]),
         "injured" : False,
         "level" : random.randint(1,settings["max_starting_level"]),
         "role" : roledic.get(i),
         "is_in_action": False,
         "xp":0,
         "uID": ''.join(random.choice(string.ascii_letters) for i in range(8)),
         }
        print(os.path.join(img_path,crew_img_list[0][random.randint(0, 3)]))
        img_base = Image.open(os.path.join(img_path,"crew","base",crew_img_list[0][random.randint(0, 3)]))
        img_face = Image.open(os.path.join(img_path,"crew","face",crew_img_list[1][random.randint(0, 10)]))
        img_head = Image.open(os.path.join(img_path,"crew","head",crew_img_list[2][random.randint(0, 7)]))
        img_base.paste(img_face,(0,0),img_face)
        img_base.paste(img_head,(0,0),img_head)
        img_base.save(os.path.join(img_path,crew_member["uID"]+".png"))
        crew.append(crew_member)

    crewfile = open("data/savegame/crew.json", "w")
    crewfile.write(json.dumps(crew))
    crewfile.close()


def island_eventgen(type,size):
    # if the island is a shop
    f = open(os.path.join(save_path,"crew.json"))
    crew_data = json.load(f)
    f.close()
    if type == 1:
        supply_price = random.randint(settings["supply_min_price"],settings["supply_max_price"])
        supply_amount = random.randint(settings["supply_min_amount"],settings["supply_max_amount"])
        ammunition_price = random.randint(settings["ammunition_min_price"],settings["ammunition_max_price"])
        ammunition_amount = random.randint(settings["ammunition_min_amount"],settings["ammunition_max_amount"])
        x = random.randint(1,4)
        bonus_item = shop_items[x]
        bonus_price = random.randint(settings["bonus_min_price"],settings["bonus_max_price"])+x
        bonus_amount = int(random.randint(settings["bonus_min_amount"],settings["bonus_max_amount"])*(size/2))
        return {"supplies":
                    {"price":supply_price,
                     "amount":supply_amount},
                "ammunition":
                    {"price":ammunition_price,
                     "amount":ammunition_amount},
                "bonus":
                    {"name":str(bonus_item),
                     "price":bonus_price,
                     "amount":bonus_amount}
                }
    elif type == 2:
        possible_loot = ["supplies","ammunition","gold"]
        victory_chances = random.randint(settings["fortress_min_win_chance"],settings["fortress_max_win_chance"])
        for member in crew_data:
            if member["role"] == "Brute":
                victory_chances+=member["level"]
                if victory_chances==100:
                    break
        defeat_chances = 100-victory_chances
        island_loot = random.choice(possible_loot)
        amount = random.randint(settings["fortress_min_loot"],settings["fortress_max_loot"])
        loot = {str(island_loot): int(amount)}
        if size>2:
            if island_loot == "gold":
                loot["gold"]+=settings["fortress_min_loot"]
            else:
                loot["gold"]=settings["fortress_min_loot"]
        hp_lost = random.randint(0, 1)
        return {"victory":int(victory_chances),"defeat":int(defeat_chances),"loot":loot,"damage":hp_lost}
    #TODO
    elif type==3:
        success_chance = random.randint(settings["treasure_min_chance"],settings["treasure_max_chance"])
        has_bonus_item = False
        if random.randint(0,100)<=settings["treasure_bonus_percentage"]:
            has_bonus_item = True
        loot = random.randint(settings["treasure_min_gold"],settings["treasure_max_gold"])+size
        if not has_bonus_item:
            return {"success":success_chance,"gold":int(loot)}
        return {"success":success_chance,"gold":int(loot),"bonus":{"type":shop_items[random.randint(1,4)]}}
    elif type==4:
        event = random.randint(1,4)
        #found new crewmember
        if event == 1:
            with open('data/other/names.json') as json_file:
                name_list = json.load(json_file)
            castaway = {
                "name": name_list[random.randint(0, settings["name_count"] - 1)],
                "attribute": random.randint(1, settings["attribute_types"]),
                "injured": False,
                "level": random.randint(1, settings["max_starting_level"]),
                "role": random.choice(roledic),
                "is_in_action": False,
                "xp": 0,
                "uID": ''.join(random.choice(string.ascii_letters) for i in range(8))
                }
            return {"castaway":castaway}
        #found supplies
        elif event == 2:
            item = random.randint(1,2)
            if item == 1:
                item = "supplies"
            else:
                item = "ammunition"
            amount = random.randint(settings["island_min_loot"],settings["island_max_loot"])
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
        crew_data = json.load(f)
        f.close()
        victory_chances = random.randint(settings["ship_battle_min_win"],settings["ship_battle_max_win"])-((settings["ship_max_HP"]-ship_HP)*3)
        for member in crew_data:
            if member["role"] == "Brute":
                victory_chances+=member["level"]
                if victory_chances==100:
                    break
        defeat_chances = 100-victory_chances
        hp_lost = random.randint(0,1)
        return {"victory":int(victory_chances),"defeat":int(defeat_chances),"damage":int(hp_lost)}


