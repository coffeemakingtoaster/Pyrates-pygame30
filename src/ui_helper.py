import pygame
import os
import json


def draw_resources(current_savegame):
    asset_path = os.path.join(os.getcwd(), "data", "img")
    text_color = (0, 0, 0)
    ammunition_values, max_ammunition = current_savegame.get_ammunition()
    supplies_values, max_supply = current_savegame.get_supplies()
    ship_HP, max_ship_HP = current_savegame.get_ship_HP()
    gold = current_savegame.get_gold_value()
    values_text = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Carlito-Regular.ttf"), 30)
    supplies_bar_basis = pygame.Rect(50, 100, 250, 30)
    supplies_bar_filled = pygame.Rect(50, 100, (supplies_values / max_supply) * 250, 30)  ##
    ammunition_bar_basis = pygame.Rect(50, 200, 250, 30)
    ammunition_bar_filled = pygame.Rect(50, 200, (ammunition_values / max_ammunition) * 250, 30)  ##
    ship_HP_bar_basis = pygame.Rect(50, 300, 250, 30)
    ship_HP_bar_filled = pygame.Rect(50, 300, (ship_HP / max_ship_HP) * 250, 30)  ##
    supplies_text_render = values_text.render(str(supplies_values) + "/" + str(max_supply), False, text_color)
    ammunition_text_render = values_text.render(str(ammunition_values) + "/" + str(max_ammunition), False, text_color)
    HP_text_render = values_text.render(str(ship_HP) + "/" + str(max_ship_HP), False, text_color)
    gold_render = values_text.render(str(gold), False, text_color)
    values_surf = pygame.Surface((533, 450))
    values_surf.fill((82, 62, 16))
    pygame.draw.rect(values_surf, (107, 86, 28), supplies_bar_basis)
    pygame.draw.rect(values_surf, (255, 0, 25), supplies_bar_filled)
    values_surf.blit(supplies_text_render, supplies_text_render.get_rect(center=(400, 115)))
    pygame.draw.rect(values_surf, (107, 86, 28), ammunition_bar_basis)
    pygame.draw.rect(values_surf, (255, 0, 25), ammunition_bar_filled)
    values_surf.blit(ammunition_text_render, ammunition_text_render.get_rect(center=(400, 215)))
    pygame.draw.rect(values_surf, (107, 86, 28), ship_HP_bar_basis)
    pygame.draw.rect(values_surf, (255, 0, 25), ship_HP_bar_filled)
    values_surf.blit(HP_text_render, HP_text_render.get_rect(center=(400, 315)))
    gold_rect = gold_render.get_rect(center=(533 / 2, 400))
    gold_icon = pygame.image.load(os.path.join(asset_path, "coin.png"))
    values_surf.blit(gold_render, gold_rect)
    values_surf.blit(pygame.transform.scale(gold_icon, (50, 50)), ((533 / 2) + (gold_rect.width / 2) + 20, 375))
    return values_surf

class popup_window():
    # Types:
    # 1 - Status Update (just OK button)
    #
     def __init__(self, type,caption,text,event_values = None):
        self.state = False
        pygame.font.init()
        self.caption_size = 70
        self.text_size = 40
        self.popup_background = (82, 62, 16)
        self.caption_color = (196, 33, 0)
        self.text_color = (207, 187, 39)
        self.window_size = (400, 300)
        self.Caption = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Avara.ttf"), self.caption_size)
        self.message_text = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Carlito-Regular.ttf"),self.text_size)
        if event_values:
            self.event_values = event_values
        if type==1:
            self.init_status_update(caption,text)
        elif type==2:
            pass

     def init_status_update(self,title,text):
         self.state = True
         i = 20
         '''
         while i < len(text):
             text = text[i] + "\n" + text[i + 1]
             i + 20
         '''
         surf = pygame.Surface(self.window_size)
         surf.fill(self.popup_background)
         caption_render = self.Caption.render(title, False, self.caption_color)
         caption_rec = caption_render.get_rect(center=(self.window_size[0] / 2, 65))
         text_render = self.message_text.render(text, False, (0,0,0))
         text_rect = caption_render.get_rect(center=(125, (self.window_size[1] / 2)))
         button_render = self.message_text.render("OK", False, self.text_color)
         button_rect = button_render.get_rect(center=(self.window_size[0] / 2, 245))
         surf.blit(caption_render, caption_rec)
         surf.blit(text_render, text_rect)
         surf.blit(button_render, button_rect)
         self.buttons = [{"button_text":"OK","hitbox":button_rect}]
         self.surf = surf

     def get_surf(self):
         return self.surf


     def is_collide(self,mouse_pos,screen,game):
         for button in self.buttons:
             if button["hitbox"].collidepoint(mouse_pos):
                 if button["button_text"]=="OK":
                     self.delete_popup(screen,game)
                 elif button["button_text"]=="Battle":
                    outcome,details = game.battle(self.event_values)
                    self.delete_popup()
                    self.init_status_update(outcome,details)
                 elif button["buttton_text"]=="Flee":
                    self.delete_popup()

                 return True
         return False

     def is_active(self):
         return self.state

     def delete_popup(self,screen,game):
         width,height = pygame.display.get_surface().get_size()
         screen.blit(draw_resources(game), (533, 450))
         screen.blit(draw_crew_overview(), (0, 0))
         ship_visual = pygame.Rect(width / 3, 0, width / 3, height / 2)
         pygame.draw.rect(screen, (0, 0, 0), ship_visual)
         self.state = False


