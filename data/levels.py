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
        cls.JUMP_PADS = cls.load_level_from_file("assets/levels/jump_pads.json")
        cls.MUNCI_STEP = cls.load_level_from_file("assets/levels/munci.json")
        cls.BALL = cls.load_level_from_file("assets/levels/ball.json")
        cls.TEXT_ANIMATION = cls.load_level_from_file("assets/levels/text_animation.json")
        cls.EXECUTION = cls.load_level_from_file("assets/levels/execution.json")
        cls.VERY_HARD_JUMP = cls.load_level_from_file("assets/levels/hard_jump.json")
        cls.ALL_LEVELS = [cls.TUTORIAL, cls.FIRST_LEVEL, cls.JUMP_PADS, cls.MUNCI_STEP, cls.BALL, cls.TEXT_ANIMATION, cls.EXECUTION, cls.VERY_HARD_JUMP]
