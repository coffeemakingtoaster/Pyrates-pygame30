import pygame
import os




def status_update(title,text):
    pygame.font.init()
    caption_size = 70
    text_size = 40
    popup_background = (82, 62, 16)
    caption_color = (196, 33, 0)
    text_color = (207, 187, 39)
    window_size = (400, 300)
    i = 20
    while i<len(text):
        text = text[i]+"\n"+text[i+1]
        i+20
    Caption = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Avara.ttf"), caption_size)
    message_text = pygame.font.Font(os.path.join(os.getcwd(), "data", "other", "Carlito-Regular.ttf"), text_size)
    surf = pygame.Surface(window_size)
    surf.fill(popup_background)
    caption_render = Caption.render(title,False,caption_color)
    caption_rec = caption_render.get_rect(center=(window_size[0]/2,65))
    text_render = message_text.render(text,False,text_color)
    text_rect = caption_render.get_rect(center=(125,(window_size[1]/2)))
    button_render = message_text.render("OK",False,text_color)
    button_rect = button_render.get_rect(center=(window_size[0]/2,245))

    surf.blit(caption_render,caption_rec)
    surf.blit(text_render, text_rect)
    surf.blit(button_render,button_rect)
    return surf,button_rect

