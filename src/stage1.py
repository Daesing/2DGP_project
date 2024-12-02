from pico2d import *

import game_framework
import game_world
import title_mode
from knight import Knight
import play_mode
import stage2
from header import WIDTH,HEIGHT
from false_knight import FalseKnight
import game_over


# knight 객체의 생성이 스테이지마다 이루어지면 위치를 어떻게 설정하는가?
def init():
    global stage1_back,text,bgm
    stage1_back = load_image('../resource/background/Forgotten_Crossroads_False_Knight_Arena.png')
    text = load_image('../resource/ui/stage1_text.png')
    bgm = load_music('../resource/audio/bgm/Boss Battle 1.wav')
    bgm.set_volume(20)
    bgm.repeat_play()

    global knight
    global false_knight
    knight = Knight(0,180)
    false_knight = FalseKnight(800,120)
    game_world.add_object(knight,1)
    game_world.add_object(false_knight,1)

    # knight_slash: false_knight collision pair
    game_world.add_collision_pair('slash:false_knight',None,false_knight)
    # knight_fireball:false_knight collision pair
    game_world.add_collision_pair('fireball:false_knight',None,false_knight)

    #knight:false_knight
    game_world.add_collision_pair('knight:false_knight',knight,false_knight)

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
    elif false_knight.dead == False and knight.x > WIDTH:
        knight.x = WIDTH

    if knight.x > WIDTH and false_knight.dead:
        bgm.stop()
        game_framework.change_mode(stage2)
    if knight.hp <= 0:
        bgm.stop()
        game_framework.change_mode(game_over)

def draw():
    clear_canvas()
    stage1_back.draw(WIDTH // 2, HEIGHT // 2)
    text.draw(1150,650)
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()
    pass
def pause(): pass
def resume(): pass

