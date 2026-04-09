import pygame
from .const import *
from util.resourse_path import resource_path

class Sprites:
    @classmethod
    def init(cls):
        # Skins
        cls.CUBE_DEFAULT = pygame.image.load(resource_path("assets/images/skins/cube/cube_default.png"))
        cls.CUBE_MINI = pygame.image.load(resource_path("assets/images/skins/cube/cube_mini.png"))
        cls.CUBE_ELECTRODYNAMIX = pygame.image.load(resource_path("assets/images/skins/cube/cube_nexus.png"))
        cls.CUBE_DOGGIE = pygame.image.load(resource_path("assets/images/skins/cube/cube_doggie.png"))
        cls.CUBE_MICHIGUN = pygame.image.load(resource_path("assets/images/skins/cube/cube_michigun.png"))
        cls.CUBE_RUBRUB = pygame.image.load(resource_path("assets/images/skins/cube/cube_rubrub.png"))

        cls.UFO_DEFAULT = pygame.image.load(resource_path("assets/images/skins/ufo/ufo_default.png"))
        cls.UFO_CLUBSTEP = pygame.image.load(resource_path("assets/images/skins/ufo/ufo_clubstep.png"))
        cls.UFO_CLOUD = pygame.image.load(resource_path("assets/images/skins/ufo/ufo_cloud.png"))
        cls.UFO_KING = pygame.image.load(resource_path("assets/images/skins/ufo/ufo_king.png"))
        cls.UFO_TETRIS = pygame.image.load(resource_path("assets/images/skins/ufo/ufo_tetris.png"))

        cls.BALL_DEFAULT = pygame.image.load(resource_path("assets/images/skins/ball/ball_default.png"))
        cls.BALL_BALL = pygame.image.load(resource_path("assets/images/skins/ball/ball_ball.png"))
        cls.BALL_SONIC = pygame.image.load(resource_path("assets/images/skins/ball/ball_sonic.png"))
        cls.BALL_SMILE = pygame.image.load(resource_path("assets/images/skins/ball/ball_smile.png"))

        # World objects
        cls.GRAVITY_PORTAL = pygame.transform.scale(pygame.image.load(resource_path("assets/images/gravity_portal.png")), PORTAL_SIZE)
        cls.UPSIDE_DOWN_PORTAL = pygame.transform.scale(pygame.image.load(resource_path("assets/images/upside_down_portal.png")), PORTAL_SIZE)
        cls.NORMAL_GRAVITY_PORTAL = pygame.transform.scale(pygame.image.load(resource_path("assets/images/normal_gravity_portal.png")), PORTAL_SIZE)
        cls.UFO_PORTAL = pygame.transform.scale(pygame.image.load(resource_path("assets/images/ufo_portal.png")), PORTAL_SIZE)
        cls.CUBE_PORTAL = pygame.transform.scale(pygame.image.load(resource_path("assets/images/cube_portal.png")), PORTAL_SIZE)
        cls.BALL_PORTAL = pygame.transform.scale(pygame.image.load(resource_path("assets/images/ball_portal.png")), PORTAL_SIZE)
        cls.SPIKE = pygame.transform.scale(pygame.image.load(resource_path("assets/images/spike.png")), SPIKE_SIZE)
        cls.CHECKPOINT = pygame.transform.scale(pygame.image.load(resource_path("assets/images/checkpoint.png")), CHECKPOINT_SIZE)
        cls.JUMP_ORB = pygame.transform.scale(pygame.image.load(resource_path("assets/images/jump_orb.png")), ORB_SIZE)
        cls.GRAVITY_ORB = pygame.transform.scale(pygame.image.load(resource_path("assets/images/gravity_orb.png")), ORB_SIZE)
        cls.END_DOOR = pygame.transform.scale(pygame.image.load(resource_path("assets/images/end_door.png")), END_DOOR_SIZE)

        # Triggers
        cls.COLOR_TRIGGER = pygame.transform.scale(pygame.image.load(resource_path("assets/images/triggers/color_trigger.png")), TRIGGER_SIZE).convert_alpha()
        cls.OPACITY_TRIGGER = pygame.transform.scale(pygame.image.load(resource_path("assets/images/triggers/opacity_trigger.png")), TRIGGER_SIZE).convert_alpha()
        cls.MOVE_TRIGGER = pygame.transform.scale(pygame.image.load(resource_path("assets/images/triggers/move_trigger.png")), TRIGGER_SIZE).convert_alpha()
        cls.TOGGLE_TRIGGER = pygame.transform.scale(pygame.image.load(resource_path("assets/images/triggers/toggle_trigger.png")), TRIGGER_SIZE).convert_alpha()
        cls.ROTATION_TRIGGER = pygame.transform.scale(pygame.image.load(resource_path("assets/images/triggers/rotation_trigger.png")), TRIGGER_SIZE).convert_alpha()
        cls.SPAWN_TRIGGER = pygame.transform.scale(pygame.image.load(resource_path("assets/images/triggers/spawn_trigger.png")), TRIGGER_SIZE).convert_alpha()

        # Other
        cls.PIXELRUN_ICON = pygame.image.load(resource_path("assets/images/icon.png"))
        cls.YOUTUBE_ICON = pygame.image.load(resource_path("assets/images/youtube.png"))