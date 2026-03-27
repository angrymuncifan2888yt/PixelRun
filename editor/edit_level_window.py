import pygame
from ui import NormalButton, LineEdit, UiManager
from data import Fonts
from window import Window, WindowType


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class LevelEditWindow(Window):

    def __init__(self, manager, screen_size, set_bg_func, set_spawn_func, set_name_func, delete_level_objects_func):
        super().__init__(manager, WindowType.LEVEL_EDIT)

        self.screen_size = screen_size

        self.set_background = set_bg_func
        self.set_spawn = set_spawn_func
        self.set_name = set_name_func
        self.delete_level_objects = delete_level_objects_func

        self.ui = UiManager()

        self.rect = pygame.Rect(
            screen_size[0] // 2 - WINDOW_WIDTH // 2,
            screen_size[1] // 2 - WINDOW_HEIGHT // 2,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        r, g, b = (0, 0, 0)
        spawn_x = 0
        spawn_y = 0

        self.input_name = LineEdit(
            (self.rect.x + 300, self.rect.y + 100),
            (400, 40),
            Fonts.NORMAL_30,
            max_length=32
        )

        self.input_r = LineEdit(
            (self.rect.x + 450, self.rect.y + 160),
            (80, 40),
            Fonts.NORMAL_30,
            max_length=3
        )
        self.input_r.text = str(r)

        self.input_g = LineEdit(
            (self.rect.x + 540, self.rect.y + 160),
            (80, 40),
            Fonts.NORMAL_30,
            max_length=3
        )
        self.input_g.text = str(g)

        self.input_b = LineEdit(
            (self.rect.x + 630, self.rect.y + 160),
            (80, 40),
            Fonts.NORMAL_30,
            max_length=3
        )
        self.input_b.text = str(b)

        self.input_spawn_x = LineEdit(
            (self.rect.x + 450, self.rect.y + 340),
            (120, 40),
            Fonts.NORMAL_30,
            max_length=6
        )
        self.input_spawn_x.text = str(spawn_x)

        self.input_spawn_y = LineEdit(
            (self.rect.x + 580, self.rect.y + 340),
            (120, 40),
            Fonts.NORMAL_30,
            max_length=6
        )
        self.input_spawn_y.text = str(spawn_y)

        self.btn_apply = NormalButton(
            position=pygame.Vector2(self.rect.x + 30, self.rect.bottom - 70),
            size=(150, 45),
            text="Apply",
            font=Fonts.NORMAL_30,
            callback=self.apply
        )

        self.btn_clear = NormalButton(
            position=pygame.Vector2(self.rect.centerx - 75, self.rect.bottom - 70),
            size=(150, 45),
            text="Clear All",
            font=Fonts.NORMAL_30,
            callback=self.delete_level_objects,
            color=(200, 0, 0)
        )
        self.btn_clear.hover_color = (150, 0, 0)

        self.btn_close = NormalButton(
            position=pygame.Vector2(self.rect.right - 160, self.rect.bottom - 70),
            size=(130, 45),
            text="Close",
            font=Fonts.NORMAL_30,
            callback=self.close
        )

        self.ui.add_ui_object(self.input_name)

        self.ui.add_ui_object(self.input_r)
        self.ui.add_ui_object(self.input_g)
        self.ui.add_ui_object(self.input_b)

        self.ui.add_ui_object(self.input_spawn_x)
        self.ui.add_ui_object(self.input_spawn_y)

        self.ui.add_ui_object(self.btn_apply)
        self.ui.add_ui_object(self.btn_clear)
        self.ui.add_ui_object(self.btn_close)

    def update_data(self, r, g, b, name, player_spawn):
        self.input_r.text = str(r)
        self.input_g.text = str(g)
        self.input_b.text = str(b)
        self.input_name.text = name
        self.input_spawn_x.text = str(player_spawn[0])
        self.input_spawn_y.text = str(player_spawn[1])

    def clamp_color(self, value):
        return max(0, min(255, value))
    def safe_int(self, text):
        try:
            return float(text.strip())
        except:
            return 0
    def apply(self):

        if self.input_r.text.isdigit():
            r = max(0, min(255, int(self.input_r.text)))
        else:
            r = 0

        if self.input_g.text.isdigit():
            g = max(0, min(255, int(self.input_g.text)))
        else:
            g = 0

        if self.input_b.text.isdigit():
            b = max(0, min(255, int(self.input_b.text)))
        else:
            b = 0

        spawn_x = self.safe_int(self.input_spawn_x.text)
        spawn_y = self.safe_int(self.input_spawn_y.text)

        self.set_background(r, g, b)
        self.set_spawn(spawn_x, spawn_y)
        self.set_name(self.input_name.text)

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta_time):
        self.ui.update(delta_time)

    def draw(self, screen):

        overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)

        font = Fonts.NORMAL_30

        title = font.render("LEVEL EDIT MENU", True, (255, 255, 255))
        screen.blit(title, (self.rect.x + 30, self.rect.y + 30))

        name_label = font.render("Level Name:", True, (255, 255, 255))
        screen.blit(name_label, (self.rect.x + 30, self.rect.y + 100))

        label = font.render("Background RGB:", True, (255, 255, 255))
        screen.blit(label, (self.rect.x + 30, self.rect.y + 165))

        preview_rect = pygame.Rect(
            self.rect.x + 30,
            self.rect.y + 230,
            200,
            100
        )

        r = self.clamp_color(int(self.input_r.text)) if self.input_r.text.isdigit() else 0
        g = self.clamp_color(int(self.input_g.text)) if self.input_g.text.isdigit() else 0
        b = self.clamp_color(int(self.input_b.text)) if self.input_b.text.isdigit() else 0

        color = (r, g, b)

        pygame.draw.rect(screen, color, preview_rect)
        pygame.draw.rect(screen, (255, 255, 255), preview_rect, 3)

        spawn_label = font.render("Player Spawn:", True, (255, 255, 255))
        screen.blit(spawn_label, (self.rect.x + 30, self.rect.y + 340))

        self.ui.draw(screen)
