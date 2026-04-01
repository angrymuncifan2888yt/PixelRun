import pygame
from ..player.gamemode import GameMode
from util import Camera, PlayerDirection
from data import Sprites
from core import (
    Entity,
    Player,
    Platform,
    GravityPortal,
    NormalGravityPortal,
    UpsideDownPortal,
    UFOPortal,
    JumpPad,
    Spike,
    Checkpoint,
    JumpOrb,
    GravityOrb,
    EndDoor,
    ColorTrigger,
    OpacityTrigger,
    MoveTrigger,
    SpawnTrigger,
    ToggleTrigger,
    RotationTrigger,
    Text
)

from .render_utils import (
    get_entity_screen_pos,
    blit_centered,
    get_transformed,
)

# ===============================
# 🎮 ENTITY RENDERERS
# ===============================

def render_player(screen, player: Player, camera=None):
    pos = get_entity_screen_pos(player, camera)

    # 🛸 UFO режим
    if player.gamemode == GameMode.UFO:
        # # 🔼 Иконка игрока сверху по центру
        # icon_size = 100

        # icon_sprite = player.skin.animations[0]

        # icon_sprite = get_transformed(
        #     icon_sprite,
        #     width=icon_size,
        #     height=icon_size,
        #     flip_x=(player.direction == PlayerDirection.LEFT),
        #     angle=0,
        #     opacity=player.opacity,
        # )

        # icon_pos = (
        #     pos[0],
        #     pos[1] - player.height // 2
        # )

        # blit_centered(screen, icon_sprite, icon_pos, icon_size, icon_size)

        base_sprite = get_transformed(
            Sprites.UFO,
            width=player.width,
            height=player.height,
            angle=player.rotation,
            opacity=player.opacity,
        )

        blit_centered(screen, base_sprite, pos, player.width, player.height)
        return

    # 🟩 Обычный режим (Cube и др.)
    sprite = (
        player.animator.get_current_sprite(player.skin.animations)
        if player.is_moving
        else player.skin.standing_sprite
    )

    sprite = get_transformed(
        sprite,
        width=player.width,
        height=player.height,
        flip_x=(player.direction == PlayerDirection.LEFT),
        angle=player.rotation,
        opacity=player.opacity,
    )

    blit_centered(screen, sprite, pos, player.width, player.height)

def render_colored_rect(screen, entity, color, camera=None):
    if entity.opacity <= 0:
        return

    pos = get_entity_screen_pos(entity, camera)

    key = (entity.width, entity.height, color)
    if not hasattr(render_colored_rect, "_cache"):
        render_colored_rect._cache = {}

    surface = render_colored_rect._cache.get(key)
    if surface is None:
        surface = pygame.Surface(
            (entity.width, entity.height), pygame.SRCALPHA
        ).convert_alpha()
        surface.fill(color)
        render_colored_rect._cache[key] = surface

    surface = get_transformed(
        surface,
        width=entity.width,
        height=entity.height,
        angle=entity.rotation,
        opacity=entity.opacity,
    )

    blit_centered(screen, surface, pos, entity.width, entity.height)


def render_sprite_entity(screen, entity, sprite, camera=None):
    if entity.opacity <= 0:
        return

    pos = get_entity_screen_pos(entity, camera)

    sprite = get_transformed(
        sprite,
        width=entity.width,
        height=entity.height,
        angle=entity.rotation,
        opacity=entity.opacity,
    )

    blit_centered(screen, sprite, pos, entity.width, entity.height)


def render_platform(screen, platform: Platform, camera=None):
    render_colored_rect(screen, platform, platform.color, camera)


def render_jump_pad(screen, jump_pad: JumpPad, camera=None):
    render_colored_rect(screen, jump_pad, jump_pad.color, camera)


def render_gravity_portal(screen, portal: GravityPortal, camera=None):
    render_sprite_entity(screen, portal, Sprites.GRAVITY_PORTAL, camera)


def render_upside_down_portal(screen, portal: UpsideDownPortal, camera=None):
    render_sprite_entity(screen, portal, Sprites.UPSIDE_DOWN_PORTAL, camera)


def render_normal_gravity_portal(screen, portal: NormalGravityPortal, camera=None):
    render_sprite_entity(screen, portal, Sprites.NORMAL_GRAVITY_PORTAL, camera)


def render_ufoportal(screen, portal: UFOPortal, camera=None):
    render_sprite_entity(screen, portal, Sprites.UFO_PORTAL, camera)


def render_checkpoint(screen, checkpoint: Checkpoint, camera=None):
    render_sprite_entity(screen, checkpoint, Sprites.CHECKPOINT, camera)


