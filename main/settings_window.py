import pygame
from ui import NormalButton, LineEdit, Text, TabContainer, UiManager
from data import Fonts, const, PlayerData
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

        # start_y = self.rect.y + 140
        start_y = 60
        spacing = 80
        # x = self.rect.x + 80
        x = 20
        padding = 20

        self.tabs = TabContainer(
            pygame.Vector2(self.rect.x + padding, self.rect.y + padding + 80),
            (
                self.rect.width - padding * 2,
                self.rect.height - padding * 2 - 80  # место под кнопки снизу
            ),
            True
        )
        # 🔹 Заголовок
        self.title = Text(
            pygame.Vector2(0, self.rect.y + 40),
            Fonts.NORMAL_40,
            "SETTINGS"
        )
        self.title.center_by_x(const.WINDOW_SIZE[0])

        # =========================
        # 🟢 EDITOR CAMERA SPEED
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
        self.input_speed.text = str(PlayerData.EDITOR_CAMERA_SPEED)

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
        self.input_fps.text = str(PlayerData.TARGET_FPS)

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
        self.input_distance.text = str(PlayerData.WORLD_LOAD_DISTANCE)

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

        r, g, b = PlayerData.WINDOW_BACKGROUND_COLOR

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
        # 🟢 MUSIC VOLUME
        # =========================
        self.label_volume = Text(
            pygame.Vector2(x, start_y + spacing * 5),
            Fonts.NORMAL_30,
            "Music Volume"
        )

        self.volume_value = PlayerData.MUSIC_VOLUME

        self.text_volume = Text(
            pygame.Vector2(x + 85, start_y + spacing * 5 + 35),
            Fonts.NORMAL_30,
            f"{self.volume_value:.2f}"
        )

        # Кнопка <
        self.btn_volume_down = NormalButton(
            position=pygame.Vector2(x, start_y + spacing * 5 + 35),
            size=(40, 40),
            text="<",
            font=Fonts.NORMAL_30,
            callback=self.decrease_music_volume
        )

        # Кнопка >
        self.btn_volume_up = NormalButton(
            position=pygame.Vector2(x + 200, start_y + spacing * 5 + 35),
            size=(40, 40),
            text=">",
            font=Fonts.NORMAL_30,
            callback=self.increase_music_volume
        )

        # =========================
        # 🟢 CAMERA SPEED
        # =========================
        self.label_camera_speed = Text(
            pygame.Vector2(x, start_y + spacing * 4),
            Fonts.NORMAL_30,
            "Camera Speed"
        )

        self.input_camera_speed = LineEdit(
            (x, start_y + spacing * 4 + 35),
            (250, 40),
            Fonts.NORMAL_30
        )
        self.input_camera_speed.text = str(PlayerData.CAMERA_SPEED)

        # =========================
        # 🟢 PLAYER VOLUME
        # =========================
        self.label_player_volume = Text(
            pygame.Vector2(x, start_y),
            Fonts.NORMAL_30,
            "Player Volume"
        )

        self.player_volume = PlayerData.PLAYER_VOLUME

        self.text_player_volume = Text(
            pygame.Vector2(x + 85, start_y + 35),
            Fonts.NORMAL_30,
            f"{self.player_volume:.2f}"
        )

        self.btn_player_volume_down = NormalButton(
            position=pygame.Vector2(x, start_y + 35),
            size=(40, 40),
            text="<",
            font=Fonts.NORMAL_30,
            callback=self.decrease_player_volume
        )

        self.btn_player_volume_up = NormalButton(
            position=pygame.Vector2(x + 200, start_y + 35),
            size=(40, 40),
            text=">",
            font=Fonts.NORMAL_30,
            callback=self.increase_player_volume
        )
        # =========================
        # 🟢 PLAYER DEATH VOLUME
        # =========================
        self.label_player_death_volume = Text(
            pygame.Vector2(x, start_y + spacing),
            Fonts.NORMAL_30,
            "Player Death Volume"
        )

        self.player_death_value = PlayerData.PLAYER_DEATH_VOLUME

        self.text_player_death_volume = Text(
            pygame.Vector2(x + 85, start_y + spacing + 35),
            Fonts.NORMAL_30,
            f"{self.player_death_value:.2f}"
        )

        self.btn_player_death_volume_down = NormalButton(
            position=pygame.Vector2(x, start_y + spacing + 35),
            size=(40, 40),
            text="<",
            font=Fonts.NORMAL_30,
            callback=self.decrease_player_death_volume
        )

        self.btn_player_death_volume_up = NormalButton(
            position=pygame.Vector2(x + 200, start_y + spacing + 35),
            size=(40, 40),
            text=">",
            font=Fonts.NORMAL_30,
            callback=self.increase_player_death_volume
        )
        # =========================
        # 🟢 КНОПКИ
        # =========================
        self.btn_apply = NormalButton(
            position=pygame.Vector2(self.rect.x + 220, self.rect.bottom - 90),
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
        self.btn_tab_left = NormalButton(
            position=pygame.Vector2(self.rect.x + 20, self.rect.bottom - 90),
            size=(60, 55),
            text="<",
            font=Fonts.NORMAL_30,
            callback=self.tabs.prev_tab
        )

        self.btn_tab_right = NormalButton(
            position=pygame.Vector2(self.rect.x + 90, self.rect.bottom - 90),
            size=(60, 55),
            text=">",
            font=Fonts.NORMAL_30,
            callback=self.tabs.next_tab
        )

        first_tab = [
            self.label_speed, self.input_speed,
            self.label_fps, self.input_fps,
            self.label_distance, self.input_distance,
            self.label_camera_speed, self.input_camera_speed,
            self.label_color, self.input_r, self.input_g, self.input_b,
            self.label_volume, self.text_volume, self.btn_volume_down, self.btn_volume_up,
        ]
        second_tab = [
            self.label_player_volume, self.text_player_volume, self.btn_player_volume_down, self.btn_player_volume_up,
            self.label_player_death_volume, self.text_player_death_volume, self.btn_player_death_volume_down, self.btn_player_death_volume_up
        ]
        self.tabs.add_tab(first_tab)
        self.tabs.add_tab(second_tab)

        # =========================
        # 🟢 ADD UI
        # =========================
        for obj in [
            self.tabs, self.title,
            self.btn_tab_left, self.btn_tab_right,
            self.btn_apply, self.btn_close
        ]:
            self.ui.add_ui_object(obj)

    def increase_player_death_volume(self):
        self.player_death_value = min(1.0, self.player_death_value + 0.05)
        self.text_player_death_volume.text = f"{self.player_death_value:.2f}"

    def decrease_player_death_volume(self):
        self.player_death_value = max(0.0, self.player_death_value - 0.05)
        self.text_player_death_volume.text = f"{self.player_death_value:.2f}"

    def increase_player_volume(self):
        self.player_volume = min(1.0, self.player_volume + 0.05)
        self.text_player_volume.text = f"{self.player_volume:.2f}"

    def decrease_player_volume(self):
        self.player_volume = max(0.0, self.player_volume - 0.05)
        self.text_player_volume.text = f"{self.player_volume:.2f}"
    def increase_music_volume(self):
        self.volume_value = min(1.0, self.volume_value + 0.05)
        self.text_volume.text = f"{self.volume_value:.2f}"

    def decrease_music_volume(self):
        self.volume_value = max(0.0, self.volume_value - 0.05)
        self.text_volume.text = f"{self.volume_value:.2f}"

    def apply_settings(self):
        try:
            PlayerData.EDITOR_CAMERA_SPEED = float(self.input_speed.text)
        except:
            pass
        try:
            PlayerData.TARGET_FPS = int(self.input_fps.text)
        except:
            pass
        try:
            PlayerData.CAMERA_SPEED = float(self.input_camera_speed.text)
        except:
            pass
        try:
            PlayerData.WORLD_LOAD_DISTANCE = float(self.input_distance.text)
        except:
            pass

        try:
            r = max(0, min(255, int(self.input_r.text)))
            g = max(0, min(255, int(self.input_g.text)))
            b = max(0, min(255, int(self.input_b.text)))

            PlayerData.WINDOW_BACKGROUND_COLOR = (r, g, b)
        except:
            pass
        PlayerData.MUSIC_VOLUME = self.volume_value
        PlayerData.PLAYER_VOLUME = self.player_volume
        PlayerData.PLAYER_DEATH_VOLUME = self.player_death_value
        PlayerData.save()
        pygame.mixer.music.set_volume(PlayerData.MUSIC_VOLUME)

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