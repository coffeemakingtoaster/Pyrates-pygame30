import pygame
import os
import json
import sys

#returns surface with bars for all resources and a gold icon
def draw_resources(current_savegame):
    asset_path = os.path.join(os.getcwd(), "data", "img")
    text_color = (0, 0, 0)
    ammunition_values, max_ammunition = current_savegame.get_ammunition()
    supplies_values, max_supply = current_savegame.get_supplies()
    ship_HP, max_ship_HP = current_savegame.get_ship_HP()
    gold = current_savegame.get_gold_value()
    #create the bars and load font
    values_text = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Carlito-Regular.ttf"), 30)
    supplies_bar_basis = pygame.Rect(50, 100, 250, 30)
    supplies_bar_filled = pygame.Rect(50, 100, (supplies_values / max_supply) * 250, 30)  ##
    ammunition_bar_basis = pygame.Rect(50, 200, 250, 30)
    ammunition_bar_filled = pygame.Rect(50, 200, (ammunition_values / max_ammunition) * 250, 30)  ##
    ship_HP_bar_basis = pygame.Rect(50, 300, 250, 30)
    ship_HP_bar_filled = pygame.Rect(50, 300, (ship_HP / max_ship_HP) * 250, 30)  ##
    #render Text
    supplies_title_render = values_text.render("Supplies:",False,text_color)
    supplies_text_render = values_text.render(str(supplies_values) + "/" + str(max_supply), False, text_color)
    ammunition_title_render = values_text.render("Ammunition:", False, text_color)
    ammunition_text_render = values_text.render(str(ammunition_values) + "/" + str(max_ammunition), False, text_color)
    ship_HP_title_render = values_text.render("Ship HP:", False, text_color)
    HP_text_render = values_text.render(str(ship_HP) + "/" + str(max_ship_HP), False, text_color)
    gold_render = values_text.render(str(gold), False, text_color)
    #draw bars and text onto surface
    values_surf = pygame.Surface((533, 450))
    values_surf.fill((82, 62, 16))
    values_surf.blit(supplies_title_render,(50,115-50))
    pygame.draw.rect(values_surf, (107, 86, 28), supplies_bar_basis)
    pygame.draw.rect(values_surf, (58, 235, 52), supplies_bar_filled)
    values_surf.blit(supplies_text_render, supplies_text_render.get_rect(center=(400, 115)))
    values_surf.blit(ammunition_title_render, (50, 215 - 50))
    pygame.draw.rect(values_surf, (107, 86, 28), ammunition_bar_basis)
    pygame.draw.rect(values_surf, (52, 101, 235), ammunition_bar_filled)
    values_surf.blit(ammunition_text_render, ammunition_text_render.get_rect(center=(400, 215)))
    values_surf.blit(ship_HP_title_render, (50, 315 - 50))
    pygame.draw.rect(values_surf, (107, 86, 28), ship_HP_bar_basis)
    pygame.draw.rect(values_surf, (255, 0, 25), ship_HP_bar_filled)
    values_surf.blit(HP_text_render, HP_text_render.get_rect(center=(400, 315)))
    gold_rect = gold_render.get_rect(center=(533 / 2, 400))
    gold_icon = pygame.image.load(os.path.join(asset_path, "coin.png"))
    values_surf.blit(gold_render, gold_rect)
    values_surf.blit(pygame.transform.scale(gold_icon, (50, 50)), ((533 / 2) + (gold_rect.width / 2) + 20, 375))
    return values_surf


#class used for creating popup window
#takes type as parameter (and event values depending on type)
#apart from displaying said window this also provides collisioncheck with the buttons and handles their functionality

