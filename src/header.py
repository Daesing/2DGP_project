from entity import *
from src.knight import Knight
from src.world import World

WIDTH,HEIGHT = 1280,720
collections = SpriteCollection()
player = Knight(400, 200)
world = World(collections)

world.add_entity(player)