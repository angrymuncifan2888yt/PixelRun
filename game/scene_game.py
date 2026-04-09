import pygame
from scene import Scene, SceneType
from core import *
from core.render import render_entity, render_hitbox
from util import player_click, player_input, Camera, Timer
from level import Level
from .pause_menu import PauseMenu
from .level_complete import LevelCompleteMenu
from data import Skins, const, Sounds, SoundChannels, PlayerData
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
            lambda: self.scene_manager.set_scene(SceneType.MAIN_MENU),
            lambda: self._on_player_death(None),
            self.play_again
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

        self.player = Player(
            self.world,
            pygame.Vector2(400, 400),
            PlayerData.CUBE_SKIN,
            PlayerData.UFO_SKIN,
            PlayerData.BALL_SKIN,
        )

    def on_enter(self):
        pygame.mixer.music.pause()

    def on_exit(self):
        pygame.mixer.music.unpause()

    def _on_player_reach_end_door(self, event):
        self.level_ended = True
        self.pause = False

    def _on_player_walk(self, event):
        Sounds.play_sound(Sounds.PLAYER_WALK, SoundChannels.GAME, PlayerData.PLAYER_VOLUME)

    def _on_player_jump(self, event):
        Sounds.play_sound(Sounds.PLAYER_JUMP, SoundChannels.GAME, PlayerData.PLAYER_VOLUME)

    def _on_player_death(self, event):
        self.dying_animation = True
        self.player.opacity = 50
        Sounds.play_sound(Sounds.PLAYER_DEATH, SoundChannels.GAME, PlayerData.PLAYER_DEATH_VOLUME)
        self.pause = False

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
        self.player = Player(self.world, self.current_level.player_spawn,
                             self.player.cube_skin, self.player.ufo_skin, self.player.ball_skin)
        level.load_to_world(self.world, self.player)
        self.subscribe_world_event()

    def play_again(self):
        # Очистка мира
        self.world = World()

        # Пересоздаем игрока
        self.player = Player(self.world, self.current_level.player_spawn,
                             self.player.cube_skin, self.player.ufo_skin, self.player.ball_skin)
        # Перезагружаем текущий уровень
        self.load_level(self.current_level)
        self.background_color = self.current_level.background_color
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
            if not self.dying_animation:
                player_click(self.player, event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    self.show_hitboxes = not self.show_hitboxes
                if event.key == pygame.K_F2:
                    self.debug = not self.debug
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self._toogle_pause()
                if event.key == pygame.K_r:
                    self._on_player_death(None)

    def update(self, delta, **kwargs):
        if not self.level_ended:
            if not self.pause:
                if not self.dying_animation:
                    # Upd world
                    entities_to_upd = self.world.get_nearest_entities(self.player.position, PlayerData.WORLD_LOAD_DISTANCE)
                    objects_updated = self.world.update_entities(entities_to_upd, delta)

                    player_input(self.player, delta)
                    self.camera.update(pygame.Vector2(self.player.hitbox.center), delta)
                    self.player.is_clicking = False

                    self.debug_menu.update(delta, kwargs["clock"], self.player, objects_updated)

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
