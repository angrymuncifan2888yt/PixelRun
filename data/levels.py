from level import Deserializator, Serializator
from core import *
import json

with open("assets/levels/level1.json", "r") as file:
    data = json.load(file)
    Level1 = Deserializator.load_level(data)
