import pygame


class Fonts:
    @classmethod
    def init(cls):
        LOGO_FONT_PATH = "assets/fonts/logo_font.ttf"
        NORMAL_FONT_PATH = "assets/fonts/normal_font.ttf"
        cls.LOGO_100 = pygame.font.Font(LOGO_FONT_PATH, 100)
        cls.LOGO_70 = pygame.font.Font(LOGO_FONT_PATH, 70)
        cls.NORMAL_30 = pygame.font.Font(NORMAL_FONT_PATH, 30)
        cls.NORMAL_25 = pygame.font.Font(NORMAL_FONT_PATH, 25)
        cls.NORMAL_40 = pygame.font.Font(NORMAL_FONT_PATH, 40)