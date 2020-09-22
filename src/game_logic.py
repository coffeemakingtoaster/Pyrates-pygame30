import os
import ui_helper
import json

class game():
    def __init__(self):
        self.path = os.path.join(os.getcwd(),"data")
        self.read_balance()
        self.read_savegame()

    def read_balance(self):
        f = open(os.path.join(self.path,"balancing.json"))
        settings = json.load(f)
        f.close()
        self.max_ship_HP = settings["ship_max_HP"]
        self.max_supply  = settings["max_supply_amount"]
        self.max_ammunition = settings["max_ammunition_amount"]

    def read_savegame(self):
        f = open(os.path.join(self.path,"savegame","savegame.json"))
        data = json.load(f)
        f.close()
        self.gold = data["gold"]
        self.supplies = data["supplies"]
        self.ammunition = data["ammunition"]
        self.ship_HP = data["ship_HP"]

    def island_event(self):
        text = "Wow this does things"
        title = "battle"
        popup,ok_hitbox = ui_helper.status_update(title,text)
        return popup,ok_hitbox


    def get_ammunition(self):
        return (self.ammunition,self.max_ammunition)

    def get_supplies(self):
        return (self.supplies,self.max_supply)

    def get_gold_value(self):
        return self.gold

    def get_ship_HP(self):
        return (self.ship_HP,self.max_ship_HP)