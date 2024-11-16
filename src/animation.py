from typing import Any

from pico2d import load_image, draw_rectangle


class SpriteAnimation:
    def __init__(self, image_path, frame_cnt, width_cnt, height_cnt):
        self.image = load_image(image_path)
        self.frame_cnt = frame_cnt
        self.width = self.image.w // width_cnt
        self.height = self.image.h // height_cnt
        self.frame_time = 30/60
        self.width_cnt = width_cnt
        self.height_cnt = height_cnt

    def draw(self, x, y, total_time):
        cycle_time = 3
        self.frame_time = cycle_time/self.frame_cnt

        current_frame = int((total_time // self.frame_time) % self.frame_cnt)
        sx = (current_frame % self.width_cnt) * self.width
        sy = (self.height_cnt - current_frame // self.width_cnt - 1) * self.height
        self.image.clip_draw(sx, sy, self.width, self.height, x, y)
        draw_rectangle(x - self.width / 2, y - self.height / 2, x + self.width / 2, y + self.height / 2)

class SpriteCollection:
    def __init__(self):
        self.animations = {}
        self.initialized = False

    def initialize(self):
        self.initialized = True
        self.animations = {
            "knight_slash_right": SpriteAnimation("../resource/knight_slash_right.png", 8, 8, 1),
            "knight_slash_left": SpriteAnimation("../resource/knight_slash_left.png", 8, 8, 1),
            "knight_idle_left": SpriteAnimation("../resource/knight_idle_left.png",4,4,1),
            "knight_idle_right": SpriteAnimation("../resource/knight_idle_right.png",4,4,1),
            "knight_move_left": SpriteAnimation("../resource/knight_move_left.png",9,9,1),
            "knight_move_right": SpriteAnimation("../resource/knight_move_right.png",9,9,1),
            "knight_jump_left": SpriteAnimation("../resource/knight_jump_left.png",8,8,1),
            "knight_jump_right": SpriteAnimation("../resource/knight_jump_right.png", 8, 8, 1),
            "knight_slash_effect_left": SpriteAnimation('../resource/knight_slash_effect_left.png',5,5,1),
            "knight_slash_effect_right": SpriteAnimation('../resource/knight_slash_effect_right.png',5,5,1),
            "knight_dash_left": SpriteAnimation('../resource/knight_dash_left.png',10,5,2),
            "knight_dash_right": SpriteAnimation('../resource/knight_dash_right.png', 10, 5, 2),
            "knight_upslash": SpriteAnimation('../resource/knight_upslash.png',8,8,1),
            "knight_upslash_effect": SpriteAnimation('../resource/knight_upslash_effect.png',5,5,1),
        }

    def get(self,animation_name:str)-> SpriteAnimation:
        if not self.initialized:
            raise "not initialized"
        return self.animations[animation_name]

