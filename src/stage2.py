from pico2d import *

import game_framework
import game_world
import title_mode
from knight import Knight
from header import WIDTH,HEIGHT
from hornet import Hornet
import game_over
import ending


def init():
    global knight
    global image,text,bgm
    global hornet
    image = load_image('../resource/background/Greenpath_Hornet_Arena.png')
    text = load_image('../resource/ui/stage2_text.png')
    bgm = load_music('../resource/audio/bgm/S45 HORNET-110.wav')
    bgm.set_volume(20)
    bgm.repeat_play()
    knight = Knight(0,140)
    hornet = Hornet(800,150)
    game_world.add_object(knight, 1)
    game_world.add_object(hornet,1)

    game_world.add_collision_pair('knight:hornet',knight,hornet)
    game_world.add_collision_pair('knight:needle',knight,None)
    game_world.add_collision_pair('slash:hornet',None, hornet)
    game_world.add_collision_pair('fireball:hornet',None,hornet)
    game_world.add_collision_pair('knight:sphere',knight,None)
    game_world.add_collision_pair('knight:barb',knight,None)

def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            knight.handle_event(event)

def update():
    game_world.update()
    game_world.handle_collisions()
    if knight.x < 0:
        knight.x = 0
    elif hornet.dead == False and knight.x > WIDTH:
        knight.x = WIDTH

    if knight.hp <= 0:
        bgm.stop()
        game_framework.change_mode(game_over)
    if hornet.dead == True and knight.x > WIDTH:
        bgm.stop()
        game_framework.change_mode(ending)




def draw():
    clear_canvas()
    image.draw(WIDTH // 2, HEIGHT // 2)
    text.draw(1150,650)
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()
    pass

def pause(): pass
def resume(): pass

