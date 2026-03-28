import pygame
from scene import Scene, SceneType
from core import *
from core.render import render_entity, render_hitbox
from util import PlayerDirection, Camera, Timer
from level import Level
from .pause_menu import PauseMenu
from .level_complete import LevelCompleteMenu
from data import Skins, const, Sounds, SoundChannels, Settings
from event import EventType
from .debug_menu import DebugMenu


class SceneGame(Scene):
    def __init__(self, scene_manager) -> None:
        super().__init__(scene_manager, SceneType.GAME)

        self.show_hitboxes = False
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
        self.debug_menu = DebugMenu()

        self.player_dying_timer = Timer(1)
        self.dying_animation = False

        self.camera = Camera(pygame.Vector2(0, 0), *const.WINDOW_SIZE)
        self.world = World()

        self.player = Player(self.world, pygame.Vector2(400, 400), Skins.DEFAULT)

    def on_enter(self):
        pygame.mixer.music.pause()

    def on_exit(self):
        pygame.mixer.music.unpause()

    def set_skin(self, skin):
        self.player.set_skin(skin)

    def _on_player_reach_end_door(self, event):
        self.level_ended = True
        self.pause = False

    def _on_player_walk(self, event):
        Sounds.play_sound(Sounds.PLAYER_WALK, SoundChannels.GAME)

    def _on_player_jump(self, event):
        Sounds.play_sound(Sounds.PLAYER_JUMP, SoundChannels.GAME)

    def _on_player_death(self, event):
        self.dying_animation = True
        self.player.opacity = 50
        Sounds.play_sound(Sounds.PLAYER_DEATH, SoundChannels.GAME)

    def _toogle_pause(self):
        if not self.level_ended:  # нельзя ставить на паузу после конца уровня
            self.pause = not self.pause

            if self.pause:
                SoundChannels.GAME.pause()
            else:
                SoundChannels.GAME.unpause()

    def subscribe_world_event(self):
        # Subscribe event
        self.world.event_bus.subscribe(EventType.PLAYER_TOUCH_END_DOOR, self._on_player_reach_end_door)
        self.world.event_bus.subscribe(EventType.PLAYER_WALK, self._on_player_walk)
        self.world.event_bus.subscribe(EventType.PLAYER_DEATH, self._on_player_death)
        self.world.event_bus.subscribe(EventType.PLAYER_JUMP, self._on_player_jump)

    def load_level(self, level: Level):
        self.current_level = level  # сохраняем текущий уровень для play_again
        self.background_color = level.background_color
        self.level_ended = False
        self.camera.position = self.player.position.copy()
        self.player = Player(self.world, self.current_level.player_spawn, self.player.skin)
        level.load_to_world(self.world, self.player)
        self.subscribe_world_event()

    def play_again(self):
        # Очистка мира
        self.world = World()

        # Пересоздаем игрока
        self.player = Player(self.world, self.current_level.player_spawn, self.player.skin)

        # Перезагружаем текущий уровень
        self.load_level(self.current_level)
        self.background_color = self.current_level.background_color
        self.level_ended = False
        self.pause = False

    def click(self):
        self.player.is_clicking = True

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
                if event.key == pygame.K_F3:
                    self.show_hitboxes = not self.show_hitboxes
                if event.key == pygame.K_F2:
                    self.debug = not self.debug
                if event.key == pygame.K_SPACE:
                    self.click()
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self._toogle_pause()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.click()

    def update(self, delta, **kwargs):
        if not self.level_ended:
            if not self.pause:
                if not self.dying_animation:
                    # Upd world
                    hitboxes_updated = self.world.update_all_hitboxes()
                    entities_to_upd = self.world.get_nearest_entities(self.player.position, Settings.WORLD_LOAD_DISTANCE)
                    objects_updated = self.world.update_entities(entities_to_upd, delta)

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
                    self.camera.update(pygame.Vector2(self.player.hitbox.center))
                    self.player.is_clicking = False

                    self.debug_menu.update(delta, kwargs["clock"], self.player, objects_updated, hitboxes_updated)

                else:
                    self.player_dying_timer.update(delta)
                    if self.player_dying_timer.finished:
                        self.player_dying_timer.reset()
                        self.dying_animation = False
                        self.player.respawn()
                        self.player.opacity = 255

            else:
                self.pause_menu.update(delta)
        else:
            self.level_complete_menu.update(delta)  # обновляем меню конца уровня

    def draw(self, screen):
        screen.fill(self.world.level_background_color)
        rendered = 0
        for entity in self.world.entities:
            try:
                if self.camera.is_object_visible(entity.position, entity.width, entity.height):
                    render_entity(screen, entity, self.camera)
                    rendered += 1
                    if self.show_hitboxes:
                        render_hitbox(screen, entity.hitbox, self.camera)

            except Exception as e:
                pass
            
        self.debug_menu.text_entities_rendered.text = f"Entities rendered: {rendered}"
        
        if self.debug:
            self.debug_menu.draw(screen)

        if self.pause:
            self.pause_menu.draw(screen)
        if self.level_ended:
            self.level_complete_menu.draw(screen)
