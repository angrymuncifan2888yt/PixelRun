from ui import UiObject, UiManager, Text
from data import Fonts
import pygame
from core import Player


class DebugMenu(UiObject):
    def __init__(self, position: pygame.Vector2=pygame.Vector2(0,0)):
        self.ui = UiManager()
        self.text_fps = Text(pygame.Vector2(10, 10), Fonts.NORMAL_30, "")
        self.text_player_pos = Text(pygame.Vector2(10, 45), Fonts.NORMAL_30, "")
        self.text_objects_updated = Text(pygame.Vector2(10, 80), Fonts.NORMAL_30, "")
        self.text_hitboxes_updated = Text(pygame.Vector2(10, 115), Fonts.NORMAL_30, "")
        self.text_entities_rendered = Text(pygame.Vector2(10, 150), Fonts.NORMAL_30, "")
        self.ui.add_ui_object(self.text_fps)
        self.ui.add_ui_object(self.text_player_pos)
        self.ui.add_ui_object(self.text_objects_updated)
        self.ui.add_ui_object(self.text_hitboxes_updated)
        self.ui.add_ui_object(self.text_entities_rendered)

    def handle_pygame_event(self, pygame_event):
        self.ui.handle_pygame_event(pygame_event)

    def update(
        self, 
        delta, 
        clock: pygame.time.Clock, 
        player: Player, 
        objects_updated: int, 
        hitboxes_updated: int,
        entities_rendered: int = 0   # новый параметр
    ):
        self.text_hitboxes_updated.text = f"Hitboxes updated: {hitboxes_updated}"
        self.text_fps.text = f"FPS: {clock.get_fps():.2f}"
        self.text_player_pos.text = f"x: {player.position.x:.2f}, y: {player.position.y:.2f}"
        self.text_objects_updated.text = f"Objects updated: {objects_updated}"
        self.text_entities_rendered.text = f"Entities rendered: {entities_rendered}"

    def draw(self, screen):
        self.ui.draw(screen)
