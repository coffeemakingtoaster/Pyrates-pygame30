import pygame
import os
import math


#given an image and an angle this returns the rotated image
#can directly be drawn to screen
def rotate_image(image,angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def main():
    pygame.init()
    #init size of the window. The background color is never visible
    width, height = (1600, 900)
    background_color = (0, 0, 0)

    #path to resources (images in this case)
    asset_path = os.path.join(os.getcwd(),"data","img")

    # init UI elements and provide them with coordinates
    overlay = pygame.image.load(os.path.join(asset_path,"overlay.png"))
    ship = pygame.image.load(os.path.join(asset_path,"ship.png"))
    screen = pygame.display.set_mode((width, height))
    managment_UI = pygame.Rect(0, 0, width / 3, height)
    ship_visual = pygame.Rect(width / 3, 0, width / 3, height/2)
    ressource_visual = pygame.Rect(width / 3, height/2, width / 3, height/2)
    ship_movement_UI = pygame.Rect((width / 3) * 2, 0, width / 3, height)

    # fill the screen with said elements
    pygame.display.set_caption("Pirate game")
    screen.fill(background_color)
    pygame.draw.rect(screen,(127,4,50),managment_UI)
    pygame.draw.rect(screen, (0,0,0), ship_visual)
    pygame.draw.rect(screen, (161, 83, 27),ressource_visual)
    pygame.draw.rect(screen, (10,169, 255), ship_movement_UI)
    screen.blit(ship, (1250, 600))
    screen.blit(overlay, (0, 0))

    #flip displayes everything for the user to see
    pygame.display.flip()

    #gameloop
    running = True
    while running:
        for event in pygame.event.get():
            #Quit
            if event.type == pygame.QUIT:
                running = False
            #at mouseclick:
            #- checks if click was in ship movement window and if so rotates the ship image
            #TODO: add support for more parts of the screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                if ship_movement_UI.collidepoint(pygame.mouse.get_pos()):
                    angle = (180 / math.pi) * -math.atan2((mouse_y - 700 ),(mouse_x - 1350))
                    pygame.draw.rect(screen, (10, 169, 255), ship_movement_UI)
                    screen.blit(rotate_image(ship,angle-90), (1250, 600))
                    screen.blit(overlay, (0, 0))
                    pygame.draw.ellipse(screen, (255,0,0), pygame.Rect(mouse_x,mouse_y,10,10))
        pygame.display.flip()


if __name__ == "__main__":
    main()
