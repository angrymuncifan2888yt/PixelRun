import pygame
from ui import NormalButton
from data import Fonts
from window import Window, WindowType  # путь поправь под свой проект


class LevelEditWindow(Window):
    def __init__(self, manager, level, screen_size):
        super().__init__(manager, WindowType.LEVEL_EDIT)

        self.level = level
        self.screen_size = screen_size

        width = 500
        height = 400

        self.rect = pygame.Rect(
            screen_size[0] // 2 - width // 2,
            screen_size[1] // 2 - height // 2,
            width,
            height
        )

        self.btn_close = NormalButton(
            position=pygame.Vector2(self.rect.right - 110, self.rect.top + 10),
            size=(100, 40),
            text="Close",
            font=Fonts.NORMAL_30,
            callback=self.close
        )

    def handle_pygame_event(self, event):
        self.btn_close.handle_pygame_event(event)

    def update(self, delta_time):
        self.btn_close.update(delta_time)

    def draw(self, screen):
        # затемнение фона
        overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # окно
        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)

        font = Fonts.NORMAL_30

        title = font.render("LEVEL EDIT MENU", True, (255, 255, 255))
        screen.blit(title, (self.rect.x + 20, self.rect.y + 20))

        bg_text = font.render(
            f"Background: {self.level.background_color}",
            True,
            (255, 255, 255)
        )
        screen.blit(bg_text, (self.rect.x + 20, self.rect.y + 80))

        self.btn_close.draw(screen)
