from level import Deserializator, Serializator
import json

class Levels:
    @staticmethod
    def load_level_from_file(file_path):
        with open(file_path, "r") as file:
            return Deserializator.load_level(json.load(file))

    @classmethod
    def init(cls):
        cls.FIRST_LEVEL = cls.load_level_from_file("assets/levels/first_level.json")
        cls.JUMP_PADS = cls.load_level_from_file("assets/levels/jump_pads.json")
        cls.MUNCI_STEP = cls.load_level_from_file("assets/levels/munci.json")
        cls.BALL = cls.load_level_from_file("assets/levels/ball.json")
        cls.ALL_LEVELS = [cls.FIRST_LEVEL, cls.JUMP_PADS, cls.MUNCI_STEP, cls.BALL]
