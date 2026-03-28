import pygame
from ui import NormalButton, LineEdit
from ui.ui_manager import UiManager
from data import Fonts
from window import Window, WindowType

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600


class EditEntityIDWindow(Window):

    def __init__(self, manager, entities, screen_size):
        super().__init__(manager, WindowType.EDIT_ID_ENTITY)

        self.entities = entities
        self.screen_size = screen_size
        self.ui = UiManager()

        self.rect = pygame.Rect(
            screen_size[0] // 2 - WINDOW_WIDTH // 2,
            screen_size[1] // 2 - WINDOW_HEIGHT // 2,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        self.base_x = self.rect.x + 120
        self.start_y = self.rect.y + 140

        self.id_inputs = []
        self.remove_buttons = []

        self.load_entity_data()

        self.btn_add = NormalButton(
            position=pygame.Vector2(self.base_x, self.rect.bottom - 150),
            size=(200, 45),
            text="Add ID",
            font=Fonts.NORMAL_30,
            callback=self.add_id_field
        )

        self.btn_apply = NormalButton(
            position=pygame.Vector2(self.rect.x + 140, self.rect.bottom - 80),
            size=(200, 50),
            text="Apply",
            font=Fonts.NORMAL_30,
            callback=self.apply_ids
        )

        self.btn_close = NormalButton(
            position=pygame.Vector2(self.rect.right - 340, self.rect.bottom - 80),
            size=(200, 50),
            text="Close",
            font=Fonts.NORMAL_30,
            callback=self.close
        )

        self.ui.add_ui_object(self.btn_add)
        self.ui.add_ui_object(self.btn_apply)
        self.ui.add_ui_object(self.btn_close)

    def clear_id_fields(self):

        for field in self.id_inputs:
            self.ui.remove_ui_object(field)

        for btn in self.remove_buttons:
            self.ui.remove_ui_object(btn)

        self.id_inputs.clear()
        self.remove_buttons.clear()

    def load_entity_data(self):

        self.clear_id_fields()

        if not self.entities:
            self.add_id_field()
            return

        ent = self.entities[0]

        if isinstance(ent.id, list):

            for ent_id in ent.id:
                self.add_id_field(str(ent_id))

        else:
            self.add_id_field(str(ent.id))

    def add_id_field(self, text=""):

        index = len(self.id_inputs)
        y = self.start_y + index * 45

        input_id = LineEdit(
            (self.base_x, y),
            (260, 40),
            Fonts.NORMAL_30,
            max_length=64
        )

        input_id.text = text

        btn_remove = NormalButton(
            position=pygame.Vector2(self.base_x + 270, y),
            size=(40, 40),
            text="X",
            font=Fonts.NORMAL_30,
            callback=lambda i=index: self.remove_id_field(i)
        )

        self.id_inputs.append(input_id)
        self.remove_buttons.append(btn_remove)

        self.ui.add_ui_object(input_id)
        self.ui.add_ui_object(btn_remove)

    def remove_id_field(self, index):

        if index < 0 or index >= len(self.id_inputs):
            return

        field = self.id_inputs.pop(index)
        btn = self.remove_buttons.pop(index)

        self.ui.remove_ui_object(field)
        self.ui.remove_ui_object(btn)

        self._rebuild_fields()

    def _rebuild_fields(self):

        for i, (field, btn) in enumerate(zip(self.id_inputs, self.remove_buttons)):
            y = self.start_y + i * 45

            field.position = pygame.Vector2(self.base_x, y)
            btn.position = pygame.Vector2(self.base_x + 270, y)

            btn.callback = lambda i=i: self.remove_id_field(i)

    def apply_ids(self):

        ids = []

        for field in self.id_inputs:
            text = field.text.strip()
            if text:
                ids.append(text)

        for entity in self.entities:
            entity.id = ids.copy()

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta):
        self.ui.update(delta)

    def draw(self, screen):

        overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)

        font = Fonts.NORMAL_30

        screen.blit(
            font.render("EDIT ENTITY IDS", True, (255, 255, 255)),
            (self.rect.x + 40, self.rect.y + 40)
        )

        screen.blit(
            font.render("IDs:", True, (255, 255, 255)),
            (self.rect.x + 40, self.rect.y + 140)
        )

        self.ui.draw(screen)