from level import Deserializator, Serializator
import json

class Levels:
    @classmethod
    def init(cls):
        with open("assets/levels/level1.json", "r") as file:
            data_level1 = json.load(file)

        with open("assets/levels/level2.json", "r") as file:
            data_level2 = json.load(file)

        cls.Level1 = Deserializator.load_level(data_level1)
        cls.Level2 = Deserializator.load_level(data_level2)

        # List of all levels
        cls.ALL_LEVELS = [cls.Level1, cls.Level2]