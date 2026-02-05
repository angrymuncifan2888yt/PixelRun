import pygame

class Sounds:
    @classmethod
    def init(cls):
        cls.VOLUME = 1.0
        cls.BUTTON_PRESS = pygame.mixer.Sound("assets/sounds/button.mp3")
        cls.BUTTON_PRESS.set_volume(cls.VOLUME)

        cls.PLAYER_WALK = pygame.mixer.Sound("assets/sounds/walk.mp3")
        cls.PLAYER_WALK.set_volume(cls.VOLUME)

        cls.PLAYER_DEATH = pygame.mixer.Sound("assets/sounds/death.mp3")
        cls.PLAYER_DEATH.set_volume(cls.VOLUME)

    @classmethod
    def button_press(cls):
        cls.BUTTON_PRESS.set_volume(cls.VOLUME)
        cls.BUTTON_PRESS.play()

    @classmethod
    def player_walk(cls):
        cls.PLAYER_WALK.set_volume(cls.VOLUME)
        cls.PLAYER_WALK.play()

    @classmethod
    def player_death(cls):
        cls.PLAYER_DEATH.set_volume(cls.VOLUME)
        cls.PLAYER_DEATH.play()

    @classmethod
    def set_volume(cls, volume: float):
        cls.VOLUME = volume
        # обновляем громкость всех звуков класса
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, pygame.mixer.Sound):
                attr.set_volume(cls.VOLUME)
