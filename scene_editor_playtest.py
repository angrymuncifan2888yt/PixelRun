import pygame
from scene import Scene, SceneType
from core import *
from core.render import render_entity, render_hitbox
from util import Camera, Timer, player_click, player_input
from level import Level
from data import Skins, const, PlayerData, Sounds, SoundChannels, Fonts
from event import EventType
from game import DebugMenu
from ui import NormalButton

class SceneEditorPlaytest(Scene):
    def __init__(self, scene_manager) -> None:
        super().__init__(scene_manager, SceneType.EDITOR_PLAYTEST)

        self.show_hitboxes = False
        self.debug = False
        self.pause = False
        self.level_ended = False
        self.background_color = (0, 0, 0)

        self.debug_menu = DebugMenu(pygame.Vector2(0, 50))

        self.player_dying_timer = Timer(1)
        self.dying_animation = False

        self.camera = Camera(pygame.Vector2(0, 0), *const.WINDOW_SIZE)
        self.world = World()

        self.player = Player(self.world, pygame.Vector2(400, 400), Skins.DEFAULT)

        self.editor_btn = NormalButton(pygame.Vector2(10, 10),
                                       "Back",
                                       Fonts.NORMAL_25,
                                       lambda: self.scene_manager.set_scene(SceneType.EDITOR),
                                       (120, 40))

    def on_enter(self):
        pygame.mixer.music.pause()

    def on_exit(self):
        pygame.mixer.music.unpause()

    def set_skin(self, skin):
        self.player.set_skin(skin)

    def _on_player_reach_end_door(self, event):
        self.play_again()

    def _on_player_walk(self, event):
        Sounds.play_sound(Sounds.PLAYER_WALK, SoundChannels.GAME)

    def _on_player_jump(self, event):
        Sounds.play_sound(Sounds.PLAYER_JUMP, SoundChannels.GAME)

    def _on_player_death(self, event):
        self.dying_animation = True
        self.player.opacity = 50
        Sounds.play_sound(Sounds.PLAYER_DEATH, SoundChannels.GAME)

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

    def handle_pygame_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                self.show_hitboxes = not self.show_hitboxes
            if event.key == pygame.K_F2:
                self.debug = not self.debug
        player_click(self.player, event)
        self.editor_btn.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        self.editor_btn.update(delta, shit="school")
        if not self.dying_animation:
            # Upd world
            hitboxes_updated = self.world.update_all_hitboxes()
            entities_to_upd = self.world.get_nearest_entities(self.player.position, PlayerData.WORLD_LOAD_DISTANCE)
            objects_updated = self.world.update_entities(entities_to_upd, delta)

            self.camera.update(pygame.Vector2(self.player.hitbox.center))
            self.player.is_clicking = False

            player_input(self.player, delta)
            self.debug_menu.update(delta, kwargs["clock"], self.player, objects_updated, hitboxes_updated)

        else:
            self.player_dying_timer.update(delta)
            if self.player_dying_timer.finished:
                self.player_dying_timer.reset()
                self.dying_animation = False
                self.player.respawn()
                self.player.opacity = 255

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
        self.editor_btn.draw(screen)
