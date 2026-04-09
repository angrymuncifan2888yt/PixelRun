import pygame
from util import resource_path

class SoundChannels:
    @classmethod
    def init(cls):
        cls.SYSTEM = pygame.mixer.Channel(0)
        cls.GAME = pygame.mixer.Channel(1)

class Sounds:
    @classmethod
    def init(cls):
        cls.VOLUME = 1.0
        cls.BUTTON_PRESS = pygame.mixer.Sound(resource_path("assets/sounds/button.mp3"))
        cls.BUTTON_PRESS.set_volume(cls.VOLUME)

        cls.PLAYER_WALK = pygame.mixer.Sound(resource_path("assets/sounds/walk.mp3"))
        cls.PLAYER_WALK.set_volume(cls.VOLUME)

        cls.PLAYER_DEATH = pygame.mixer.Sound(resource_path("assets/sounds/death.mp3"))
        cls.PLAYER_DEATH.set_volume(cls.VOLUME)

        cls.PLAYER_JUMP = pygame.mixer.Sound(resource_path("assets/sounds/click.mp3"))
        cls.PLAYER_JUMP.set_volume(cls.VOLUME * 3) # To make jump a bit louder

    @staticmethod
    def play_sound(sound: pygame.mixer.Sound, channel: pygame.mixer.Channel, volume: float | None = None):
        if volume is not None:
            sound.set_volume(volume)
        channel.play(sound)

    @classmethod
    def set_volume(cls, volume: float):
        cls.VOLUME = volume
        # обновляем громкость всех звуков класса
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, pygame.mixer.Sound):
                attr.set_volume(cls.VOLUME)
