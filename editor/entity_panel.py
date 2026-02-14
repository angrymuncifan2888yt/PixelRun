import pygame
from data import Fonts, Sounds, SoundChannels
from ui import NormalButton, UiObject
from .entity_list import editor_entity_list


class EntityPanel(UiObject):
    def __init__(
        self,
        position: pygame.Vector2,
        width: int,
        height: int,
        entity_classes: list = editor_entity_list
    ):
        super().__init__(position)

        self.width = width
        self.height = height
        self.scroll = 0
        self.scroll_speed = 30
        self.entity_classes = entity_classes
        self.selected_index = None

        self.buttons = []
        self.button_height = 60
        self.margin = 10

        # Создание кнопок
        for i, cls in enumerate(self.entity_classes):
            btn = NormalButton(
                position=pygame.Vector2(self.position.x, self.position.y),
                size=(self.width, self.button_height),
                text=cls.__name__,
                font=Fonts.NORMAL_30,
                callback=lambda i=i: self.select(i)
            )
            self.buttons.append(btn)

    # -----------------------
    # Логика выбора
    # -----------------------

    def select(self, index: int):
        self.selected_index = index

    def get_selected(self):
        if self.selected_index is None:
            return None
        return self.entity_classes[self.selected_index]

    # -----------------------
    # Обработка событий
    # -----------------------

    def handle_pygame_event(self, event):

        # Скролл колесом
        if event.type == pygame.MOUSEWHEEL:
            self.scroll -= event.y * self.scroll_speed

            max_scroll = max(
                0,
                len(self.buttons) * (self.button_height + self.margin) - self.height
            )
            self.scroll = max(0, min(self.scroll, max_scroll))

        # Клик мышью
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mouse_pos = pygame.Vector2(event.pos)

            panel_rect = pygame.Rect(
                self.position.x,
                self.position.y,
                self.width,
                self.height
            )

            # Если клик вне панели — игнорируем
            if not panel_rect.collidepoint(mouse_pos):
                return

            # Проверяем кнопки
            for i in range(len(self.buttons)):

                visual_y = (
                    self.position.y
                    + i * (self.button_height + self.margin)
                    - self.scroll
                )

                btn_rect = pygame.Rect(
                    self.position.x,
                    visual_y,
                    self.width,
                    self.button_height
                )

                if btn_rect.collidepoint(mouse_pos):
                    self.select(i)

                    # Звук нажатия
                    Sounds.play_sound(
                        Sounds.BUTTON_PRESS,
                        SoundChannels.SYSTEM
                    )
                    return

    # -----------------------
    # Обновление
    # -----------------------

    def update(self, delta, **kwargs):
        for btn in self.buttons:
            btn.update(delta, **kwargs)

    def get_rect(self):
        return pygame.Rect(
            self.position.x,
            self.position.y,
            self.width,
            self.height
        )

    # -----------------------
    # Отрисовка
    # -----------------------

    def draw(self, screen):

        panel_rect = pygame.Rect(
            self.position.x,
            self.position.y,
            self.width,
            self.height
        )

        # Фон панели
        pygame.draw.rect(screen, (40, 40, 40), panel_rect)

        # Обводка
        pygame.draw.rect(screen, (120, 120, 120), panel_rect, 5)

        # Клиппинг (обрезаем лишнее)
        previous_clip = screen.get_clip()
        screen.set_clip(panel_rect)

        for i, btn in enumerate(self.buttons):

            visual_y = (
                self.position.y
                + i * (self.button_height + self.margin)
                - self.scroll
            )

            # Если кнопка вне панели — не рисуем
            if (
                visual_y + self.button_height < self.position.y
                or visual_y > self.position.y + self.height
            ):
                continue

            btn_rect = pygame.Rect(
                self.position.x,
                visual_y,
                self.width,
                self.button_height
            )

            # Подсветка выбранной
            if self.selected_index == i:
                pygame.draw.rect(
                    screen,
                    (100, 100, 255),
                    btn_rect
                )

            # Hover эффект
            mouse_pos = pygame.mouse.get_pos()
            if btn_rect.collidepoint(mouse_pos):
                pygame.draw.rect(
                    screen,
                    (70, 70, 70),
                    btn_rect
                )

            # Текст кнопки
            text_surface = btn.font.render(btn.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=btn_rect.center)
            screen.blit(text_surface, text_rect)

        screen.set_clip(previous_clip)