class popup_window():

    # Types:
    # 1 - Status Update (just OK button)
    # 2 - Battlescreen (Fight and Flee button)
    # 3 - Recruitscreen (Recruit and Leave here)
    # 4 - Abandonscreen (yes and no)
    # 5 - PauseScreen (Resume,Save,Save and Exit)
    # 6 - GameOver  (MM, Quit)
    def __init__(self, type,caption=None,text=None,event_values = None,crew = None):
        self.state = False
        pygame.font.init()
        self.caption_size = 70
        self.text_size = 25
        self.popup_background = (82, 62, 16)
        self.caption_color = (196, 33, 0)
        self.text_color = (207, 187, 39)
        self.window_size = (400, 300)
        self.Caption = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Avara.ttf"), self.caption_size)
        self.message_text = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Carlito-Regular.ttf"),self.text_size)
        self.offset_x = 0
        self.offset_y = 0
        if event_values:
            self.event_values = event_values
        if type==1:
            self.init_status_update(caption,text)
        elif type==2:
            self.init_battle_screen(event_values)
        elif type==3:
            self.init_recruit_screen(event_values,crew)
        elif type==4:
            self.init_yes_no_screen()
        elif type==5:
            self.init_pause_screen()
        elif type==6:
            self.init_game_over_screen(text)
        elif type==7:
            self.page = 0
            self.init_heal_crew_member()

    def init_heal_crew_member(self):
        self.state = True
        self.buttons =[]
        f = open(os.path.join(os.getcwd(), "data", "savegame", "crew.json"))
        crew = json.load(f)
        f.close()
        wounded_count = 0
        for member in crew:
            if member["injured"] == True:
                wounded_count+=1
        #crew_overview_surface = pygame.Surface((400, 200+(wounded_count*50)))
        crew_overview_surface = pygame.Surface((400, 300))
        crew_overview_surface.fill((217, 141, 0))
        caption_render = self.Caption.render("Heal", False, (196, 33, 0))
        caption_rect = caption_render.get_rect(center=(200, 50))
        crew_overview_surface.blit(caption_render, caption_rect)
        index = 0
        cnt = 0
        for member in crew:
            if member["injured"] == True:
                cnt+=1
            if member["injured"] == True and (self.page*4)<cnt<(self.page*4+4):
                if member["level"]<=self.event_values["level"]:
                    duration = 1
                else:
                    duration = member["level"] - self.event_values["level"]
                display_text = member["name"] + " Lvl:" + str(member["level"]) + " Role:" + member["role"] +"("+str(duration)+" days)"
                display_text_render = self.message_text.render(display_text, False, (0, 0, 0))
                display_text_rect = display_text_render.get_rect(center=(200,100+(index*50)))
                crew_overview_surface.blit(display_text_render, display_text_rect)
                self.buttons.append({"button_text":"heal","hitbox":display_text_rect,"crew_member":member})
                index += 1
        next_page_button_render = self.message_text.render(">", False, self.text_color)
        next_page_button_rect = next_page_button_render.get_rect(center=((self.window_size[0]/4)*3, 250))
        previous_page_button_render = self.message_text.render("<", False, self.text_color)
        previous_page_button_rect = previous_page_button_render.get_rect(center=((self.window_size[0] / 4), 250))
        Cancel_button_render = self.message_text.render("Cancel", False, self.text_color)
        Cancel_button_rect = Cancel_button_render.get_rect(center=((self.window_size[0]/4)*2, 250))
        crew_overview_surface.blit(Cancel_button_render,Cancel_button_rect)
        crew_overview_surface.blit(next_page_button_render,next_page_button_rect)
        crew_overview_surface.blit(previous_page_button_render, previous_page_button_rect)
        self.buttons.append({"button_text":"Cancel","hitbox":Cancel_button_rect})
        self.buttons.append({"button_text": "Next", "hitbox": next_page_button_rect})
        self.buttons.append({"button_text":"Previous", "hitbox":previous_page_button_rect})
        self.surf = crew_overview_surface

    def init_game_over_screen(self,text):
        self.state = True
        surf = pygame.Surface(self.window_size)
        surf.fill(self.popup_background)
        caption_render = self.Caption.render("Game Over!", False, self.caption_color)
        caption_rec = caption_render.get_rect(center=(self.window_size[0] / 2, 65))
        i = 0
        while i < len(text):
            print(i)
            if (i + 25) > len(text):
                text_to_print = text[i:len(text)]
            else:
                text_to_print = text[i:i + 25]
            print(text_to_print)
            text_render = self.message_text.render(text_to_print, False, (0, 0, 0))
            text_rect = caption_render.get_rect(center=(200, (self.window_size[1] / 2) + (50 * (i / 20))))
            surf.blit(text_render, text_rect)
            i += 25
        MM_button_render = self.message_text.render("Main Menu", False, self.text_color)
        MM_button_rect = MM_button_render.get_rect(center=(self.window_size[0] / 3, 265))
        Quit_button_render = self.message_text.render("Quit", False, self.text_color)
        Quit_button_rect = MM_button_render.get_rect(center=((self.window_size[0] / 3)*2, 265))
        surf.blit(caption_render, caption_rec)
        surf.blit(text_render, text_rect)
        pygame.draw.rect(surf, (0, 0, 0), MM_button_rect)
        pygame.draw.rect(surf, (0, 0, 0), Quit_button_rect)
        surf.blit(MM_button_render, MM_button_rect)
        surf.blit(Quit_button_render, Quit_button_rect)
        self.buttons = [{"button_text": "MM", "hitbox": MM_button_rect},{"button_text":"Quit","hitbox":Quit_button_rect}]
        self.surf = surf

    def init_pause_screen(self):
        self.window_size = (400,400)
        self.state = True
        surf = pygame.Surface(self.window_size)
        surf.fill(self.popup_background)
        caption_render = self.Caption.render("Pause", False, self.caption_color)
        caption_rec = caption_render.get_rect(center=(self.window_size[0] / 2, 65))
        resume_button = self.message_text.render("Resume",False,(0,0,0))
        save_button = self.message_text.render("Save game",False,(0,0,0))
        quit_button = self.message_text.render("Save and Quit",False,(0,0,0))
        resume_button_rect = resume_button.get_rect(center=(self.window_size[0]/2,125))
        save_button_rect = save_button.get_rect(center=(self.window_size[0]/2,225))
        quit_button_rect = quit_button.get_rect(center=(self.window_size[0]/2,325))
        pygame.draw.rect(surf, self.caption_color, resume_button_rect)
        pygame.draw.rect(surf, self.caption_color, save_button_rect)
        pygame.draw.rect(surf, self.caption_color, quit_button_rect)
        surf.blit(caption_render,caption_rec)
        surf.blit(resume_button,resume_button_rect)
        surf.blit(save_button,save_button_rect)
        surf.blit(quit_button,quit_button_rect)
        self.buttons = [{"button_text": "Resume", "hitbox": resume_button_rect},{"button_text": "Save", "hitbox": save_button_rect},{"button_text":"Exit","hitbox":quit_button_rect}]
        self.surf = surf

    def init_yes_no_screen(self):
        self.state = True
        surf = pygame.Surface(self.window_size)
        surf.fill(self.popup_background)
        caption_render = self.Caption.render("Castaway", False, self.caption_color)
        caption_rec = caption_render.get_rect(center=(self.window_size[0] / 2, 65))
        text_render_1 = self.message_text.render("Are you sure you want", False, (0, 0, 0))
        text_render_2 = self.message_text.render("to abandon:", False, (0, 0, 0))
        name_render = self.message_text.render(self.event_values["name"]+"(Lvl:"+str(self.event_values["level"])+" "+str(self.event_values["role"])+")", False, (255, 0, 25))
        text_render_1_rect = text_render_1.get_rect(center=(self.window_size[0] / 2, 100))
        text_render_2_rect = text_render_2.get_rect(center=(self.window_size[0] / 2, 125))
        name_render_rect = name_render.get_rect(center=(self.window_size[0] / 2,175))
        castaway_button_render = self.message_text.render("Castaway", False, self.text_color)
        keep_button_render = self.message_text.render("Keep", False, self.text_color)
        castaway_button_rect = castaway_button_render.get_rect(center=(self.window_size[0] / 3, 265))
        keep_button_rect = keep_button_render.get_rect(center=((self.window_size[0] / 3)*2, 265))
        surf.blit(caption_render, caption_rec)
        surf.blit(text_render_1, text_render_1_rect)
        surf.blit(text_render_2, text_render_2_rect)
        surf.blit(name_render, name_render_rect)
        pygame.draw.rect(surf, (0, 0, 0), castaway_button_rect)
        surf.blit(castaway_button_render, castaway_button_rect)
        pygame.draw.rect(surf, (0, 0, 0), keep_button_rect)
        surf.blit(keep_button_render, keep_button_rect)
        self.buttons = [{"button_text": "Dispatch", "hitbox": castaway_button_rect},{"button_text":"Keep","hitbox":keep_button_rect}]
        self.surf = surf

    # a recruitment screen that shows stats of found crewmember and gives you the option of recruiting or ignoring
    def init_recruit_screen(self,event_values,crew):
        self.state = True
        surf = pygame.Surface(self.window_size)
        self.Caption = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Avara.ttf"), 40)
        surf.fill(self.popup_background)
        caption_render = self.Caption.render("Castaway found", False, self.caption_color)
        caption_rec = caption_render.get_rect(center=(self.window_size[0] / 2, 65))

        castaway_name_render = self.message_text.render(event_values["castaway"]["name"],False,self.text_color)
        castaway_level_render = self.message_text.render("Lvl: "+str(event_values["castaway"]["level"]),False,self.text_color)
        castaway_role_render =  self.message_text.render("Role: "+str(event_values["castaway"]["role"]),False,self.text_color)

        surf.blit(castaway_name_render,castaway_name_render.get_rect(center=(self.window_size[0] / 2, 100)))
        surf.blit(castaway_level_render,castaway_level_render.get_rect(center=(self.window_size[0] / 2, 150)))
        surf.blit(castaway_role_render, castaway_role_render.get_rect(center=(self.window_size[0] / 2, 200)))

        recruit_button_render = self.message_text.render("Recruit", False,self.text_color)
        recruit_button_rect = recruit_button_render.get_rect(center=(self.window_size[0] / 3, 265))
        leave_button_render = self.message_text.render("Abandon", False, self.text_color)
        leave_button_rect = leave_button_render.get_rect(center=((self.window_size[0] / 3) * 2, 265))
        surf.blit(caption_render, caption_rec)
        if (len(crew)>=8):
            pygame.draw.rect(surf, (150, 150, 150), recruit_button_rect)
        else:
            pygame.draw.rect(surf, (0, 0, 0), recruit_button_rect)
        surf.blit(recruit_button_render, recruit_button_rect)
        pygame.draw.rect(surf, (0, 0, 0), leave_button_rect)
        surf.blit(leave_button_render, leave_button_rect)
        self.buttons = [{"button_text": "Recruit!", "hitbox": recruit_button_rect},{"button_text": "Abandon", "hitbox": leave_button_rect}]
        self.surf = surf

    #battle screen features a fight and a flee button and on the fight button the win percentage is displayed
    def init_battle_screen(self,event_values):
         self.state = True
         surf = pygame.Surface(self.window_size)
         surf.fill(self.popup_background)
         caption_render = self.Caption.render("BATTLE", False, self.caption_color)
         caption_rec = caption_render.get_rect(center=(self.window_size[0] / 2, 65))
         fight_button_render = self.message_text.render("Fight! ("+str(event_values["victory"])+"%)", False, self.text_color)
         fight_button_rect = fight_button_render.get_rect(center=(self.window_size[0] / 3, 265))
         flee_button_render = self.message_text.render("Flee", False,self.text_color)
         flee_button_rect = flee_button_render.get_rect(center=((self.window_size[0] / 3)*2, 265))
         surf.blit(caption_render, caption_rec)
         pygame.draw.rect(surf, (0, 0, 0), fight_button_rect)
         surf.blit(fight_button_render, fight_button_rect)
         pygame.draw.rect(surf, (0, 0, 0), flee_button_rect)
         surf.blit(flee_button_render, flee_button_rect)
         self.buttons = [{"button_text": "Flee", "hitbox": flee_button_rect},{"button_text":"Battle","hitbox":fight_button_rect}]
         self.surf = surf

    #status update displays changes of stats and therefore only features okay button
    def init_status_update(self,title,text):
        self.state = True
        surf = pygame.Surface(self.window_size)
        surf.fill(self.popup_background)
        caption_render = self.Caption.render(title, False, self.caption_color)
        caption_rec = caption_render.get_rect(center=(self.window_size[0] / 2, 65))
        i = 0
        while i < len(text):
            print(i)
            if (i+25)>len(text):
                text_to_print = text[i:len(text)]
            else:
                text_to_print = text[i:i+25]
            print(text_to_print)
            text_render = self.message_text.render(text_to_print, False, (0, 0, 0))
            text_rect = caption_render.get_rect(center=(200, (self.window_size[1] / 2)+(50*(i/20))))
            surf.blit(text_render, text_rect)
            i += 25
        button_render = self.message_text.render("OK", False, self.text_color)
        button_rect = button_render.get_rect(center=(self.window_size[0] / 2, 265))
        surf.blit(caption_render, caption_rec)
        surf.blit(text_render, text_rect)
        pygame.draw.rect(surf,(0,0,0),button_rect)
        surf.blit(button_render, button_rect)
        self.buttons = [{"button_text":"OK","hitbox":button_rect}]
        self.surf = surf

    #get object surface
    def get_surf(self):
        return self.surf

    #set offset for calculting button hitboxes
    def set_offset(self,x,y):
        self.offset_x = x-(self.window_size[0]/2)
        self.offset_y = y-(self.window_size[1]/2)

    #given a mouse pos - here is calculated if mouse collides with button and if so functionality is given
    def is_collide(self,mouse_pos,screen,game):
        print("checking")
        mouse_x, mouse_y = mouse_pos
        mouse_pos = (mouse_x-self.offset_x,mouse_y-self.offset_y)
        for button in self.buttons:
            print(mouse_pos)
            print(button["hitbox"].center)
            if button["hitbox"].collidepoint(mouse_pos):
                print(button)
                if button["button_text"]=="OK":
                    print("OK")
                    self.delete_popup(screen,game)
                    self.surf = None
                    self.state = False
                elif button["button_text"]=="Battle":
                    outcome,details = game.battle(self.event_values)
                    self.delete_popup(screen,game)
                    self.init_status_update(outcome,details)
                elif button["button_text"]=="Flee" or button["button_text"]=="Abandon" or button["button_text"]=="Keep" or button["button_text"]=="Resume" or button["button_text"]=="Cancel":
                    print("we out")
                    self.delete_popup(screen, game)
                    self.surf = None
                    self.state = False
                elif button["button_text"]=="Recruit!":
                    print("recruting")
                    game.recruit(self.event_values["castaway"])
                    self.delete_popup(screen,game)
                    self.surf = None
                    self.state = False
                elif button["button_text"]=="Dispatch":
                    game.dispatch(self.event_values)
                    self.delete_popup(screen, game)
                    self.surf = None
                    self.state = False
                elif button["button_text"]=="Save" or button["button_text"]=="Exit":
                    game.write_savegame()
                    if button["button_text"] == "Exit":
                        sys.exit(0)
                    self.delete_popup(screen, game)
                    self.surf = None
                    self.state = False
                elif button["button_text"] == "Quit":
                    sys.exit(1)
                elif button["button_text"] == "MM":
                    self.surf = None
                    self.state = False
                elif button["button_text"] == "heal":
                    print("healing")
                    game.heal_crewmember(button["crew_member"],self.event_values["uID"])
                    self.delete_popup(screen, game)
                    self.surf = None
                    self.state = False
                    print("all clear")
                elif button["button_text"] == "Next":
                    self.page +=1
                    self.init_heal_crew_member()
                elif button["button_text"] == "Previous":
                    self.page -=1
                    self.init_heal_crew_member()
                return True
        print("no matching button found")
        return False

    #get alive state of object
    def is_active(self):
        return self.state

    #hides popup
    def delete_popup(self,screen,game):
        width,height = pygame.display.get_surface().get_size()
        screen.blit(draw_resources(game), (533, 450))
        screen.blit(draw_crew_overview(), (0, 0))
        ship_visual = pygame.Rect(width / 3, 0, width / 3, height / 2)
        pygame.draw.rect(screen, (0, 0, 0), ship_visual)
        self.state = False

