import pygame
from scene import Scene, SceneType
from core import *
from core.render import render_world
from util import PlayerDirection, Camera
from level import Level
from .pause_menu import PauseMenu
from .level_complete import LevelCompleteMenu
from data import Skins, const, Levels
from event import EventType


class SceneGame(Scene):
    def __init__(self, scene_manager) -> None:
        super().__init__(scene_manager, SceneType.GAME)

        self.debug = False
        self.pause = False
        self.level_ended = False
        self.background_color = (0, 0, 0)

        self.pause_menu = PauseMenu(
            pygame.Vector2(0, 0),
            const.WINDOW_SIZE,
            self._toogle_pause,
            lambda: self.scene_manager.set_scene(SceneType.MAIN_MENU)
        )
        self.level_complete_menu = LevelCompleteMenu(
            pygame.Vector2(0, 0),
            const.WINDOW_SIZE,
            on_menu=lambda: self.scene_manager.set_scene(SceneType.MAIN_MENU),
            on_play_again=self.play_again,
            on_levels=lambda: self.scene_manager.set_scene(SceneType.LEVELS)
        )

        self.camera = Camera(pygame.Vector2(0, 0), *const.WINDOW_SIZE)
        self.world = World()
        self.world.event_bus.subscribe(EventType.PLAYER_TOUCH_END_DOOR, self._on_player_reach_end_door)
        self.world.event_bus.subscribe(EventType.CHANGE_BACKGROUND_COLOR, self._on_change_background_color)

        self.player = Player(self.world, pygame.Vector2(400, 400), Skins.CAT_JARD)
        self.load_level(Levels.Level1)

    def set_skin(self, skin):
        self.player.set_skin(skin)

    def _on_player_reach_end_door(self, event):
        self.level_ended = True
        self.pause = False

    def _on_change_background_color(self, event):
        self.background_color = event.data["color"]

    def _toogle_pause(self):
        if not self.level_ended:  # нельзя ставить на паузу после конца уровня
            self.pause = not self.pause

    def load_level(self, level: Level):
        self.current_level = level  # сохраняем текущий уровень для play_again
        self.background_color = level.background_color
        self.level_ended = False
        self.camera.position = self.player.position.copy()
        level.load_to_world(self.world, self.player)

    def play_again(self):
        # Очистка мира
        self.world = World()
        self.world.event_bus.subscribe(EventType.PLAYER_TOUCH_END_DOOR, self._on_player_reach_end_door)

        # Пересоздаем игрока
        self.player = Player(self.world, self.current_level.player_spawn, self.player.skin)

        # Перезагружаем текущий уровень
        self.load_level(self.current_level)
        self.level_ended = False
        self.pause = False

    def handle_pygame_event(self, event):
        if self.level_ended:
            self.level_complete_menu.handle_pygame_event(event)
        elif self.pause:
            self.pause_menu.handle_pygame_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self._toogle_pause()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.debug = not self.debug
                if event.key == pygame.K_SPACE:
                    self.player.is_clicking = True
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self._toogle_pause()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.player.is_clicking = True

    def update(self, delta, **kwargs):
        if not self.level_ended:
            if not self.pause:
                self.world.update(delta)
                self.camera.update(pygame.Vector2(self.player.hitbox.center))
                self.player.is_clicking = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.player.jump()
                if keys[pygame.K_a]:
                    self.player.move_left(delta)
                elif keys[pygame.K_d]:
                    self.player.move_right(delta)

                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    self.player.jump()
            else:
                self.pause_menu.update(delta)
        else:
            self.level_complete_menu.update(delta)  # обновляем меню конца уровня

    def draw(self, screen):
        screen.fill(self.background_color)
        render_world(screen, self.world, self.camera, self.debug)
        if self.pause:
            self.pause_menu.draw(screen)
        if self.level_ended:
            self.level_complete_menu.draw(screen)
