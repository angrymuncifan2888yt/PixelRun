from level import Deserializator, Serializator
import json

class Levels:
    @staticmethod
    def load_level_from_file(file_path):
        with open(file_path, "r") as file:
            return Deserializator.load_level(json.load(file))

    @classmethod
    def init(cls):
        cls.TUTORIAL = cls.load_level_from_file("assets/levels/tutorial.json")
        cls.FIRST_LEVEL = cls.load_level_from_file("assets/levels/first_level.json")
        cls.BALL = cls.load_level_from_file("assets/levels/ball.json")
        cls.EXECUTION = cls.load_level_from_file("assets/levels/execution.json")
        cls.UFO = cls.load_level_from_file("assets/levels/ufo.json")
        cls.ALL_LEVELS = [cls.TUTORIAL, cls.FIRST_LEVEL, cls.BALL, cls.EXECUTION, cls.UFO]
