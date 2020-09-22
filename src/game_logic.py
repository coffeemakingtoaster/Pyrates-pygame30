import os
import ui_helper

class game():
    def __init__(self):
        self.path = os.path.join(os.getcwd(),"dataa")
        self.gold = 0
        self.supplies = 0
        self.ammunition = 0
        self.ship_HP = 0

    def read_balance(self):


    def read_savegame(self):


    def island_event(self):
        text = "Wow this does things"
        title = "battle"
        popup,ok_hitbox = ui_helper.status_update(title,text)
        return popup,ok_hitbox


    def get_ammunition(self):
        return self.ammunition

    def get_supplies(self):
        return self.supplies

    def get_gold_value(self):
        return self.gold

    def get_ship_HP(self):
        return self.ship_HP