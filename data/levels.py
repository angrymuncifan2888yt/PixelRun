from level import Deserializator, Serializator
import json
from util import resource_path

class Levels:
    @staticmethod
    def load_level_from_file(file_path):
        with open(file_path, "r") as file:
            return Deserializator.load_level(json.load(file))

    @classmethod
    def init(cls):
        cls.TUTORIAL = cls.load_level_from_file(resource_path("assets/levels/tutorial.json"))
        cls.FIRST_LEVEL = cls.load_level_from_file(resource_path("assets/levels/first_level.json"))
        cls.BALL = cls.load_level_from_file(resource_path("assets/levels/ball.json"))
        cls.UFO = cls.load_level_from_file(resource_path("assets/levels/ufo.json"))
        cls.EASY_CHALLENGE = cls.load_level_from_file(resource_path("assets/levels/easy_challenge.json"))
        cls.ALL_LEVELS = [cls.TUTORIAL, cls.FIRST_LEVEL, cls.BALL, cls.UFO, cls.EASY_CHALLENGE]
