from .sprites import Sprites

class Skin:
    def __init__(self, name: str, description: str, standing_sprite, animations) -> None:
        self.standing_sprite = standing_sprite
        self.name = name
        self.description = description
        self.animations = animations

    @property
    def animation_length(self):
        return len(self.animations)


class Skins:
    @classmethod
    def init(cls):
        cls.DEFAULT = Skin("Default",
                               "Default skin",
                               Sprites.DEFAULT,
                               [Sprites.DEFAULT])
        cls.MINI = Skin("Mini",
                               "Idk what to type here lol",
                               Sprites.MINI,
                               [Sprites.MINI])
        cls.ELECTRODYNAMIX = Skin("Electrodynamix",
                               "Complete Extreme Demon \"Electrodynamix\" to get this icon",
                               Sprites.ELECTRODYNAMIX,
                               [Sprites.ELECTRODYNAMIX])
        cls.DOGGIE = Skin("Doggie",
                               "Doggie's icon",
                               Sprites.DOGGIE,
                               [Sprites.DOGGIE])
        cls.MICHIGUN = Skin("Michigun",
                               "Michigun's icon",
                               Sprites.MICHIGUN,
                               [Sprites.MICHIGUN])
        cls.RUBRUB = Skin("Rubrub (Robtop)",
                               "Creator of the original game (Geometry Dash)",
                               Sprites.RUBRUB,
                               [Sprites.RUBRUB])
        cls.ALL_SKINS = [cls.DEFAULT, cls.MINI, cls.ELECTRODYNAMIX, cls.DOGGIE, cls.MICHIGUN, cls.RUBRUB]