from pygame import Vector2, Rect
from .entity import Entity
from data import Skin, const
from util import SpriteAnimator, PlayerDirection


class Player(Entity):
    def __init__(self, world, position: Vector2, skin: Skin, rotation=0):
        super().__init__(world, position, *const.PLAYER_SIZE, rotation)
        self.kill_y = 5000
        self.direction = PlayerDirection.RIGHT
        self.current_checkpoint = None

        self.is_clicking = False
        self.base_spawn_position = position.copy()

        self.prev_position = self.position.copy()
        self.prev_rect = self.hitbox.copy()

        self.skin = skin
        self.animator = SpriteAnimator(skin.animation_length, 0.1)

        self.velocity = Vector2(0, 0)

        self.gravity_dir = 1
        self.gravity = 2000
        self.jump_force = 1000

        self.on_ground = False
        self.rotation = 0

        self.move_speed = 800  # максимальная скорость движения
        self.acceleration = 10000  # ускорение пикселей/с^2
        self.friction = 4000  # замедление, когда клавиша отпущена

    @property
    def is_upside_down(self):
        return self.gravity_dir == -1

    def update_rotation(self):
        self.rotation = 180 if self.is_upside_down else 0

    def set_skin(self, skin: Skin):
        self.skin = skin
        self.animator.set_sprite_count(self.skin.animation_length)

    def jump(self):
        if self.on_ground:
            self.velocity.y = -self.jump_force * self.gravity_dir
            self.on_ground = False

    def move_right(self, delta_time: float):
        self.velocity.x += self.acceleration * delta_time
        if self.velocity.x > self.move_speed:
            self.velocity.x = self.move_speed
        self.direction = PlayerDirection.RIGHT

    def move_left(self, delta_time: float):
        self.velocity.x -= self.acceleration * delta_time
        if self.velocity.x < -self.move_speed:
            self.velocity.x = -self.move_speed
        self.direction = PlayerDirection.LEFT

    def stop_horizontal(self, delta_time: float):
        if self.velocity.x > 0:
            self.velocity.x -= self.friction * delta_time
            if self.velocity.x < 0:
                self.velocity.x = 0
        elif self.velocity.x < 0:
            self.velocity.x += self.friction * delta_time
            if self.velocity.x > 0:
                self.velocity.x = 0

    def update(self, delta_time: float):
        self.direction = PlayerDirection.STANDING
        self.prev_position = self.position.copy()
        self.prev_rect = self.hitbox.copy()

        self.animator.update(delta_time)

        self.velocity.y += self.gravity * delta_time * self.gravity_dir
        self.position += self.velocity * delta_time

        self.stop_horizontal(delta_time)
        self.update_rotation()

        if abs(self.position.y - 0) >= self.kill_y:
            self.respawn()

    def respawn(self):
        if self.current_checkpoint:
            self.position = self.current_checkpoint.position.copy()
        else:
            self.position = self.base_spawn_position.copy()

        self.velocity = Vector2(0, 0)
        self.gravity_dir = 1
        self.on_ground = False
        self.animator.reset()

    def reverse_gravity(self):
        self.gravity_dir *= -1
        self.on_ground = False

    def handle_platform_collision(self, platform):
        plat_rect = platform.hitbox
        curr_rect = self.hitbox

        if not curr_rect.colliderect(plat_rect):
            return

        dx_left = curr_rect.right - plat_rect.left
        dx_right = plat_rect.right - curr_rect.left
        dy_top = curr_rect.bottom - plat_rect.top
        dy_bottom = plat_rect.bottom - curr_rect.top

        min_dx = min(dx_left, dx_right)
        min_dy = min(dy_top, dy_bottom)

        if min_dx < min_dy:
            if dx_left < dx_right:
                self.position.x -= dx_left
            else:
                self.position.x += dx_right
            self.velocity.x = 0
        else:
            if self.gravity_dir == 1:
                if dy_top < dy_bottom:
                    self.position.y -= dy_top
                    if self.velocity.y > 0:
                        self.velocity.y = 0
                        self.on_ground = True
                else:
                    self.position.y += dy_bottom
                    if self.velocity.y < 0:
                        self.velocity.y = 0
            else:
                if dy_bottom < dy_top:
                    self.position.y += dy_bottom
                    if self.velocity.y < 0:
                        self.velocity.y = 0
                        self.on_ground = True
                else:
                    self.position.y -= dy_top
                    if self.velocity.y > 0:
                        self.velocity.y = 0
