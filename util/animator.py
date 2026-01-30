from .timer import Timer

class Animator:
    def __init__(self, sprite_count: int, frame_time: float):
        self.sprite_count = sprite_count
        self.current_frame = 0
        self.timer = Timer(frame_time)

    def reset(self):
        self.current_frame = 0
        
    def update(self, delta_time: float):
        self.timer.update(delta_time)

        if self.timer.is_finished():
            self.current_frame += 1

            if self.current_frame >= self.sprite_count:
                self.current_frame = 0
            self.timer.reset()

    def render(self, surface, sprites: list, position):
        surface.blit(sprites[self.current_frame], position)

    def set_sprite_count(self, sprite_count: int):
        self.sprite_count = sprite_count
        self.current_frame = 0
        self.timer.reset()

    def get_current_sprite(self, sprites: list):
        return sprites[self.current_frame]
