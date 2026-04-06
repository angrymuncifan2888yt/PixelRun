from .sprites import Sprites
from core import GameMode


class Skin:
    def __init__(self, name: str, description: str, sprite, gamemode, size=(75, 75)) -> None:
        self.name = name
        self.description = description
        self.sprite = sprite
        self.gamemode = gamemode
        self.size = size


class Skins:
    @classmethod
    def init(cls):
        cls.ALL_SKINS = []

        cls.CUBE_SKINS = []
        cls.UFO_SKINS = []
        cls.BALL_SKINS = []

        def add(skin):
            cls.ALL_SKINS.append(skin)

            if skin.gamemode == GameMode.CUBE:
                cls.CUBE_SKINS.append(skin)
            elif skin.gamemode == GameMode.UFO:
                cls.UFO_SKINS.append(skin)
            elif skin.gamemode == GameMode.BALL:
                cls.BALL_SKINS.append(skin)

        add(Skin("Default", "Default skin", Sprites.CUBE_DEFAULT, GameMode.CUBE))
        add(Skin("Mini", "Idk what to type here lol", Sprites.CUBE_MINI, GameMode.CUBE))
        add(Skin("Electrodynamix", "Complete Extreme Demon \"Electrodynamix\" to get this icon", Sprites.CUBE_ELECTRODYNAMIX, GameMode.CUBE))
        add(Skin("Doggie", "Doggie's icon", Sprites.CUBE_DOGGIE, GameMode.CUBE))
        add(Skin("Michigun", "Michigun's icon", Sprites.CUBE_MICHIGUN, GameMode.CUBE))
        add(Skin("Rubrub (Robtop)", "Creator of the original game (Geometry Dash)", Sprites.CUBE_RUBRUB, GameMode.CUBE))

        add(Skin("Default", "Default UFO skin", Sprites.UFO_DEFAULT, GameMode.UFO, size=(90, 75)))
        add(Skin("Clubstep", "You are lucky there is no Clubstep in PixelRun", Sprites.UFO_CLUBSTEP, GameMode.UFO, size=(90, 75)))
        add(Skin("Cloud", "Cloudy weather!", Sprites.UFO_CLOUD, GameMode.UFO, size=(75, 75)))
        add(Skin("Nexus", "Nexus's UFO", Sprites.UFO_KING, GameMode.UFO, size=(90, 75)))
        add(Skin("Tetris", "The real most popular game", Sprites.UFO_TETRIS, GameMode.UFO, size=(90, 75)))

        add(Skin("Default", "Default Ball skin", Sprites.BALL_DEFAULT, GameMode.BALL, size=(75, 75)))
        add(Skin("Ball", "Literally... a ball", Sprites.BALL_BALL, GameMode.BALL, size=(75, 75)))
        add(Skin("Sonic", "Sonic Ball", Sprites.BALL_SONIC, GameMode.BALL, size=(75, 75)))
        add(Skin("Smile", "Smile!", Sprites.BALL_SMILE, GameMode.BALL, size=(75, 75)))