import pygame
from ui import NormalButton, LineEdit
from ui.ui_manager import UiManager
from data import Fonts
from window import Window, WindowType

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 750


class EditSpecialWindow(Window):

    def __init__(self, manager, entities, screen_size):
        super().__init__(manager, WindowType.EDIT_SPECIAL_ENTITY)

        self.entities = entities if entities else []
        self.screen_size = screen_size
        self.ui = UiManager()

        self.rect = pygame.Rect(
            screen_size[0] // 2 - WINDOW_WIDTH // 2,
            screen_size[1] // 2 - WINDOW_HEIGHT // 2,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        self.inputs = {}
        self.fields = {}
        button_y = self.rect.bottom - 90

        self.btn_close = NormalButton(
            position=pygame.Vector2(self.rect.right - 240, button_y),
            size=(200, 55),
            text="Close",
            font=Fonts.NORMAL_30,
            callback=self.close
        )

        self.ui.add_ui_object(self.btn_close)

    def load_entity_data(self):
        self.ui.ui_objects = [self.btn_close]
        self.inputs.clear()

        if not self.entities:
            return

        entity = self.entities[0]
        self.fields = entity.get_special_fields()

        base_x = self.rect.x + 350
        start_y = self.rect.y + 200
        spacing = 80

        for i, (key, info) in enumerate(self.fields.items()):
            y = start_y + i * spacing

            input_box = LineEdit(
                (base_x, y),
                (200, 45),
                Fonts.NORMAL_30
            )
            input_box.text = str(info.get("value", ""))
            self.ui.add_ui_object(input_box)

            self.inputs[key] = (input_box, info.get("type", "str"))

            btn_apply = NormalButton(
                position=pygame.Vector2(base_x + 250, y),
                size=(180, 45),
                text=f"Apply {key}",
                font=Fonts.NORMAL_25,
                callback=lambda k=key: self.apply_one(k)
            )
            self.ui.add_ui_object(btn_apply)

        button_y = self.rect.bottom - 90

        self.btn_apply_all = NormalButton(
            position=pygame.Vector2(self.rect.x + 240, button_y),
            size=(200, 55),
            text="Apply All",
            font=Fonts.NORMAL_30,
            callback=self.apply_all
        )

        self.ui.add_ui_object(self.btn_apply_all)

    def convert_value(self, text, type_):
        try:
            if type_ == "int":
                return int(text)
            if type_ == "float":
                return float(text)
            if type_ == "bool":
                return text.lower() in ["1", "true", "yes"]
            return text
        except:
            return None

    def apply_one(self, key):
        input_box, type_ = self.inputs[key]
        value = self.convert_value(input_box.text, type_)

        if value is None:
            return

        for entity in self.entities:
            entity.apply_special_fields({key: value})

    def apply_all(self):
        data = {}

        for key, (input_box, type_) in self.inputs.items():
            value = self.convert_value(input_box.text, type_)
            if value is not None:
                data[key] = value

        for entity in self.entities:
            entity.apply_special_fields(data)

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
            font.render("EDIT SPECIAL", True, (255, 255, 255)),
            (self.rect.x + 40, self.rect.y + 40)
        )

        for i, (key, info) in enumerate(self.fields.items()):
            y = self.rect.y + 205 + i * 80

            label = info.get("label", key)
            screen.blit(
                font.render(label + ":", True, (255, 255, 255)),
                (self.rect.x + 40, y + 5)
            )

        self.ui.draw(screen)