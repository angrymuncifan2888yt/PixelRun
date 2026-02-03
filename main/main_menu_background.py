from ui import UiObject
from core import Player, World, GravityPortal, Platform, JumpOrb, GravityOrb
from core.render import render_world
from data import Skins
import pygame
import math

class MainMenuBackground(UiObject):
    def __init__(self):
        super().__init__(pygame.Vector2(0, 0))
        self.world = World()

        # Игрок для фона
        self.bg_player = Player(self.world, pygame.Vector2(100, 500), Skins.CAT_JARD)
        self.world.add_entity(self.bg_player)
        self.world.add_entity(GravityPortal(self.world, pygame.Vector2(100, 300), rotation=90))

        # Платформы
        self.moving_platforms = []
        positions = [(50, 700), (300, 550), (600, 500)]
        for pos in positions:
            plat = Platform(self.world, pygame.Vector2(pos), width=150, height=20, color=(120,120,255))
            self.world.add_entity(plat)
            self.moving_platforms.append(plat)

        # JumpOrb
        self.jump_orbs = [
            JumpOrb(self.world, pygame.Vector2(100, 50))
        ]
        for orb in self.jump_orbs:
            self.world.add_entity(orb)

        # GravityOrb
        self.gravity_orbs = [
            
        ]
        for orb in self.gravity_orbs:
            self.world.add_entity(orb)

        self.time = 0
        self.world_time_multiplier = 0.5 # Slow mo

    def update(self, delta, **kwargs):
        self.time += delta

        # Двигаем платформы влево/вправо синусоидой
        for i, plat in enumerate(self.moving_platforms):
            plat.position.x += math.sin(self.time + i) * 0.5

        # Проверка столкновения игрока с JumpOrb
        player_rect = self.bg_player.hitbox
        for orb in self.jump_orbs:
            if player_rect.colliderect(orb.hitbox):
                self.bg_player.is_clicking = True
                self.bg_player.jump()

        # Проверка столкновения игрока с GravityOrb
        for orb in self.gravity_orbs:
            if player_rect.colliderect(orb.hitbox):
                self.bg_player.reverse_gravity()

        # Обновляем мир
        self.world.update(delta * self.world_time_multiplier)
        self.bg_player.jump()

    def draw(self, screen):
        render_world(screen, self.world)
