import json
from pico2d import load_image, draw_rectangle


class SpriteAnimation:
    def __init__(self, image_path, frame_cnt, width_cnt, height_cnt, v_align=None, h_align=None):
        self.image_path = image_path
        self.image = load_image(image_path)
        self.frame_cnt = frame_cnt
        self.width = self.image.w // width_cnt
        self.height = self.image.h // height_cnt
        self.frame_time = 30 / 60
        self.width_cnt = width_cnt
        self.height_cnt = height_cnt
        self.v_align = 'center' if v_align is None else v_align
        self.h_align = 'center' if h_align is None else h_align

        self.c_width = None
        self.c_height = None

    def calculate_rect(self, x, y, width, height):
        """
        :param x: 그려지는 x 좌표
        :param y: 그려지는 y 좌표
        :param width: 가로 길이
        :param height: 세로 길이
        :return: clip draw 맞춤형 x,y,width,height 튜플
        """

        game_width = self.width
        game_height = self.height
        if width is not None: game_width = width
        if height is not None: game_height = height

        if self.v_align == 'center':
            draw_y = y
        elif self.v_align == 'bottom':
            draw_y = y + game_height // 2
        else:
            draw_y = y - game_height // 2

        if self.h_align == 'center':
            draw_x = x
        elif self.h_align == 'left':
            draw_x = x + game_width // 2
        else:
            draw_x = x - game_width // 2

        return draw_x, draw_y, game_width, game_height

    def draw(self, x, y, total_time, inverted: bool, width=None, height=None):
        cycle_time = 3
        self.frame_time = cycle_time / self.frame_cnt

        self.c_width = width
        self.c_height = height

        current_frame = int((total_time // self.frame_time) % self.frame_cnt)
        sx = (current_frame % self.width_cnt) * self.width
        sy = (self.height_cnt - current_frame // self.width_cnt - 1) * self.height

        draw_x, draw_y, draw_width, draw_height = self.calculate_rect(x, y, width, height)

        if inverted:
            self.image.clip_composite_draw(sx, sy, self.width, self.height, 0, 'h', draw_x, draw_y, draw_width,
                                           draw_height)
        elif not inverted:
            self.image.clip_draw(sx, sy, self.width, self.height, draw_x, draw_y, draw_width, draw_height)

        draw_rectangle(draw_x - draw_width / 2, draw_y - draw_height / 2, draw_x + draw_width / 2,
                       draw_y + draw_height / 2)

    def get_size(self) -> tuple:

        return self.width, self.height


class SpriteCollection:
    def __init__(self):
        self.animations = {}
        self.initialized = False

    def initialize(self):
        with open('../resource/animations.json', 'r') as file:
            data = json.load(file)
            self.animations = {
                name: SpriteAnimation(
                    image_path=anim_data["path"],
                    frame_cnt=anim_data["frames"],
                    width_cnt=anim_data["width"],
                    height_cnt=anim_data["height"],
                    v_align=anim_data["v_align"] if "v_align" in anim_data else None,
                    h_align=anim_data["h_align"] if "h_align" in anim_data else None
                )
                for name, anim_data in data["animations"].items()
            }
        self.initialized = True

    def get(self, animation_name: str) -> SpriteAnimation:
        if not self.initialized:
            raise "not initialized"
        return self.animations[animation_name]
