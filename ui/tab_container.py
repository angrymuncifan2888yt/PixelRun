import pygame
from .ui_object import UiObject


class TabContainer(UiObject):
    def __init__(self, position, size, show_tabs=False):
        super().__init__(position)
        self.show_tabs = show_tabs
        self.size = size

        self.tabs = []  # [[ui_objects]]
        self.current_tab = 0

        self.tab_height = 40

        self.bg_color = (40, 40, 40)
        self.tab_color = (70, 70, 70)
        self.active_tab_color = (120, 120, 120)

    def add_tab(self, objects):
        for obj in objects:
            obj.parent = self
        self.tabs.append(objects)

    def next_tab(self):
        if not self.tabs:
            return
        self.current_tab = (self.current_tab + 1) % len(self.tabs)

    def prev_tab(self):
        if not self.tabs:
            return
        self.current_tab = (self.current_tab - 1) % len(self.tabs)
        
    def handle_pygame_event(self, event):
        pos = self.get_global_position()

        # 🖱️ клик по вкладкам
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.tabs:
                return

            tab_width = self.size[0] // len(self.tabs)

            for i in range(len(self.tabs)):
                rect = pygame.Rect(
                    pos.x + i * tab_width,
                    pos.y,
                    tab_width,
                    self.tab_height
                )

                if rect.collidepoint(event.pos):
                    self.current_tab = i
                    return

        # 🖱️ колесо мыши
        if event.type == pygame.MOUSEWHEEL and self.tabs:
            self.current_tab -= event.y
            self.current_tab %= len(self.tabs)

        # события текущей вкладке
        if self.tabs:
            for obj in self.tabs[self.current_tab]:
                obj.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        if self.tabs:
            for obj in self.tabs[self.current_tab]:
                obj.update(delta, **kwargs)

    def draw(self, screen):
        pos = self.get_global_position()

        # фон
        pygame.draw.rect(
            screen,
            self.bg_color,
            (pos.x, pos.y, self.size[0], self.size[1])
        )

        if not self.tabs:
            return

        tab_width = self.size[0] // len(self.tabs)

        if self.show_tabs:
            # 🔝 рисуем вкладки (просто полоски)
            for i in range(len(self.tabs)):
                rect = pygame.Rect(
                    pos.x + i * tab_width,
                    pos.y,
                    tab_width,
                    self.tab_height
                )

                color = self.active_tab_color if i == self.current_tab else self.tab_color
                pygame.draw.rect(screen, color, rect)

        # 📦 рисуем содержимое
        for obj in self.tabs[self.current_tab]:
            obj.draw(screen)