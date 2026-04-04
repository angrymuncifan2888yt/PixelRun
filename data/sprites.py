import pygame
from .const import *

class Sprites:
    @classmethod
    def init(cls):
        # Player
        cls.UFO = pygame.image.load("assets/images/ufo.png")

        # Skins
        cls.DEFAULT = pygame.image.load("assets/images/skins/default.png")
        cls.MINI = pygame.image.load("assets/images/skins/mini.png")
        cls.ELECTRODYNAMIX = pygame.image.load("assets/images/skins/nexus.png")
        cls.DOGGIE = pygame.image.load("assets/images/skins/doggie.png")
        cls.MICHIGUN = pygame.image.load("assets/images/skins/michigun.png")
        cls.RUBRUB = pygame.image.load("assets/images/skins/rubrub.png")

        # World objects
        cls.GRAVITY_PORTAL = pygame.transform.scale(pygame.image.load("assets/images/gravity_portal.png"), PORTAL_SIZE)
        cls.UPSIDE_DOWN_PORTAL = pygame.transform.scale(pygame.image.load("assets/images/upside_down_portal.png"), PORTAL_SIZE)
        cls.NORMAL_GRAVITY_PORTAL = pygame.transform.scale(pygame.image.load("assets/images/normal_gravity_portal.png"), PORTAL_SIZE)
        cls.UFO_PORTAL = pygame.transform.scale(pygame.image.load("assets/images/ufo_portal.png"), PORTAL_SIZE)
        cls.CUBE_PORTAL = pygame.transform.scale(pygame.image.load("assets/images/cube_portal.png"), PORTAL_SIZE)
        cls.SPIKE = pygame.transform.scale(pygame.image.load("assets/images/spike.png"), SPIKE_SIZE)
        cls.CHECKPOINT = pygame.transform.scale(pygame.image.load("assets/images/checkpoint.png"), CHECKPOINT_SIZE)
        cls.JUMP_ORB = pygame.transform.scale(pygame.image.load("assets/images/jump_orb.png"), ORB_SIZE)
        cls.GRAVITY_ORB = pygame.transform.scale(pygame.image.load("assets/images/gravity_orb.png"), ORB_SIZE)
        cls.END_DOOR = pygame.transform.scale(pygame.image.load("assets/images/end_door.png"), END_DOOR_SIZE)

        # Triggers
        cls.COLOR_TRIGGER = pygame.transform.scale(pygame.image.load("assets/images/triggers/color_trigger.png"), TRIGGER_SIZE).convert_alpha()
        cls.OPACITY_TRIGGER = pygame.transform.scale(pygame.image.load("assets/images/triggers/opacity_trigger.png"), TRIGGER_SIZE).convert_alpha()
        cls.MOVE_TRIGGER = pygame.transform.scale(pygame.image.load("assets/images/triggers/move_trigger.png"), TRIGGER_SIZE).convert_alpha()
        cls.TOGGLE_TRIGGER = pygame.transform.scale(pygame.image.load("assets/images/triggers/toggle_trigger.png"), TRIGGER_SIZE).convert_alpha()
        cls.ROTATION_TRIGGER = pygame.transform.scale(pygame.image.load("assets/images/triggers/rotation_trigger.png"), TRIGGER_SIZE).convert_alpha()
        cls.SPAWN_TRIGGER = pygame.transform.scale(pygame.image.load("assets/images/triggers/spawn_trigger.png"), TRIGGER_SIZE).convert_alpha()

        # Other
        cls.YOUTUBE_ICON = pygame.image.load("assets/images/youtube.png")