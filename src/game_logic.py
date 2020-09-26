import os
import json
import random
import generator
import ui_helper
import pygame
from PIL import Image


crew_img_list = [["beige_base.png","brown_base.png","invis_base.png","pink_base.png"],
                 ["ascended_face.png","baby_face.png","blind_face.png","creepy_face.png","protagonist_face.png","scared_face.png","sleepy_face.png","smart_face.png","twoface_face.png","weird_face.png","twoface_face.png"],
                 ["blonde_head.png","brown_head.png","crown_head.png","flamingo_head.png","pink_head.png","pirate_head.png","princess_head.png","protagonist_head.png"]
                 ]

class game():
    def __init__(self,screen):
        self.current_tick = 0
        self.path = os.path.join(os.getcwd(),"data")
        self.read_balance()
        self.read_savegame()
        self.screen = screen
        self.speed_boost = 0

    def is_game_over(self):
        if self.supplies<0 or len(self.crew)<=0 or self.ship_HP==0:
            for file in os.listdir(os.path.join(self.path,"savegame")):
                try:
                    os.remove(os.path.join(self.path,"savegame",file))
                except Exception as e:
                    print(e)
            for file in os.listdir(os.path.join(self.path,"img","crew_faces")):
                try:
                    os.remove(os.path.join(self.path, "savegame", file))
                except Exception as e:
                    print(e)
            return True, "Better Luck next time!"
        else:
            return False,None

    def crew_heal_potion(self,index):
        if self.inventory["heal_pots"] > 0:
            member = self.crew[index]
            member_name = member["name"]
            member["injured"] = False
            self.inventory["heal_pots"] = 0
            self.write_crew()
            popup = ui_helper.popup_window(type=1,caption="Healed",text="%s was healed but 1 heal pot was consumed"%member_name)
        else:
            popup = ui_helper.popup_window(type=1, caption="Meh",text="You dont have enough heal potions for this")
        self.screen.blit(popup.get_surf(), popup.get_surf().get_rect(center=(800, 450)))
        popup.set_offset(800, 450)
        return popup

    def set_cord(self,x,y):
        self.ship_x = x
        self.ship_y = y

    def set_minimap(self,minimap):
        self.minimap = minimap

    def get_minimap(self):
        return  self.minimap

    def write_savegame(self):
        savepath = os.path.join(self.path,"savegame")
        print(self.max_ship_HP)
        self.write_crew()
        f = open(os.path.join(savepath,"savegame.json"),"w")
        f.write(json.dumps({
            "username":self.username,
            "gold":self.gold,
            "supplies":self.supplies,
            "ammunition":self.ammunition,
            "game_tick":self.current_tick,
            "ship_HP":self.ship_HP,
            "max_ship_hp":self.max_ship_HP,
            "ship_map_x":self.ship_x,
            "ship_map_y":self.ship_y,
            "inventory":self.inventory}))
        print("saved")
        f.close()
        image_string = pygame.image.tostring(self.minimap,'RGBA')
        print(image_string)
        img = Image.frombytes("RGBA",(40,450),image_string,"raw")
        img.save(os.path.join(os.getcwd(),"data","savegame","minimap.png"))
        
    def read_balance(self):
        f = open(os.path.join(self.path,"balancing.json"))
        settings = json.load(f)
        f.close()
        self.max_ship_HP = settings["ship_max_HP"]
        self.max_supply  = settings["max_supply_amount"]
        self.max_ammunition = settings["max_ammunition_amount"]
        f = open(os.path.join(self.path,"other","settings.json"))
        data = json.load(f)
        f.close()
        self.sound_state = data["sound_state"]

    def read_savegame(self):
        f = open(os.path.join(self.path,"savegame","savegame.json"),"r")
        data = json.load(f)
        f.close()
        self.gold = data["gold"]
        self.supplies = data["supplies"]
        self.ammunition = data["ammunition"]
        self.ship_HP = data["ship_HP"]
        self.username = str(data["username"])
        if "max_ship_hp" in data.keys():
            self.max_ship_HP = data["max_ship_hp"]
        self.current_tick = self.current_tick+data["game_tick"]
        self.inventory = data["inventory"]
        f = open(os.path.join(self.path,"savegame","crew.json"))
        self.crew = json.load(f)
        for member in self.crew:
            if "xp" in member.keys():
                member["xp"] += 1
                if member["xp"] >= member["level"]:
                    member["xp"] = member["xp"]-member["level"]
                    member["level"] += 1
        f.close()
        self.write_crew()

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
        if type != 5:
            event_values = generator.island_eventgen(type,size)
        if type==1:
            shop_popup = ui_helper.shop(event_values,self.gold)
            print(shop_popup.is_active())
            self.screen.blit(shop_popup.get_surface(),(0,0))
            return shop_popup
        elif type==2:
            battle_window = ui_helper.popup_window(type=2,event_values=event_values)
            self.screen.blit(battle_window.get_surf(), battle_window.get_surf().get_rect(center=(800, 450)))
            battle_window.set_offset(800, 450)
            return battle_window
        elif type==3:
            print("treasure 2")
            has_map = False
            if self.inventory["treasure_map"]>0:
                has_map = True
                event_values["success"]+=15
                if event_values["success"]>100:
                    event_values["success"] = 100
            treasure_window = ui_helper.popup_window(type=8, event_values=event_values,has_map = has_map)
            self.screen.blit(treasure_window.get_surf(), treasure_window.get_surf().get_rect(center=(800, 450)))
            treasure_window.set_offset(800, 450)
            return treasure_window
        elif type==0:
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
        elif type==5:
            update_window = ui_helper.popup_window(type=1, caption="VICTORY", text="you reached "+str(self.calc_score())+" points!")
            self.screen.blit(update_window.get_surf(), update_window.get_surf().get_rect(center=(800, 450)))
            update_window.set_offset(800, 450)
            return update_window

    def calc_score(self):
        score = self.gold*100+self.ammunition*10+self.supplies*10
        print("score"+str(score))
        multiplier = 1
        for member in self.crew:
            if member["role"] == "Fattie":
                multiplier+=member["level"]/2
            score += member["level"]*5
        score = score * multiplier
        if os.path.isfile(os.path.join(os.getcwd(),"data","other","highscores.json")):
            print("file exists")
            f = open(os.path.join(os.getcwd(),"data","other","highscores.json"))
            data = json.load(f)
            print(data)
            f.close()
            new_score = {"username": self.username, "score": int(score)}
            print(data)
            data.append(new_score)
            new_f = open(os.path.join(os.getcwd(),"data","other","highscores.json"),"w")
            new_f.write(json.dumps(data))
            new_f.close()
        else:
            print("creating file")
            f = open(os.path.join(os.getcwd(), "data", "other", "highscores.json"), "w")
            f.write(json.dumps([{"username":self.username,"score":int(score)}]))
            f.close()
        return int(score)

    def treasure_hunt(self,values):
        outcome = random.randint(0, 100)
        if outcome<=values["success"]:
            outcome = "Success"
            message = "You found "+str(values["gold"])+" gold"
            self.gold += int(values["gold"])
            if "bonus" in values.keys():
                message+=" and 1 "+str(values["bonus"]["type"])
            message+="!"
        else:
            outcome = "Failure"
            message = "You failed to find the treasure "
            index = random.randint(0, len(self.crew) - 1)
            crew_member = self.crew[index]
            crew_member_name = crew_member["name"]
            if crew_member["injured"] == True:
                self.crew.remove(crew_member)
                message += " " + str(crew_member_name) + " had to die for it"
            else:
                crew_member["injured"] = True
                message += " " + str(crew_member_name) + " was wounded while trying their best"
                self.crew[index] = crew_member
            if self.inventory["safeguard"]>0:
                message = "You failed to find the treasure! Luckily safeguard protected "+str(crew_member_name)+" from harm"
            message+="!"
        return outcome,message


    def battle(self,values):
        outcome = random.randint(0,100)
        if self.ammunition<=0:
            print("no supplies")
            outcome = 999
        else:
            self.ammunition-=5
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
            if self.ammunition<=0:
                message+="You fought without ammunition"
                values["damage"] = 1
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
            self.ship_HP -= values["damage"]
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

    def get_supply_consumption(self):
        consum = 0
        for member in self.crew:
            if member["role"] == "Cook":
                consum -= member["level"]*2
            else:
                consum += member["level"]
        return consum

    def get_gold_consumption(self):
        consum = 0
        for member in self.crew:
            if member["role"] == "Cook":
                consum = member["level"]
        return consum

    def get_speed_multiplier(self):
        self.speed_boost = 1
        for member in self.crew:
            if member["role"] == "Helmsman" and member["injured"] is False:
                self.speed_boost += (member["level"]/100)
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
        self.write_crew()

    def crew_ability(self, index):
        member = self.crew[index]
        print(member)
        if member["injured"] == True:
            return ui_helper.popup_window(type=1, caption="Info",text=str(member["name"])+"is hurt and therefore useless...heal this crewmember first!")
        if member["role"] == "Carpenter" and member["is_in_action"] is False:
            print("now in action")
            member["finish_tick"] = self.current_tick + 1
            member["is_in_action"] = True
            if self.sound_state == 1:
                start_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), "data", "sound", "job_start.mp3"))
                start_sound.set_volume(0.5)
                pygame.mixer.Sound.play(start_sound)
        elif member["role"] == "Helmsman":
            return ui_helper.popup_window(type=1,caption ="Info",text="Is boosting ship speed by "+str(member["level"])+"%",is_crewmember = True)
        elif member["role"] == "Fattie":
            return ui_helper.popup_window(type=1, caption="Info",text="Is fat, useless and does not contribute in any way...is there any real reason to have him on board?!",is_crewmember = True)
        elif member["role"] == "Adventurer":
            return ui_helper.popup_window(type=1, caption="Info",text="Increases chance for successful treasure hunt by " + str(member["level"]) + "%",is_crewmember = True)
        elif member["role"] == "Doctor" and member["is_in_action"] is False:
            return ui_helper.popup_window(type=7,event_values=member)
        elif member["role"] == "Cook":
            return ui_helper.popup_window(type=1, caption="Info",text="Consumes "+str(member["level"])+"gold per day but also produces "+str(member["level"])+" supplies per day",is_crewmember = True)
        elif member["role"] == "Brute":
            return ui_helper.popup_window(type=1, caption="Info",text="Increases victory chance in battly by " + str(member["level"]) + "%",is_crewmember = True)
        self.write_crew()
        self.screen.blit(ui_helper.draw_crew_overview(), (0, 0))
        return None

    def advance_tick(self):
        self.current_tick += 1
        print("now at gametick" + str(self.current_tick))
        for member in self.crew:
            if "xp" in member.keys():
                member["xp"] += 1
                if member["xp"] >= member["level"]:
                    member["xp"] = 0
                    member["level"] += 1
        for member in self.crew:
            if "is_in_action" in member.keys():
                if member["is_in_action"] == True:
                    print(self.current_tick)
                    if "finish_tick" in member.keys():
                        print(member["finish_tick"])
                    if member["finish_tick"] <= self.current_tick:
                        if member["role"] == "Doctor":
                            print("finding healed")
                            for target in self.crew:
                                if target["uID"] == member["target_id"]:
                                    print("found healer")
                                    print(target)
                                    target["injured"] = False
                                    break
                        elif member["role"] == "Carpenter":
                            print("fixing")
                            if self.ship_HP < self.max_ship_HP:
                                self.ship_HP += 1
                            elif (self.ship_HP+1) <= member["level"]:
                                print("overhealing")
                                self.ship_HP+=1
                                self.max_ship_HP+=1
                        member["xp"] += 1
                        member["is_in_action"] = False
            else:
                member["is_in_action"] = False
        for member in self.crew:
            if member["role"] == "Cook":
                if self.gold < member["level"]:
                    self.supplies -= member["level"]*2
                else:
                    self.gold -= member["level"]
                    self.supplies+=member["level"]
            else:
                self.supplies-=member["level"]
        if self.gold<0:
            self.gold = 0
        print(self.supplies)
        self.write_crew()

    def update_screen(self,screen):
        self.screen = screen

    def recruit(self,crewmember):
        img_path = os.path.join(os.getcwd(),"data","img")
        img_base = Image.open(os.path.join(img_path, "crew", "base", crew_img_list[0][random.randint(0, 3)]))
        img_face = Image.open(os.path.join(img_path, "crew", "face", crew_img_list[1][random.randint(0, 10)]))
        img_head = Image.open(os.path.join(img_path, "crew", "head", crew_img_list[2][random.randint(0, 7)]))
        img_base.paste(img_face, (0, 0), img_face)
        img_base.paste(img_head, (0, 0), img_head)
        img_base.save(os.path.join(img_path, "crew_faces", crewmember["uID"] + ".png"))
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
        if self.sound_state == 1:
            start_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), "data", "sound", "scream.wav"))
            start_sound.set_volume(0.1)
            pygame.mixer.Sound.play(start_sound)
        self.crew.remove(crew_member)
        self.write_crew()
        self.screen.blit(ui_helper.draw_crew_overview(), (0, 0))

    def crew_has_space(self):
        if len(self.crew)!=8:
            return True
        return False

    def heal_crewmember(self,target,source):
        for member in self.crew:
            if member["uID"]==source:
                member["is_in_action"] = True
                member["target_id"] = target["uID"]
                if member["level"]>=target["level"]:
                    member["finish_tick"] = self.current_tick+1
                else:
                    member["finish_tick"] = self.current_tick + (target["level"]-member["level"])
                break
        self.write_crew()
        if self.sound_state == 1:
            start_sound = pygame.mixer.Sound(os.path.join(os.getcwd(),"data","sound","job_start.mp3"))
            start_sound.set_volume(0.5)
            pygame.mixer.Sound.play(start_sound)
        print("healing initiated")