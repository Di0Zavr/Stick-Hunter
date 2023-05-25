import pygame

class GameSolidObject:
    def __init__(self, x, y, path):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(path)
        self.hitbox = pygame.Rect((self.x, self.y), self.sprite.get_size())

class Level:
    def __init__(self, name):
        self.name = name
        self.game_objects_on_screen = []

class Editor:
    def __init__(self):
        pass