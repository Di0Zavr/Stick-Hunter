import pygame


class GameSolidObject:
    def __init__(self, x, y, path):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(path)
        self.hitbox = pygame.Rect((self.x, self.y), self.sprite.get_size())


class Level:
    def __init__(self, name, x, y):
        self.name = name
        self.player_x = x
        self.player_y = y
        self.enemies = []
        self.death_blocks = []
        self.solid_blocks = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.goblets = []


class Editor:
    def __init__(self):
        pass