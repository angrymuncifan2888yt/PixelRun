from level import Deserializator, Serializator
import json

class Levels:
    @staticmethod
    def load_level_from_file(file_path):
        with open(file_path, "r") as file:
            return Deserializator.load_level(json.load(file))

    @classmethod
    def init(cls):
        cls.Level1 = cls.load_level_from_file("assets/levels/level1.json")
        # cls.Level2 = cls.load_level_from_file("assets/levels/level2.json")

        # List of all levels
        cls.ALL_LEVELS = [cls.Level1]
