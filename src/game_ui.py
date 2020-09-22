import pygame
import os
import math
import time
import ui_helper
import game_logic
import map

# given an image and an angle this returns the rotated image
# can directly be drawn to screen



def rotate_image(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def reset_screen(screen,current_game):
    screen.blit(ui_helper.draw_resources(current_game), (533, 450))
    screen.blit(ui_helper.draw_crew_overview(),(0, 0))
    ship_visual = pygame.Rect(width / 3, 0, width / 3, height / 2)
    pygame.draw.rect(screen, (0, 0, 0), ship_visual)

def main():
    pygame.init()
    # init size of the window. The background color is never visible
    width, height = (1600, 900)
    background_color = (0, 0, 0)

    # path to resources (images in this case)
    asset_path = os.path.join(os.getcwd(), "data", "img")

    # init UI elements and provide them with coordinates
    overlay = pygame.image.load(os.path.join(asset_path, "overlay.png"))
    ship = pygame.image.load(os.path.join(asset_path, "ship.png"))
    screen = pygame.display.set_mode((width, height))
    current_game = game_logic.game(screen)
    managment_UI = pygame.Rect(0, 0, width / 3, height)
    ship_visual = pygame.Rect(width / 3, 0, width / 3, height / 2)
    ressource_visual = pygame.Rect(width / 3, height / 2, width / 3, height / 2)
    ship_movement_UI = pygame.Rect((width / 3) * 2, 0, width / 3, height)

    # fill the screen with said elements
    pygame.display.set_caption("Pirate game")
    screen.fill(background_color)
    pygame.draw.rect(screen, (127, 4, 50), managment_UI)
    pygame.draw.rect(screen, (0, 0, 0), ship_visual)
    pygame.draw.rect(screen, (161, 83, 27), ressource_visual)
    pygame.draw.rect(screen, (43, 132, 216), ship_movement_UI)
    screen.blit(ship, (1250, 350))
    screen.blit(overlay, (0, 0))

    # flip displayes everything for the user to see
    pygame.display.flip()

    # gameloop
    running = True
    in_shop = False
    UI_is_blocked = False
    angle = 0
    ship_map_x = 750
    ship_map_y = 350
    dotexists = False
    initx = 0
    inity = 0
    dot_map_x = 0
    dot_map_y = 0
    hitradius = 30
    currentangle = 0
    island_demo_x = 1250
    island_demo_y = 300
    speed = 2
    rotation_speed = 1
    ship_hit_box = pygame.Rect(1340, 440, 20, 20)
    clock = pygame.time.Clock()
    shop = ui_helper.shop(None)


    while running:
        map.mapdraw(ship_map_x,ship_map_y,screen)  
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                running = False
            # at mouseclick:
            # - checks if click was in ship movement window and if so rotates the ship image
            # TODO: add support for more parts of the screen
            if event.type == pygame.MOUSEBUTTONDOWN and ship_movement_UI.collidepoint(pygame.mouse.get_pos()) and not in_shop and not UI_is_blocked:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                initx, inity = pygame.mouse.get_pos()
                dot_map_x = ship_map_x - 266 + mouse_x - 1066
                dot_map_y = 900 - mouse_y + ship_map_y - 200
                # angle = (180 / math.pi) * -math.atan2((mouse_y - 450), (mouse_x - 1350))
                pygame.draw.rect(screen, (43, 132, 216), ship_movement_UI)
                screen.blit(overlay, (0, 0))
                pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(mouse_x, mouse_y, 10, 10))
                dotexists = True

            if event.type == pygame.MOUSEBUTTONDOWN and in_shop and not UI_is_blocked:
                if managment_UI.collidepoint(pygame.mouse.get_pos()):
                    item,price = shop.interact(pygame.mouse.get_pos())
                    if shop.is_active():
                        current_game.make_purchase(item, price)
                        screen.blit(shop.get_surface(),(0,0))
                    else:
                        in_shop = False

            if event.type == pygame.MOUSEBUTTONDOWN and UI_is_blocked:
                popup.is_collide(pygame.mouse.get_pos(),screen,current_game)
                if not popup.is_active():
                    UI_is_blocked = False
#########################################################################
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    shop = current_game.island_event(type=1,size=2)
                    in_shop = True
                if event.key == pygame.K_a:
                    popup = current_game.island_event(type = 4,size = 2)
                    if popup:
                        UI_is_blocked = True
                if event.key == pygame.K_ESCAPE and UI_is_blocked:
                    popup.delete_popup(screen,current_game)
                    UI_is_blocked = False
#######################################################################
        pygame.display.flip()

        point_hit_box = pygame.Rect(initx, inity, 10, 10)



        y_speed = math.sin(math.radians(currentangle + 90))
        x_speed = math.cos(math.radians(currentangle + 90))

        if dotexists and not (ship_hit_box.colliderect(point_hit_box)):
            initx -= x_speed * speed
            inity += y_speed * speed
            pygame.draw.rect(screen, (43, 132, 216), ship_movement_UI)
            pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(initx, inity, 10, 10))

            island_demo_x -= x_speed * speed
            island_demo_y += y_speed * speed
            pygame.draw.ellipse(screen, (237, 226, 197), pygame.Rect(island_demo_x, island_demo_y, 70, 70))

            ship_map_x += x_speed * speed
            ship_map_y += y_speed * speed

            angle = (180 / math.pi) * -math.atan2((inity - 450), (initx - 1350))

            # Rotation
            # ----------------------------------------------------------
            if currentangle > -90 and ((angle - 90) - currentangle) < -180:
                currentangle += rotation_speed
            elif currentangle < -90 and ((angle - 90) - currentangle) > 180:
                currentangle -= rotation_speed
            else:
                if currentangle < angle - 90:
                    currentangle += rotation_speed
                elif currentangle > angle - 90:
                    currentangle -= rotation_speed
            if currentangle < -279.5:
                currentangle = 89.5
            elif currentangle > 89.5:
                currentangle = -279.5
            screen.blit(rotate_image(ship, +currentangle), (1250, 350))
            # ------------------------------------------------------------



        clock.tick(60)


        screen.blit(ui_helper.draw_resources(current_game),(533,450))
        if not in_shop:
            screen.blit(ui_helper.draw_crew_overview(),(0,0))

if __name__ == "__main__":
    main()
