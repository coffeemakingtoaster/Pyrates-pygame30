import os
import json
import generator
import random
import ui_helper

class game():
    def __init__(self,screen):
        self.current_tick = 0
        self.path = os.path.join(os.getcwd(),"data")
        self.read_balance()
        self.read_savegame()
        self.screen = screen
        self.speed_boost = 0



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
        self.current_tick = self.current_tick+data["game_tick"]
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
            shop_popup = ui_helper.shop(event_values,self.gold)
            self.screen.blit(shop_popup.get_surface(),(0,0))
            return shop_popup
        elif type==2:
            battle_window = ui_helper.popup_window(type=2,event_values=event_values)
            self.screen.blit(battle_window.get_surf(), battle_window.get_surf().get_rect(center=(800, 450)))
            battle_window.set_offset(800, 450)
            return battle_window
        elif type==3:
            pass
        elif type==4:
            print(event_values)
            if event_values is None:
                update_window = ui_helper.popup_window(type=1, caption="ZZZ", text="nothing happened")
                self.screen.blit(update_window.get_surf(), update_window.get_surf().get_rect(center=(800, 450)))
                update_window.set_offset(800, 450)
                return update_window
            elif "castaway" in event_values.keys():
                print("castaway")
                update_window = ui_helper.popup_window(type=3,event_values=event_values,crew = self.crew)
                self.screen.blit(update_window.get_surf(), update_window.get_surf().get_rect(center=(800, 450)))
                update_window.set_offset(800, 450)
                return update_window
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
                update_window.set_offset(800,450)
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
                update_window.set_offset(800, 450)
                print(message)
                return update_window


    def battle(self,values):
        outcome = random.randint(0,100)
        #battle won
        if outcome<=values["victory"]:
            outcome = "Victory"
            message = ""
            found_gold = False
            if "loot" in values.keys():
                message += "You found"
                if "gold" in values["loot"].keys():
                    found_gold = True
                    self.gold += values["loot"]["gold"]
                    message += " "+str(values["loot"]["gold"])+" gold"
                if "supplies" in values["loot"].keys():
                    self.supplies += values["loot"]["supplies"]
                    if self.supplies>self.max_supply:
                        self.supplies = 150
                    if found_gold:
                        message += "and "+str(values["loot"]["supplies"])+" supplies"
                    else:
                        message += " "+str(values["loot"]["supplies"])+" supplies"
                elif "ammunition" in values["loot"].keys():
                    self.ammunition += values["loot"]["ammunition"]
                    if self.ammunition>self.max_ammunition:
                        self.ammunition = 150
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
            index = random.randint(0,len(self.crew)-1)
            crew_member = self.crew[index]
            crew_member_name = crew_member["name"]
            if crew_member["injured"] == True:
                self.crew.remove(crew_member)
                message += " "+str(crew_member_name)+" fought heroically but died on the battlefield."
            else:
                crew_member["injured"] = True
                message += " "+str(crew_member_name)+" was wounded on the battlefield and needs to be healed."
                self.crew[index] = crew_member
            if values["damage"] != 0:
                message += "And your ship hast lost " + str(values["damage"]) + "HP"
            else:
                message += "Luckily your ship is not damaged"
            message += "!"
        self.level_up_crew()
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

    def write_crew(self):
        f = open(os.path.join(os.getcwd(), "data", "savegame", "crew.json"),"w")
        f.write(json.dumps(self.crew))
        f.close()

    def get_speed_multiplier(self):
        return self.speed_boost

    def level_up_crew(self):
        self.speed_boost = 0
        for member in self.crew:
            if "xp" in member.keys():
                member["xp"] += 1
                if member["xp"] >= member["level"]:
                    member["xp"] = 0
                    member["level"] += 1
            else:
                member["xp"]=1
            if member["role"] == "Helmsman":
                self.speed_boost += member["level"]
        self.write_crew()

    def crew_ability(self, index):
        member = self.crew[index]
        print(member)
        if member["role"] == "Carpenter":
            if member["is_in_action"] is False:
                print("now in action")
                member["finish_tick"] = self.current_tick + 1
                member["is_in_action"] = True
        elif member["role"] == "Helmsman":
            print("is boosting speed by " + str(member["level"]) + "%!")
        self.write_crew()
        self.screen.blit(ui_helper.draw_crew_overview(), (0, 0))

    def advance_tick(self):
        self.current_tick += 1
        print("now at gametick" + str(self.current_tick))
        for member in self.crew:
            if "is_in_action" in member.keys():
                if member["is_in_action"] == True:
                    if member["finish_tick"] <= self.current_tick:
                        if member["role"] == "Doctor":
                            for target in self.crew:
                                if target["uID"] == member["target_id"]:
                                    target["is_injured"] = False
                                    break
                        elif member["role"] == "Carpenter":
                            if self.ship_HP < 5:
                                self.ship_HP += 1
                        member["xp"] += 1
                        member["is_in_action"] = False
            else:
                member["is_in_action"] = False
        food_cons = 0
        gold_cons = 0
        for member in self.crew:
            if member["role"] == "Cook":
                gold_cons += member["level"]
            else:
                food_cons += member["level"]
        self.supplies -= food_cons
        self.gold -= gold_cons
        self.write_crew()

    def update_screen(self,screen):
        self.screen = screen

    def recruit(self,crewmember):
        self.crew.append(crewmember)
        self.write_crew()
        self.screen.blit(ui_helper.draw_crew_overview(), (0, 0))

    def attempt_dispatch(self,index):
        member = self.crew[index]
        dispatch_dialog = ui_helper.popup_window(type=4,event_values=member)
        self.screen.blit(dispatch_dialog.get_surf(), dispatch_dialog.get_surf().get_rect(center=(800, 450)))
        dispatch_dialog.set_offset(800, 450)
        return dispatch_dialog

    def dispatch(self,crew_member):
        self.crew.remove(crew_member)
        self.write_crew()
        self.screen.blit(ui_helper.draw_crew_overview(), (0, 0))

    def crew_has_space(self):
        if len(self.crew)!=8:
            return True
        return False