class shop():
    def __init__(self,values = None,player_gold=None):
        if values and player_gold:
            self.state = True
            self.values = values
            self.player_gold = player_gold
            self.draw_shop(values)

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
            amount_render = text.render(str(values["supplies"]["amount"]),False,(0,0,0))
            price_render = text.render(str(values["supplies"]["price"]),False,(0,0,0))
            self.shop_surface.blit(amount_render,amount_render.get_rect(center=amount_rect.center))
            self.shop_surface.blit(price_render,(325,amount_rect.centery-20))
            self.shop_surface.blit(pygame.transform.scale(gold_icon, (50, 50)),(370,(amount_rect.centery-25)))
            self.items.append({"item":"supplies","hitbox":amount_rect})
            index+=1
        if values["ammunition"]["amount"]>0:
            color = active_color
            if values["ammunition"]["price"] > self.player_gold:
                color = inactive_color
            amount_rect = pygame.Rect(50,100+(index*150),400,100)
            pygame.draw.rect(self.shop_surface,color,amount_rect)
            amount_render = text.render(str(values["ammunition"]["amount"]),False,(0,0,0))
            price_render = text.render(str(values["ammunition"]["price"]),False,(0,0,0))
            self.shop_surface.blit(amount_render,amount_render.get_rect(center=amount_rect.center))
            self.shop_surface.blit(price_render,(325,amount_rect.centery-20))
            self.shop_surface.blit(pygame.transform.scale(gold_icon, (50, 50)),(370,(amount_rect.centery-25)))
            self.items.append({"item": "ammunition", "hitbox": amount_rect})
            index += 1
        if values["bonus"]["amount"]>0:
            color = active_color
            if values["bonus"]["price"] > self.player_gold:
                color = inactive_color
            amount_rect = pygame.Rect(50,100+(index*150),400,100)
            pygame.draw.rect(self.shop_surface,color,amount_rect)
            amount_render = text.render(str(values["bonus"]["amount"]),False,(0,0,0))
            price_render = text.render(str(values["bonus"]["price"]),False,(0,0,0))
            self.shop_surface.blit(amount_render,amount_render.get_rect(center=amount_rect.center))
            self.shop_surface.blit(price_render,(325,amount_rect.centery-20))
            self.shop_surface.blit(pygame.transform.scale(gold_icon, (50, 50)),(370,(amount_rect.centery-25)))
            self.items.append({"item": values["bonus"]["name"], "hitbox": amount_rect})
            index += 1
        self.leave_rect = pygame.Rect(400,800,50,50)
        pygame.draw.rect(self.shop_surface,(255,0,0),self.leave_rect)

    def get_surface(self):
        return self.shop_surface

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

    def is_active(self):
        return self.state



def draw_crew_overview():
    f = open(os.path.join(os.getcwd(), "data", "savegame", "crew.json"))
    crew = json.load(f)
    f.close()
    crew_overview_surface = pygame.Surface((533, 900))
    crew_overview_surface.fill((217, 141, 0))
    Caption = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Avara.ttf"), 50)
    text = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Carlito-Regular.ttf"), 30)
    caption_render = Caption.render("Your Crew", False, (196, 33, 0))
    caption_rect = caption_render.get_rect(center=(533 / 2, 50))
    crew_overview_surface.blit(caption_render, caption_rect)
    index = 0
    for member in crew:
        if "xp" not in member.keys():
            member["xp"] = 0
        display_text = member["name"] + " Lvl:" + str(member["level"]) + "(" + str(member["xp"]) + "/" + str(
            member["level"]) + "XP) Role:" + member["role"]
        display_text_render = text.render(display_text, False, (0, 0, 0))
        if "status" in member.keys():
            if member["status"] != None:
                if member["status"] == "hungry":
                    icon = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "status_hungry.png"))
                crew_overview_surface.blit(pygame.transform.scale(icon, (100, 33)), (400, 130 + (index * 100)))
        crew_overview_surface.blit(display_text_render, (50, 100 + (index * 100)))
        index += 1
    return crew_overview_surface
