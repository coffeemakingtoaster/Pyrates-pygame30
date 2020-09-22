import os
import json
import generator
import random
import ui_helper

class game():
    def __init__(self,screen):
        self.path = os.path.join(os.getcwd(),"data")
        self.read_balance()
        self.read_savegame()
        self.screen = screen

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
        f = open(os.path.join(self.path,"savegame","crew.json"))
        self.crew = json.load(f)
        f.close()

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

    def island_event(self,type,size):
        event_values = generator.island_eventgen(type,size)
        if type==1:
            shop = ui_helper.shop(event_values,self.gold)
            self.screen.blit(shop.get_surface(),(0,0))
            return shop
        elif type==2:
            ui_helper.popup_window(type=2,event_values=event_values)
        elif type==3:
            pass
        elif type==4:
            print(event_values)
            if "castaway" in event_values.keys():
                print("castaway")
                return None
                #ui_helper.popup_window(type=4,event_values=event_values)
            elif "loss" in event_values.keys():
                title = "Oh no!"
                if event_values["loss"]["type"]=="supplies":
                    self.supplies -= event_values["loss"]["amount"]
                    message = "Your men had their lunch stolen by monkeys! You lose "+str(event_values["loss"]["amount"])+" supplies!"
                elif event_values["loss"]["type"]=="ammunition":
                    self.ammunition -= event_values["loss"]["amount"]
                    message = "Your men shot at monkeys! You lose "+str(event_values["loss"]["amount"])+" ammunition!"
                update_window = ui_helper.popup_window(type=1,caption=title,text=message)
                self.screen.blit(update_window.get_surf(),update_window.get_surf().get_rect(center=(800,450)))
                print(message)
                return update_window
            elif "loot" in event_values.keys():
                title = "YAAAAAR!"
                if event_values["loot"]["type"]=="supplies":
                    self.supplies += event_values["loot"]["amount"]
                    message = "Your men were useful for once! You found "+str(event_values["loot"]["amount"])+" supplies!"
                elif event_values["loot"]["type"]=="ammunition":
                    self.ammunition += event_values["loot"]["amount"]
                    message = "Your men were useful for once! You found "+str(event_values["loot"]["amount"])+" ammunition!"
                update_window = ui_helper.popup_window(type=1,caption=title,text=message)
                self.screen.blit(update_window.get_surf(), update_window.get_surf().get_rect(center=(800, 450)))
                print(message)
                return update_window

    def battle(self,values):
        outcome = random.randint(0,100)
        #battle won
        if outcome<=values["victory"]:
            outcome = "Victory"
            message = ""
            found_gold = False
            if "loot" in values.keys:
                message += "You found"
                if "gold" in values["loot"].keys:
                    found_gold = True
                    self.gold += values["loot"]["gold"]
                    message += " "+str(values["loot"]["gold"])+" gold"
                if "supplies" in values["loot"].keys:
                    self.supplies += values["loot"]["supplies"]
                    if found_gold:
                        message += "and "+str(values["loot"]["supplies"])+" supplies"
                    else:
                        message += " "+str(values["loot"]["supplies"])+" supplies"
                elif "ammunition" in values["loot"].keys:
                    self.ammunition += values["loot"]["ammunition"]
                    if found_gold:
                        message += "and "+str(values["loot"]["ammunition"])+" ammunition"
                    else:
                        message += " "+str(values["loot"]["ammunition"])+" ammunition"

                message += "!"
            else:
                if values["damage"] != 0:
                    message += "but your ship hast lost "+str(values["damage"]+"HP")
                else:
                    message+= "You won without any casualties"
                message += "!"
        else:
            outcome = "Defeat"
            message = ""
            index = random.randint(0,len(self.crew))
            crew_member = self.crew[index]
            crew_member_name = crew_member["name"]
            if crew_member["injured"] == True:
                self.crew.remove(crew_member)
                message += " "+str(crew_member_name)+" fought heroically but died on the battlefield."
            else:
                crew_member["injured"] = True
                message += " "+str(crew_member_name)+" was wounded on the battlefield and needs to be healed."
        return outcome,message

    def make_purchase(self,item,price):
        if not price:
            return
        if not item:
            return
        if item == "supplies":
            self.supplies+=1
        if item == "ammunition":
            self.ammunition+=1
        self.gold -=price



