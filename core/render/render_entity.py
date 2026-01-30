import pygame
from util import Camera, PlayerDirection
from .. import *
from data import Sprites


def render_player(screen, player, camera=None):
    # Получаем позицию на экране
    pos = camera.get_screen_position(player.position) if camera else player.position

    # Выбираем спрайт в зависимости от направления игрока
    if player.direction == PlayerDirection.LEFT:
        sprite = player.animator.get_current_sprite(player.skin.animations)
        flip_x = True
    elif player.direction == PlayerDirection.RIGHT:
        sprite = player.animator.get_current_sprite(player.skin.animations)
        flip_x = False
    else:
        sprite = player.skin.standing_sprite
        flip_x = False
        
    # Вращение вокруг центра спрайта
    rotated_sprite = pygame.transform.rotate(sprite, player.rotation)
    sprite_rect = rotated_sprite.get_rect(center=(int(pos.x + player.width / 2),
                                                  int(pos.y + player.height / 2)))

    screen.blit(rotated_sprite, sprite_rect)


def render_surface_entity(screen, entity, color=(255, 255, 255), camera=None):
    # Общий метод для прямоугольных объектов с цветом
    pos = camera.get_screen_position(entity.position) if camera else entity.position

    surface = pygame.Surface((entity.width, entity.height), pygame.SRCALPHA)
    surface.fill(color)

    rotated_surface = pygame.transform.rotate(surface, entity.rotation)
    rect = rotated_surface.get_rect(center=(int(pos.x + entity.width / 2),
                                            int(pos.y + entity.height / 2)))

    screen.blit(rotated_surface, rect)


def render_platform(screen, platform, camera=None):
    render_surface_entity(screen, platform, color=platform.color, camera=camera)


def render_jump_pad(screen, jump_pad, camera=None):
    render_surface_entity(screen, jump_pad, color=jump_pad.color, camera=camera)


def render_gravity_portal(screen, portal, camera=None):
    pos = camera.get_screen_position(portal.position) if camera else portal.position
    sprite = Sprites.GRAVITY_PORTAL
    rotated_sprite = pygame.transform.rotate(sprite, portal.rotation)
    rect = rotated_sprite.get_rect(center=(int(pos.x + portal.width / 2),
                                           int(pos.y + portal.height / 2)))
    screen.blit(rotated_sprite, rect)


def render_spike(screen, spike, camera=None):
    pos = camera.get_screen_position(spike.position) if camera else spike.position
    sprite = Sprites.SPIKE
    rotated_sprite = pygame.transform.rotate(sprite, spike.rotation)
    rect = rotated_sprite.get_rect(center=(int(pos.x + spike.width / 2),
                                           int(pos.y + spike.height / 2)))
    screen.blit(rotated_sprite, rect)


def render_checkpoint(screen, checkpoint, camera=None):
    pos = camera.get_screen_position(checkpoint.position) if camera else checkpoint.position
    sprite = Sprites.CHECKPOINT
    rotated_sprite = pygame.transform.rotate(sprite, checkpoint.rotation)
    rect = rotated_sprite.get_rect(center=(int(pos.x + checkpoint.width / 2),
                                           int(pos.y + checkpoint.height / 2)))
    screen.blit(rotated_sprite, rect)


def render_jump_orb(screen, jump_orb, camera=None):
    pos = camera.get_screen_position(jump_orb.position) if camera else jump_orb.position
    sprite = Sprites.JUMP_ORB
    rotated_sprite = pygame.transform.rotate(sprite, jump_orb.rotation)
    rect = rotated_sprite.get_rect(center=(int(pos.x + jump_orb.width / 2),
                                           int(pos.y + jump_orb.height / 2)))
    screen.blit(rotated_sprite, rect)


def render_gravity_orb(screen, gravity_orb, camera=None):
    pos = camera.get_screen_position(gravity_orb.position) if camera else gravity_orb.position
    sprite = Sprites.GRAVITY_ORB
    rotated_sprite = pygame.transform.rotate(sprite, gravity_orb.rotation)
    rect = rotated_sprite.get_rect(center=(int(pos.x + gravity_orb.width / 2),
                                           int(pos.y + gravity_orb.height / 2)))
    screen.blit(rotated_sprite, rect)

def render_end_door(screen, end_door, camera=None):
    pos = camera.get_screen_position(end_door.position) if camera else end_door.position
    sprite = Sprites.END_DOOR
    rotated_sprite = pygame.transform.rotate(sprite, end_door.rotation)
    rect = rotated_sprite.get_rect(center=(int(pos.x + end_door.width / 2),
                                           int(pos.y + end_door.height / 2)))
    screen.blit(rotated_sprite, rect)

# Словарь для быстрого выбора функции рендеринга по классу
entity_renderers = {
    Player: render_player,
    Platform: render_platform,
    GravityPortal: render_gravity_portal,
    JumpPad: render_jump_pad,
    Spike: render_spike,
    Checkpoint: render_checkpoint,
    JumpOrb: render_jump_orb,
    GravityOrb: render_gravity_orb,
    EndDoor: render_end_door
}


def render_entity(screen, entity: Entity, camera: Camera = None):
    # Вызываем соответствующую функцию из словаря
    renderer = entity_renderers.get(type(entity))
    if renderer:
        renderer(screen, entity, camera)
