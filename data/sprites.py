import pygame
from .const import *

class Sprites:
    @classmethod
    def init(cls):
        # Angry Munci skin
        cls.ANGRY_MUNCI_STANDING = pygame.transform.scale(pygame.image.load("assets/images/angry_munci/angry_munci_standing.png"), PLAYER_SIZE)
        cls.ANGRY_MUNCI = [
            pygame.transform.scale(pygame.image.load("assets/images/angry_munci/angry_munci_running.png"), PLAYER_SIZE),
            pygame.transform.scale(pygame.image.load("assets/images/angry_munci/angry_munci_running2.png"), PLAYER_SIZE),
            pygame.transform.scale(pygame.image.load("assets/images/angry_munci/angry_munci_running3.png"), PLAYER_SIZE),
        ]
        # Cat Jard skin    
        cls.CAT_JARD_STANDING = pygame.transform.scale(pygame.image.load("assets/images/cat_jard/cat_jard_standing.png"), PLAYER_SIZE)
        cls.CAT_JARD = [
            pygame.transform.scale(pygame.image.load("assets/images/cat_jard/cat_jard_running.png"), PLAYER_SIZE),
            pygame.transform.scale(pygame.image.load("assets/images/cat_jard/cat_jard_running2.png"), PLAYER_SIZE),
            pygame.transform.scale(pygame.image.load("assets/images/cat_jard/cat_jard_running3.png"), PLAYER_SIZE),
            pygame.transform.scale(pygame.image.load("assets/images/cat_jard/cat_jard_running4.png"), PLAYER_SIZE),
            pygame.transform.scale(pygame.image.load("assets/images/cat_jard/cat_jard_running5.png"), PLAYER_SIZE),
        ]
        # Sliding garou skin
        cls.SLIDING_GAROU_STANDING = pygame.transform.flip(
            pygame.transform.scale(pygame.image.load("assets/images/sliding_garou.png"), PLAYER_SIZE),
            True, False)
        cls.SLIDING_GAROU = [
            cls.SLIDING_GAROU_STANDING,
        ]

        # World objects
        cls.GRAVITY_PORTAL = pygame.transform.scale(pygame.image.load("assets/images/gravity_portal.png"), PORTAL_SIZE)
        cls.UPSIDE_DOWN_PORTAL = pygame.transform.scale(pygame.image.load("assets/images/upside_down_portal.png"), PORTAL_SIZE)
        cls.NORMAL_GRAVITY_PORTAL = pygame.transform.scale(pygame.image.load("assets/images/normal_gravity_portal.png"), PORTAL_SIZE)
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

        # Other
