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
        cls.ANGRY_MUNCI = Skin("Angry Munci",
                               "Angry Munci on top",
                               Sprites.ANGRY_MUNCI_STANDING,
                               Sprites.ANGRY_MUNCI)
        cls.CAT_JARD = Skin("Cat Jard",
                        "He stays on your ass and he makes sure you die pretty much",
                               Sprites.CAT_JARD_STANDING,
                               Sprites.CAT_JARD)
        cls.SLIDING_GAROU = Skin("Sliding garou",
                                 "We waited for this for so long",
                                 Sprites.SLIDING_GAROU_STANDING, Sprites.SLIDING_GAROU)
        cls.ALL_SKINS = [cls.CAT_JARD, cls.ANGRY_MUNCI, cls.SLIDING_GAROU]