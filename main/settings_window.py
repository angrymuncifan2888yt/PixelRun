import pygame
from ui import NormalButton, LineEdit, Text
from ui.ui_manager import UiManager
from data import Fonts, const, Settings
from window import Window, WindowType


WINDOW_WIDTH = 750
WINDOW_HEIGHT = 750


class SettingsWindow(Window):

    def __init__(self, manager):
        super().__init__(manager, WindowType.SETTINGS)

        self.ui = UiManager()

        self.rect = pygame.Rect(
            const.WINDOW_SIZE[0] // 2 - WINDOW_WIDTH // 2,
            const.WINDOW_SIZE[1] // 2 - WINDOW_HEIGHT // 2,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        start_y = self.rect.y + 140
        spacing = 80
        x = self.rect.x + 80

        # 🔹 Заголовок
        self.title = Text(
            pygame.Vector2(0, self.rect.y + 40),
            Fonts.NORMAL_40,
            "SETTINGS"
        )
        self.title.center_by_x(const.WINDOW_SIZE[0])

        # =========================
        # 🟢 CAMERA SPEED
        # =========================
        self.label_speed = Text(
            pygame.Vector2(x, start_y),
            Fonts.NORMAL_30,
            "Editor Camera Speed"
        )

        self.input_speed = LineEdit(
            (x, start_y + 35),
            (250, 40),
            Fonts.NORMAL_30
        )
        self.input_speed.text = str(Settings.EDITOR_CAMERA_SPEED)

        # =========================
        # 🟢 TARGET FPS
        # =========================
        self.label_fps = Text(
            pygame.Vector2(x, start_y + spacing),
            Fonts.NORMAL_30,
            "Target FPS"
        )

        self.input_fps = LineEdit(
            (x, start_y + spacing + 35),
            (250, 40),
            Fonts.NORMAL_30
        )
        self.input_fps.text = str(Settings.TARGET_FPS)

        # =========================
        # 🟢 LOAD DISTANCE
        # =========================
        self.label_distance = Text(
            pygame.Vector2(x, start_y + spacing * 2),
            Fonts.NORMAL_30,
            "World Load Distance"
        )

        self.input_distance = LineEdit(
            (x, start_y + spacing * 2 + 35),
            (250, 40),
            Fonts.NORMAL_30
        )
        self.input_distance.text = str(Settings.WORLD_LOAD_DISTANCE)

        # =========================
        # 🟢 BACKGROUND COLOR
        # =========================
        self.label_color = Text(
            pygame.Vector2(x, start_y + spacing * 3),
            Fonts.NORMAL_30,
            "Background Color (R G B)"
        )
        # =========================
        # 🟢 BACKGROUND COLOR (RGB)
        # =========================
        self.label_color = Text(
            pygame.Vector2(x, start_y + spacing * 3),
            Fonts.NORMAL_30,
            "Background Color (RGB)"
        )

        r, g, b = Settings.WINDOW_BACKGROUND_COLOR

        input_y = start_y + spacing * 3 + 35

        self.input_r = LineEdit(
            (x, input_y),
            (80, 40),
            Fonts.NORMAL_30,
            max_length=3
        )
        self.input_r.text = str(r)

        self.input_g = LineEdit(
            (x + 100, input_y),
            (80, 40),
            Fonts.NORMAL_30,
            max_length=3
        )
        self.input_g.text = str(g)

        self.input_b = LineEdit(
            (x + 200, input_y),
            (80, 40),
            Fonts.NORMAL_30,
            max_length=3
        )
        self.input_b.text = str(b)

        # =========================
        # 🟢 КНОПКИ
        # =========================
        self.btn_apply = NormalButton(
            position=pygame.Vector2(self.rect.x + 120, self.rect.bottom - 90),
            size=(200, 55),
            text="Apply",
            font=Fonts.NORMAL_30,
            callback=self.apply_settings
        )

        self.btn_close = NormalButton(
            position=pygame.Vector2(self.rect.right - 240, self.rect.bottom - 90),
            size=(200, 55),
            text="Close",
            font=Fonts.NORMAL_30,
            callback=self.close
        )

        # =========================
        # 🟢 ADD UI
        # =========================
        for obj in [
            self.title,
            self.label_speed, self.input_speed,
            self.label_fps, self.input_fps,
            self.label_distance, self.input_distance,
            self.label_color, self.input_r, self.input_b, self.input_g,
            self.btn_apply, self.btn_close
        ]:
            self.ui.add_ui_object(obj)

    def apply_settings(self):
        try:
            Settings.EDITOR_CAMERA_SPEED = float(self.input_speed.text)
        except:
            pass

        try:
            Settings.TARGET_FPS = int(self.input_fps.text)
        except:
            pass

        try:
            Settings.WORLD_LOAD_DISTANCE = float(self.input_distance.text)
        except:
            pass

        try:
            r = max(0, min(255, int(self.input_r.text)))
            g = max(0, min(255, int(self.input_g.text)))
            b = max(0, min(255, int(self.input_b.text)))

            Settings.WINDOW_BACKGROUND_COLOR = (r, g, b)
        except:
            pass

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta_time):
        self.ui.update(delta_time)

    def draw(self, screen):
        overlay = pygame.Surface(const.WINDOW_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)

        self.ui.draw(screen)