#generates shop interface based on values that are generated in generator.py
class shop():
    def __init__(self,values = None,player_gold=None):
        if values and player_gold:
            self.state = True
            self.values = values
            self.player_gold = player_gold
            self.draw_shop(values)

    #draws the shop onto surface
    def draw_shop(self,values):
        active_color = (199, 104, 2)
        inactive_color = (125, 88, 47)
        asset_path = os.path.join(os.getcwd(), "data", "img")
        self.shop_surface = pygame.Surface((533, 900))
        self.shop_surface.fill((173, 90, 0))
        caption = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Avara.ttf"), 50)
        text = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Carlito-Regular.ttf"), 30)
        caption_render = caption.render("The Shop", False, (196, 33, 0))
        caption_rect = caption_render.get_rect(center=(533 / 2, 50))
        self.shop_surface.blit(caption_render, caption_rect)
        gold_icon = pygame.image.load(os.path.join(asset_path, "coin.png"))
        index = 0
        self.items = []
        if values["supplies"]["amount"]>0:
            color = active_color
            if values["supplies"]["price"]>self.player_gold:
                color = inactive_color
            amount_rect = pygame.Rect(50,100+(index*150),400,100)
            pygame.draw.rect(self.shop_surface,color,amount_rect)
            amount_render = text.render(str(values["supplies"]["amount"])+"x",False,(0,0,0))
            price_render = text.render(str(values["supplies"]["price"]),False,(0,0,0))
            supply_icon = pygame.image.load(os.path.join(asset_path, "supplies.png"))
            amount_pos_x,amount_pos_y = amount_rect.center
            self.shop_surface.blit(amount_render,(amount_pos_x-50,amount_pos_y-10))
            self.shop_surface.blit(price_render,(amount_pos_x+50,amount_pos_y-10))
            self.shop_surface.blit(pygame.transform.scale(supply_icon, (50, 50)), (100, (amount_rect.centery - 25)))
            self.shop_surface.blit(pygame.transform.scale(gold_icon, (50, 50)),(370,(amount_rect.centery-25)))
            self.items.append({"item":"supplies","hitbox":amount_rect})
            index+=1
        if values["ammunition"]["amount"]>0:
            color = active_color
            if values["ammunition"]["price"] > self.player_gold:
                color = inactive_color
            amount_rect = pygame.Rect(50,100+(index*150),400,100)
            amount_pos_x, amount_pos_y = amount_rect.center
            pygame.draw.rect(self.shop_surface,color,amount_rect)
            amount_render = text.render(str(values["ammunition"]["amount"])+"x",False,(0,0,0))
            price_render = text.render(str(values["ammunition"]["price"]),False,(0,0,0))
            ammunition_icon = pygame.image.load(os.path.join(asset_path, "ammunition.png"))
            self.shop_surface.blit(amount_render,(amount_pos_x-50,amount_pos_y-10))
            self.shop_surface.blit(price_render,(amount_pos_x+50,amount_pos_y-10))
            self.shop_surface.blit(pygame.transform.scale(ammunition_icon, (50, 50)), (100, (amount_rect.centery - 25)))
            self.shop_surface.blit(pygame.transform.scale(gold_icon, (50, 50)),(370,(amount_rect.centery-25)))
            self.items.append({"item": "ammunition", "hitbox": amount_rect})
            index += 1
        if values["bonus"]["amount"]>0:
            color = active_color
            if values["bonus"]["price"] > self.player_gold:
                color = inactive_color
            amount_rect = pygame.Rect(50,100+(index*150),400,100)
            amount_pos_x, amount_pos_y = amount_rect.center
            pygame.draw.rect(self.shop_surface,color,amount_rect)
            amount_render = text.render(str(values["bonus"]["amount"])+"x",False,(0,0,0))
            price_render = text.render(str(values["bonus"]["price"]),False,(0,0,0))
            self.shop_surface.blit(amount_render,(amount_pos_x-50,amount_pos_y-10))
            self.shop_surface.blit(price_render,(amount_pos_x+50,amount_pos_y-10))
            self.shop_surface.blit(pygame.transform.scale(gold_icon, (50, 50)),(370,(amount_rect.centery-25)))
            self.items.append({"item": values["bonus"]["name"], "hitbox": amount_rect})
            index += 1
        exit_icon = pygame.image.load(os.path.join(asset_path,"x_button.png"))
        self.leave_rect = pygame.Rect(400, 800, 50, 50)
        #pygame.draw.rect(self.shop_surface, (255, 0, 0), self.leave_rect)
        self.shop_surface.blit(pygame.transform.scale(exit_icon, (50, 50)), (400,800))

    #returns obj surface
    def get_surface(self):
        return self.shop_surface

    #equivalent to popup collide
    def interact(self,mouse_pos):
        if self.leave_rect.collidepoint(mouse_pos):
            self.state = False
            return None,None
        for button in self.items:
            if button["hitbox"].collidepoint(mouse_pos):
                print(self.values)
                item = button["item"]
                print(item)
                if button["item"] == "ammunition" or button["item"]=="supplies":
                    price = self.values[button["item"]]["price"]
                    if price>self.player_gold:
                        self.draw_shop(self.values)
                        return None,None
                    self.values[button["item"]]["amount"]-=1
                else:
                    price = self.values["bonus"]["price"]
                    if price>self.player_gold:
                        self.draw_shop(self.values)
                        return None,None
                    self.values["bonus"]["amount"]-= 1
                self.draw_shop(self.values)
                self.player_gold -= price
                return item,price

        return None,None

    #get alive state of shop
    def is_active(self):
        return self.state


