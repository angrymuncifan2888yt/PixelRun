from data import Skins
from ui import UiObject
from core import World, GravityPortal, Platform, JumpOrb, GravityOrb, Player, NormalGravityPortal, UpsideDownPortal
from core.render import render_entity
from event import EventType
from util import player_click, player_input
import pygame
import math


class MainMenuBackground(UiObject):
    def __init__(self):
        super().__init__(pygame.Vector2(0, 0))

        self.world = World()
        self.time = 0

        self._build_scene()

    def click(self):
        self.player.is_clicking = True

    def handle_pygame_event(self, pygame_event):
        player_click(self.player, pygame_event, False)
        
    def _build_scene(self):
        self.moving_platforms = []
        self.base_positions = []

        positions = [(50, 700), (300, 550), (600, 500)]
        for pos in positions:
            plat = Platform(
                self.world,
                pygame.Vector2(pos),
                width=150,
                height=20,
                color=(120, 120, 255)
            )
            self.world.add_entity(plat)
            self.moving_platforms.append(plat)
            self.base_positions.append(pygame.Vector2(pos))

        self.portals = [
            GravityPortal(self.world, pygame.Vector2(200, 350), rotation=90),
            GravityPortal(self.world, pygame.Vector2(800, 200), rotation=270),
            NormalGravityPortal(self.world, pygame.Vector2(1100, 150), rotation=90),
            UpsideDownPortal(self.world, pygame.Vector2(1100, 600), rotation=270)
        ]
        for portal in self.portals:
            self.world.add_entity(portal)

        self.jump_orbs = [
            JumpOrb(self.world, pygame.Vector2(350, 450)),
            JumpOrb(self.world, pygame.Vector2(550, 300))
        ]
        for orb in self.jump_orbs:
            self.world.add_entity(orb)

        self.gravity_orbs = [
            GravityOrb(self.world, pygame.Vector2(700, 250))
        ]
        for orb in self.gravity_orbs:
            self.world.add_entity(orb)

        self.player = Player(self.world, pygame.Vector2(1100, 500), Skins.DEFAULT)
        self.world.add_entity(
            self.player
        )
        self.world.add_entity(
            Platform(self.world, pygame.Vector2(1000, 0), width=200, height=25, color=(255, 0, 0)),
        )
        self.world.add_entity(
            Platform(self.world, pygame.Vector2(1000, 775), width=200, height=25, color=(255, 0, 0)),
        )
        self.world.event_bus.subscribe(EventType.PLAYER_DEATH, self._on_player_death)
    
    def _on_player_death(self, event):
        self.player.respawn()

    def update(self, delta, player_input_=True):
        self.time += delta

        for i, plat in enumerate(self.moving_platforms):
            base = self.base_positions[i]
            plat.position.x = base.x + math.sin(self.time + i) * 40
            plat.position.y = base.y + math.cos(self.time * 0.8 + i) * 10

        for i, orb in enumerate(self.jump_orbs):
            orb.position.y += math.sin(self.time * 2 + i) * 0.3

        for i, orb in enumerate(self.gravity_orbs):
            orb.position.x += math.cos(self.time * 1.5 + i) * 0.2

        self.world.update_all_hitboxes()
        self.world.update_entities(self.world.entities, delta)

        self.player.is_clicking = False

        if player_input_:
            player_input(self.player, delta, False)

    def draw(self, screen):
        for entity in self.world.entities:
            render_entity(screen, entity)
            