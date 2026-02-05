import pygame
from core import Player
from ui import UiObject, Text, UiManager
from data import Fonts


class DebugMenu(UiObject):
    def __init__(self, position: pygame.Vector2=pygame.Vector2(0,0)):
        self.ui = UiManager()
        self.text_fps = Text(pygame.Vector2(10, 10), Fonts.NORMAL_30, "")
        self.text_player_pos = Text(pygame.Vector2(10, 45), Fonts.NORMAL_30, "")
        self.ui.add_ui_object(self.text_fps)
        self.ui.add_ui_object(self.text_player_pos)

    def handle_pygame_event(self, pygame_event):
        self.ui.handle_pygame_event(pygame_event)

    def update(self, delta, clock: pygame.time.Clock, player: Player):
        self.text_fps.text = f"FPS: {clock.get_fps():.2f}"
        self.text_player_pos.text = f"x: {player.position.x:.2f}, y: {player.position.y:.2f}"

    def draw(self, screen):
        self.ui.draw(screen)