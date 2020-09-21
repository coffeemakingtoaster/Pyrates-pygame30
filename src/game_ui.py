import pygame
import os


def main():
    pygame.init()
    width, height = (1600, 900)
    background_color = (0, 0, 0)

    asset_path = os.path.join("data","img")

    overlay = pygame.image.load(os.path.join(os.getcwd(),asset_path,"overlay.png"))
    screen = pygame.display.set_mode((width, height))
    managment_UI = pygame.Rect(0, 0, width / 3, height)
    ship_visual = pygame.Rect(width / 3, 0, width / 3, height/2)
    ressource_visual = pygame.Rect(width / 3, height/2, width / 3, height/2)
    ship_movement_UI = pygame.Rect((width / 3) * 2, 0, width / 3, height)

    pygame.display.set_caption("Pirate game")
    screen.fill(background_color)


    pygame.draw.rect(screen,(127,4,50),managment_UI)
    pygame.draw.rect(screen, (0,0,0), ship_visual)
    pygame.draw.rect(screen, (161, 83, 27),ressource_visual)
    pygame.draw.rect(screen, (10,169, 255), ship_movement_UI)
    screen.blit(overlay, (0, 0))

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()


if __name__ == "__main__":
    main()