def render_jump_orb(screen, jump_orb: JumpOrb, camera=None):
    render_sprite_entity(screen, jump_orb, Sprites.JUMP_ORB, camera)


def render_gravity_orb(screen, gravity_orb: GravityOrb, camera=None):
    render_sprite_entity(screen, gravity_orb, Sprites.GRAVITY_ORB, camera)


def render_text(screen, text: Text, camera=None):
    if text.opacity <= 0:
        return

    if text._dirty or text._text_surface is None:
        text._update_surface()

    pos = get_entity_screen_pos(text, camera)

    surface = text._text_surface

    # 🟢 AUTO RESIZE (entity под текст)
    if text.auto_resize:
        draw_surface = get_transformed(
            surface,
            width=surface.get_width(),
            height=surface.get_height(),
            angle=text.rotation,
            opacity=text.opacity,
        )

        blit_centered(
            screen,
            draw_surface,
            pos,
            surface.get_width(),
            surface.get_height()
        )

    # 🔵 MANUAL SIZE (текст под entity)
    else:
        draw_surface = get_transformed(
            surface,
            width=text.width,
            height=text.height,
            angle=text.rotation,
            opacity=text.opacity,
        )

        blit_centered(
            screen,
            draw_surface,
            pos,
            text.width,
            text.height
        )
def render_end_door(screen, end_door: EndDoor, camera=None):
    render_sprite_entity(screen, end_door, Sprites.END_DOOR, camera)


def render_color_trigger(screen, trigger: ColorTrigger, camera=None):
    render_sprite_entity(screen, trigger, Sprites.COLOR_TRIGGER, camera)

def render_opacity_trigger(screen, trigger: OpacityTrigger, camera=None):
    render_sprite_entity(screen, trigger, Sprites.OPACITY_TRIGGER, camera)

def render_move_trigger(screen, trigger: MoveTrigger, camera=None):
    render_sprite_entity(screen, trigger, Sprites.MOVE_TRIGGER, camera)

def render_spawn_trigger(screen, trigger: SpawnTrigger, camera=None):
    render_sprite_entity(screen, trigger, Sprites.SPAWN_TRIGGER, camera)

def render_toggle_trigger(screen, trigger: ToggleTrigger, camera=None):
    render_sprite_entity(screen, trigger, Sprites.TOGGLE_TRIGGER, camera)

def render_rotation_trigger(screen, trigger: RotationTrigger, camera=None):
    render_sprite_entity(screen, trigger, Sprites.ROTATION_TRIGGER, camera)

def render_spike(screen, spike: Spike, camera=None):
    if spike.opacity <= 0:
        return

    pos = get_entity_screen_pos(spike, camera)

    key = (spike.width, spike.height, spike.color_fill, spike.color_border)
    if not hasattr(render_spike, "_cache"):
        render_spike._cache = {}

    surface = render_spike._cache.get(key)
    if surface is None:
        surface = pygame.Surface(
            (spike.width, spike.height), pygame.SRCALPHA
        ).convert_alpha()
        points = [
            (spike.width // 2, 0),
            (0, spike.height),
            (spike.width, spike.height),
        ]
        pygame.draw.polygon(surface, spike.color_fill, points)
        pygame.draw.polygon(surface, spike.color_border, points, width=3)
        render_spike._cache[key] = surface

    surface = get_transformed(
        surface,
        width=spike.width,
        height=spike.height,
        angle=spike.rotation,
        opacity=spike.opacity,
    )

    blit_centered(screen, surface, pos, spike.width, spike.height)

# ===============================
# 🗂 ENTITY → RENDERER MAP
# ===============================

ENTITY_RENDERERS = {
    Player: render_player,
    Platform: render_platform,
    JumpPad: render_jump_pad,
    GravityPortal: render_gravity_portal,
    UpsideDownPortal: render_upside_down_portal,
    NormalGravityPortal: render_normal_gravity_portal,
    UFOPortal: render_ufoportal,
    Spike: render_spike,
    Checkpoint: render_checkpoint,
    JumpOrb: render_jump_orb,
    GravityOrb: render_gravity_orb,
    EndDoor: render_end_door,
    ColorTrigger: render_color_trigger,
    OpacityTrigger: render_opacity_trigger,
    MoveTrigger: render_move_trigger,
    SpawnTrigger: render_spawn_trigger,
    ToggleTrigger: render_toggle_trigger,
    RotationTrigger: render_rotation_trigger,
    Text: render_text
}

def render_entity(screen, entity: Entity, camera: Camera | None = None):
    if entity.opacity <= 0:
        return

    renderer = ENTITY_RENDERERS.get(type(entity))
    if renderer:
        renderer(screen, entity, camera)