# draw crew including status
# returns surface
def draw_crew_overview():
    f = open(os.path.join(os.getcwd(), "data", "savegame", "crew.json"))
    crew = json.load(f)
    f.close()
    crew_overview_surface = pygame.Surface((533, 900))
    crew_overview_surface.fill((217, 141, 0))
    Caption = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Avara.ttf"), 50)
    text = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Carlito-Regular.ttf"), 20)
    caption_render = Caption.render("Your Crew", False, (196, 33, 0))
    caption_rect = caption_render.get_rect(center=(533 / 2, 50))
    crew_overview_surface.blit(caption_render, caption_rect)
    index = 0
    for member in crew:
        if "xp" not in member.keys():
            member["xp"] = 0
        display_text = member["name"] + " Lvl:" + str(member["level"]) + "(" + str(member["xp"]) + "/" + str(member["level"]) + "XP) Role:" + member["role"]
        display_text_render = text.render(display_text, False, (0, 0, 0))
        if "status" in member.keys():
            print(member["injured"])
            if member["status"] != None:
                if member["status"] == "hungry":
                    icon = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "status_hungry.png"))
                crew_overview_surface.blit(pygame.transform.scale(icon, (100, 33)), (400, 130 + (index * 100)))
        if member["injured"]:
            icon = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "status_injured.png"))
            crew_overview_surface.blit(pygame.transform.scale(icon, (100, 33)), (225, 130 + (index * 100)))
        if member["role"] == "Doctor" or member["role"] == "Carpenter":
            if "is_in_action" in member.keys():
                ability_icon = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "status_work.png"))
                if member["is_in_action"] == True:
                    ability_icon = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "status_busy.png"))
        else:
            ability_icon = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "status_boosting.png"))
        crew_overview_surface.blit(pygame.transform.scale(ability_icon, (100, 33)), (100, 130 + (index * 100)))
        castaway_icon = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "x_button.png"))
        crew_overview_surface.blit(pygame.transform.scale((castaway_icon),(40,40)),(475, 100 + (index * 100)))
        crew_overview_surface.blit(display_text_render, (100, 100 + (index * 100)))
        crew_face = pygame.image.load(os.path.join(os.getcwd(), "data", "img","crew_faces",str(member["uID"])+".png"))
        crew_overview_surface.blit(pygame.transform.scale((crew_face),(50,50)),(25,100 + (index * 100)))
        index += 1
    return crew_overview_surface
