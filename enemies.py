import pygame
class EnemyBullet:
    def __init__(self, direction, x, y):
        self.speed = 5
        self.direction = direction
        self.x = x
        self.y = y
        self.sprites = [
            pygame.image.load('materials/images/enemies/bullet/enemy_bullet_right.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/bullet/enemy_bullet_left.png').convert_alpha()
        ]
        self.hitbox = None
        self.get_hitbox()

    def get_hitbox(self):
        top_left = (self.x + (1 - self.direction) * 7, self.y)
        self.hitbox = pygame.Rect(top_left, (8, 8))

class LowTurret:
    def __init__(self, x, y, hp):
        self.sprites = [
            pygame.image.load('materials/images/enemies/turrets/low_turret_right.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/turrets/low_turret_left.png').convert_alpha()
        ]
        self.direction = 0
        self.type = 0
        self.x = x
        self.y = y
        self.reload_time = 1600
        self.timer = None
        self.health = hp
        self.hitbox = pygame.Rect((self.x, self.y), (48, 16))

    def shot(self, array):
        bullet = EnemyBullet(direction=self.direction, x=self.x + (1 - self.direction) * 50, y=self.y + 1)
        array.append(bullet)

    def get_hitbox(self):
        self.hitbox = pygame.Rect((self.x, self.y), (48, 16))

class HighTurret:
    def __init__(self, x, y, hp):
        self.sprites = [
            pygame.image.load('materials/images/enemies/turrets/high_turret_right.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/turrets/high_turret_left.png').convert_alpha()
        ]
        self.direction = 0
        self.type = 1
        self.x = x
        self.y = y
        self.reload_time = 1600
        self.timer = None
        self.health = hp
        self.hitbox = pygame.Rect((self.x, self.y), (48, 32))

    def shot(self, array):
        bullet = EnemyBullet(direction=self.direction, x=self.x + (1 - self.direction) * 50, y=self.y + 1)
        array.append(bullet)

    def get_hitbox(self):
        self.hitbox = pygame.Rect((self.x, self.y), (48, 32))

class CircleTurret:
    def __init__(self, x, y, hp):
        self.sprites = [
            pygame.image.load('materials/images/enemies/turrets/circle_turret.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/turrets/circle_turret.png').convert_alpha()
        ]
        self.direction = 0
        self.type = 2
        self.x = x
        self.y = y
        self.reload_time = 1600
        self.timer = None
        self.health = hp
        self.hitbox = pygame.Rect((self.x, self.y), (32, 16))

    def shot(self, array):
        bullet = EnemyBullet(direction=1, x=self.x, y=self.y + 2)
        array.append(bullet)
        bullet = EnemyBullet(direction=0, x=self.x + 33, y=self.y + 2)
        array.append(bullet)

    def get_hitbox(self):
        self.hitbox = pygame.Rect((self.x, self.y), (32, 16))