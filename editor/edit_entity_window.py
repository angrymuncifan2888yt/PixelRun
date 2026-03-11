import pygame
from ui import NormalButton, LineEdit
from ui.ui_manager import UiManager
from data import Fonts
from window import Window, WindowType

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 750


class EditEntityWindow(Window):

    def __init__(self, manager, entities, screen_size):
        super().__init__(manager, WindowType.EDIT_ENTITY)

        self.entities = entities if entities else []
        self.screen_size = screen_size
        self.ui = UiManager()

        self.rect = pygame.Rect(
            screen_size[0] // 2 - WINDOW_WIDTH // 2,
            screen_size[1] // 2 - WINDOW_HEIGHT // 2,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        entity_ids = ""
        pos_x = 0
        pos_y = 0
        opacity = 255
        rotation = 0
        width = 100
        height = 100
        active_state = True

        if self.entities:
            entity_ids = ", ".join(str(e.id) for e in self.entities)
            first = self.entities[0]

            pos_x = int(first.position.x)
            pos_y = int(first.position.y)
            opacity = int(first.opacity)

            if hasattr(first, "rotation"):
                rotation = int(first.rotation)

            if hasattr(first, "width"):
                width = int(first.width)

            if hasattr(first, "height"):
                height = int(first.height)

            if hasattr(first, "active"):
                active_state = first.active

        self.active_state = active_state

        base_x = self.rect.x + 350

        self.input_id = LineEdit(
            (base_x, self.rect.y + 120),
            (350, 45),
            Fonts.NORMAL_30,
            max_length=128
        )
        self.input_id.text = entity_ids
        self.ui.add_ui_object(self.input_id)

        self.input_pos_x = LineEdit(
            (base_x, self.rect.y + 210),
            (140, 45),
            Fonts.NORMAL_30,
            max_length=6
        )
        self.input_pos_x.text = str(pos_x)
        self.ui.add_ui_object(self.input_pos_x)

        self.input_pos_y = LineEdit(
            (base_x + 170, self.rect.y + 210),
            (140, 45),
            Fonts.NORMAL_30,
            max_length=6
        )
        self.input_pos_y.text = str(pos_y)
        self.ui.add_ui_object(self.input_pos_y)

        self.input_opacity = LineEdit(
            (base_x, self.rect.y + 300),
            (140, 45),
            Fonts.NORMAL_30,
            max_length=3
        )
        self.input_opacity.text = str(opacity)
        self.ui.add_ui_object(self.input_opacity)

        self.input_rotation = LineEdit(
            (base_x, self.rect.y + 390),
            (140, 45),
            Fonts.NORMAL_30,
            max_length=4
        )
        self.input_rotation.text = str(rotation)
        self.ui.add_ui_object(self.input_rotation)

        self.input_width = LineEdit(
            (base_x, self.rect.y + 480),
            (140, 45),
            Fonts.NORMAL_30,
            max_length=5
        )
        self.input_width.text = str(width)
        self.ui.add_ui_object(self.input_width)

        self.input_height = LineEdit(
            (base_x + 170, self.rect.y + 480),
            (140, 45),
            Fonts.NORMAL_30,
            max_length=5
        )
        self.input_height.text = str(height)
        self.ui.add_ui_object(self.input_height)

        self.btn_active = NormalButton(
            position=pygame.Vector2(base_x, self.rect.y + 570),
            size=(220, 55),
            text="Active" if active_state else "Inactive",
            font=Fonts.NORMAL_30,
            color=(0, 200, 0) if active_state else (200, 0, 0),
            callback=self.toggle_active
        )

        self.btn_active.hover_color = (0, 150, 0) if active_state else (150, 0, 0)
        self.ui.add_ui_object(self.btn_active)

        button_y1 = self.rect.bottom - 170
        button_y2 = self.rect.bottom - 90

        spacing = 240
        start_x = self.rect.x + 40

        self.btn_apply_all = NormalButton(
            position=pygame.Vector2(240, button_y2),
            size=(200, 55),
            text="Apply All",
            font=Fonts.NORMAL_30,
            callback=self.apply_all
        )
        self.btn_apply_id = NormalButton(
            position=pygame.Vector2(base_x + 360, self.rect.y + 120),  # рядом с ID
            size=(140, 45),
            text="Apply ID",
            font=Fonts.NORMAL_30,
            callback=self.apply_id
        )
        self.ui.add_ui_object(self.btn_apply_id)

        self.btn_apply_pos = NormalButton(
            position=pygame.Vector2(base_x + 360, self.rect.y + 210),  # рядом с Pos
            size=(140, 45),
            text="Apply Position",
            font=Fonts.NORMAL_30,
            callback=self.apply_position
        )
        self.ui.add_ui_object(self.btn_apply_pos)

        self.btn_apply_opacity = NormalButton(
            position=pygame.Vector2(base_x + 360, self.rect.y + 300),  # рядом с Opacity
            size=(140, 45),
            text="Apply Opacity",
            font=Fonts.NORMAL_30,
            callback=self.apply_opacity
        )
        self.ui.add_ui_object(self.btn_apply_opacity)

        self.btn_apply_rotation = NormalButton(
            position=pygame.Vector2(base_x + 360, self.rect.y + 390),  # рядом с Rotation
            size=(140, 45),
            text="Apply Rotation",
            font=Fonts.NORMAL_30,
            callback=self.apply_rotation
        )
        self.ui.add_ui_object(self.btn_apply_rotation)

        self.btn_apply_size = NormalButton(
            position=pygame.Vector2(base_x + 360, self.rect.y + 480),  # рядом с Size
            size=(140, 45),
            text="Apply Size",
            font=Fonts.NORMAL_30,
            callback=self.apply_size
        )
        self.ui.add_ui_object(self.btn_apply_size)

        self.btn_apply_active = NormalButton(
            position=pygame.Vector2(base_x + 360, self.rect.y + 570),  # рядом с Active
            size=(140, 45),
            text="Apply Active",
            font=Fonts.NORMAL_30,
            callback=self.apply_active
        )
        self.ui.add_ui_object(self.btn_apply_active)
        self.btn_close = NormalButton(
            position=pygame.Vector2(self.rect.right - 240, button_y2),
            size=(200, 55),
            text="Close",
            font=Fonts.NORMAL_30,
            callback=self.close
        )
        for btn in [
            self.btn_apply_all,
            self.btn_close
        ]:
            self.ui.add_ui_object(btn)

    def update_active_button(self):
        if self.active_state:
            self.btn_active.text = "Active"
            self.btn_active.color = (0, 200, 0)
            self.btn_active.hover_color = (0, 150, 0)
        else:
            self.btn_active.text = "Inactive"
            self.btn_active.color = (200, 0, 0)
            self.btn_active.hover_color = (150, 0, 0)
    def load_entity_data(self):
        if not self.entities:
            self.input_id.text = ""
            self.input_pos_x.text = "0"
            self.input_pos_y.text = "0"
            self.input_opacity.text = "255"
            self.input_rotation.text = "0"
            self.input_width.text = "100"
            self.input_height.text = "100"
            self.active_state = True
            self.update_active_button()
            return

        first = self.entities[0]

        self.input_id.text = ", ".join(str(e.id) for e in self.entities)
        self.input_pos_x.text = str(int(first.position.x))
        self.input_pos_y.text = str(int(first.position.y))
        self.input_opacity.text = str(int(first.opacity))
        self.input_rotation.text = str(int(getattr(first, "rotation", 0)))
        self.input_width.text = str(int(getattr(first, "width", 100)))
        self.input_height.text = str(int(getattr(first, "height", 100)))
        self.active_state = getattr(first, "active", True)
        self.update_active_button()
        
    def toggle_active(self):

        self.active_state = not self.active_state

        if self.active_state:
            self.btn_active.text = "Active"
            self.btn_active.color = (0, 200, 0)
            self.btn_active.hover_color = (0, 150, 0)
        else:
            self.btn_active.text = "Inactive"
            self.btn_active.color = (200, 0, 0)
            self.btn_active.hover_color = (150, 0, 0)

    def apply_position(self):

        if not self.input_pos_x.text.isdigit():
            return
        if not self.input_pos_y.text.isdigit():
            return

        pos = pygame.Vector2(
            int(self.input_pos_x.text),
            int(self.input_pos_y.text)
        )

        for entity in self.entities:
            entity.position = pos

    def apply_opacity(self):

        if not self.input_opacity.text.isdigit():
            return

        opacity = max(0, min(255, int(self.input_opacity.text)))

        for entity in self.entities:
            entity.opacity = opacity

    def apply_rotation(self):

        if not self.input_rotation.text.isdigit():
            return

        rotation = int(self.input_rotation.text) % 360

        for entity in self.entities:
            if hasattr(entity, "rotation"):
                entity.rotation = rotation

    def apply_size(self):

        if not self.input_width.text.isdigit():
            return
        if not self.input_height.text.isdigit():
            return

        width = int(self.input_width.text)
        height = int(self.input_height.text)

        for entity in self.entities:
            if hasattr(entity, "width"):
                entity.width = width
            if hasattr(entity, "height"):
                entity.height = height

    def apply_id(self):

        ids = [i.strip() for i in self.input_id.text.split(",") if i.strip()]

        if not ids:
            return

        for i, entity in enumerate(self.entities):

            if i < len(ids):
                entity.id = ids[i]
            else:
                entity.id = ids[-1]

    def apply_active(self):

        for entity in self.entities:
            entity.active = self.active_state

    def apply_all(self):

        self.apply_id()
        self.apply_position()
        self.apply_opacity()
        self.apply_rotation()
        self.apply_size()
        self.apply_active()

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

        screen.blit(font.render("EDIT ENTITIES", True, (255, 255, 255)), (self.rect.x + 40, self.rect.y + 40))

        screen.blit(font.render("Object ID(s):", True, (255, 255, 255)), (self.rect.x + 40, self.rect.y + 125))
        screen.blit(font.render("Position (X Y):", True, (255, 255, 255)), (self.rect.x + 40, self.rect.y + 215))
        screen.blit(font.render("Opacity (0-255):", True, (255, 255, 255)), (self.rect.x + 40, self.rect.y + 305))
        screen.blit(font.render("Rotation:", True, (255, 255, 255)), (self.rect.x + 40, self.rect.y + 395))
        screen.blit(font.render("Size (W H):", True, (255, 255, 255)), (self.rect.x + 40, self.rect.y + 485))
        screen.blit(font.render("Active State:", True, (255, 255, 255)), (self.rect.x + 40, self.rect.y + 575))

        self.ui.draw(screen)