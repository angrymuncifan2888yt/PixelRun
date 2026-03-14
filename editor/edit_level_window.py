import pygame
from ui import NormalButton, LineEdit
from data import Fonts
from window import Window, WindowType


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class LevelEditWindow(Window):

    def __init__(self, manager, screen_size, set_bg_func, set_spawn_func, set_name_func):
        super().__init__(manager, WindowType.LEVEL_EDIT)

        self.screen_size = screen_size

        self.set_background = set_bg_func
        self.set_spawn = set_spawn_func
        self.set_name = set_name_func
        self.rect = pygame.Rect(
            screen_size[0] // 2 - WINDOW_WIDTH // 2,
            screen_size[1] // 2 - WINDOW_HEIGHT // 2,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        # NAME
        self.input_name = LineEdit(
            (self.rect.x + 300, self.rect.y + 100),
            (400, 40),
            Fonts.NORMAL_30,
            max_length=32
        )

        # default params
        r, g, b = (0, 0, 0)
        spawn_x = 0
        spawn_y = 0
        # RGB
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

        # PLAYER SPAWN
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

        self.btn_close = NormalButton(
            position=pygame.Vector2(self.rect.right - 160, self.rect.bottom - 70),
            size=(130, 45),
            text="Close",
            font=Fonts.NORMAL_30,
            callback=self.close
        )
    def update_data(self, r, g, b, name, player_spawn):
        self.input_r.text = str(r)
        self.input_b.text = str(b)
        self.input_g.text = str(g)
        self.input_name.text = name
        self.input_spawn_x.text = str(player_spawn[0])
        self.input_spawn_y.text = str(player_spawn[1])
        
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

        try:
            spawn_x = int(self.input_spawn_x.text)
        except:
            spawn_x = 0

        try:
            spawn_y = int(self.input_spawn_y.text)
        except:
            spawn_y = 0
        self.set_background(r, g, b)
        self.set_spawn(spawn_x, spawn_y)
        self.set_name(self.input_name.text)

    def handle_pygame_event(self, event):

        self.btn_close.handle_pygame_event(event)
        self.btn_apply.handle_pygame_event(event)

        self.input_name.handle_pygame_event(event)

        self.input_r.handle_pygame_event(event)
        self.input_g.handle_pygame_event(event)
        self.input_b.handle_pygame_event(event)

        self.input_spawn_x.handle_pygame_event(event)
        self.input_spawn_y.handle_pygame_event(event)

    def update(self, delta_time):

        self.btn_close.update(delta_time)
        self.btn_apply.update(delta_time)

        self.input_name.update(delta_time)

        self.input_r.update(delta_time)
        self.input_g.update(delta_time)
        self.input_b.update(delta_time)

        self.input_spawn_x.update(delta_time)
        self.input_spawn_y.update(delta_time)

    def draw(self, screen):

        overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)

        font = Fonts.NORMAL_30

        title = font.render("LEVEL EDIT MENU", True, (255, 255, 255))
        screen.blit(title, (self.rect.x + 30, self.rect.y + 30))

        # NAME
        name_label = font.render("Level Name:", True, (255, 255, 255))
        screen.blit(name_label, (self.rect.x + 30, self.rect.y + 100))

        # BACKGROUND
        label = font.render("Background RGB:", True, (255, 255, 255))
        screen.blit(label, (self.rect.x + 30, self.rect.y + 165))

        preview_rect = pygame.Rect(
            self.rect.x + 30,
            self.rect.y + 230,
            200,
            100
        )

        color = (
            int(self.input_r.text) if self.input_r.text.isdigit() else 0,
            int(self.input_g.text) if self.input_g.text.isdigit() else 0,
            int(self.input_b.text) if self.input_b.text.isdigit() else 0
        )

        pygame.draw.rect(screen,  color, preview_rect)
        pygame.draw.rect(screen, (255, 255, 255), preview_rect, 3)

        # PLAYER SPAWN
        spawn_label = font.render("Player Spawn:", True, (255, 255, 255))
        screen.blit(spawn_label, (self.rect.x + 30, self.rect.y + 340))

        self.input_name.draw(screen)

        self.input_r.draw(screen)
        self.input_g.draw(screen)
        self.input_b.draw(screen)

        self.input_spawn_x.draw(screen)
        self.input_spawn_y.draw(screen)

        self.btn_apply.draw(screen)
        self.btn_close.draw(screen)