import os
import ui_helper




def island_event():
    text = "Wow this does things"
    title = "battle"
    popup,ok_hitbox = ui_helper.status_update(title,text)
    return popup,ok_hitbox