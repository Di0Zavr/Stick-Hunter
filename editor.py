import pygame


class GameSolidObject:
    def __init__(self, x, y, path, t=0):
        self.x = x
        self.y = y
        self.type = t
        self.sprite = pygame.image.load(path).convert_alpha()
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

    def convert_object(self, g_obj, obj_type):
        match obj_type:
            case 1:
                hash = f'01-{g_obj.x}-{g_obj.y}-{g_obj.type}-{g_obj.health}'
            case 2:
                hash = f'02-{g_obj.x}-{g_obj.y}-{g_obj.type}'
            case 3:
                hash = f'03-{g_obj.x}-{g_obj.y}-{g_obj.direction}'
            case 4:
                hash = f'04-{g_obj.x}-{g_obj.y}-{g_obj.direction}'
            case 5:
                hash = f'05-{g_obj.x}-{g_obj.y}'
        return hash

    def save(self):
        with open(f'saves/{self.name}.txt') as f:
            f.write(f'00-{self.player_x}-{self.player_y}\n')
            for obj in self.enemies:
                h = self.convert_object(obj, 1)
                f.write(f'{h}\n')
            for obj in self.death_blocks:
                h = self.convert_object(obj, 2)
                f.write(f'{h}\n')
            for obj in self.solid_blocks:
                h = self.convert_object(obj, 2)
                f.write(f'{h}\n')
            for obj in self.player_bullets:
                h = self.convert_object(obj, 3)
                f.write(f'{h}\n')
            for obj in self.enemy_bullets:
                h = self.convert_object(obj, 4)
                f.write(f'{h}\n')
            for obj in self.goblets:
                h = self.convert_object(obj, 5)
                f.write(f'{h}\n')

class Editor:
    def __init__(self):
        pass