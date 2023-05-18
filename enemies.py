import pygame
import random

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

class LowTurret:
    def __init__(self, x, y):
        self.sprites = [
            pygame.image.load('materials/images/enemies/turrets/low_turret_right.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/turrets/low_turret_left.png').convert_alpha()
        ]
        self.direction = 0
        self.x = x
        self.y = y
        self.shot_timer = pygame.USEREVENT + 1
        self.reload_lock = True

    def shot(self, array):
        bullet = EnemyBullet(direction=self.direction, x=self.x + (1 - self.direction) * 50, y=self.y - 1)
        array.append(bullet)

