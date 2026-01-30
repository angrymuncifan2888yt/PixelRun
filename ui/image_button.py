import pygame
from .button import Button

class ImageButton(Button):
    def __init__(self, position, image, callback=None, size=(100, 100), hover_scale=1.2):
        super().__init__(position, size, callback)

        self.original_image = pygame.transform.smoothscale(image, size)
        self.image = self.original_image

        self.hover_scale = hover_scale
        self.rect = self.image.get_rect()

    def update(self, delta: float, **kwargs):
        global_pos = self.get_global_position()

        # hitbox ВСЕГДА = базовый размер кнопки
        self.hitbox.topleft = (global_pos.x, global_pos.y)

        if self.is_mouse_on_button():
            new_size = (
                int(self.hitbox.width * self.hover_scale),
                int(self.hitbox.height * self.hover_scale)
            )

            self.image = pygame.transform.smoothscale(self.original_image, new_size)

            # визуалка растёт ИЗ ЦЕНТРА hitbox
            self.rect = self.image.get_rect(center=self.hitbox.center)
        else:
            self.image = self.original_image
            self.rect.topleft = self.hitbox.topleft

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def center_by_x(self, width: int):
        self.position.x = (width - self.hitbox.width) // 2

    def center_by_y(self, height: int):
        self.position.y = (height - self.hitbox.height) // 2
