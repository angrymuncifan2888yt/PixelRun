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
        cls.SUPER_TRIGGER = cls.load_level_from_file("assets/levels/super_trigger.json")
        cls.ALL_LEVELS = [cls.FIRST_LEVEL, cls.SUPER_TRIGGER]
