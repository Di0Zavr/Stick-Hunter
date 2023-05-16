import pygame
import random

class EnemyBullet:
    def __init__(self, direction, x, y):
        self.speed = 7
        self.direction = direction
        self.x = x
        self.y = y
        self.sprites = [
            pygame.image.load('materials/images/enemies/bullet/enemy_bullet_right.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/bullet/enemy_bullet_left.png').convert_alpha()
        ]

class Turret:
    def __init__(self, pos, reload_time):
        self.sprites = [
            [
                pygame.image.load('materials/images/enemies/turrets/low_turret_right.png').convert_alpha(),
                pygame.image.load('materials/images/enemies/turrets/low_turret_left.png').convert_alpha()
            ],  # нижние турели
            [
                pygame.image.load('materials/images/enemies/turrets/high_turret_right.png').convert_alpha(),
                pygame.image.load('materials/images/enemies/turrets/high_turret_left.png').convert_alpha()
            ],  # высокие турели
            [
                pygame.image.load('materials/images/enemies/turrets/circle_turret.png').convert_alpha()
            ]
        ]
        self.shot_timer = pygame.USEREVENT + 1
        self.direction = 0
        self.pos = pos
        self.reload = reload_time
        pygame.time.set_timer(self.shot_timer, self.reload)

    def single_shot(self):
        gun_pos = (self.pos[0] + (1 - self.direction) * 50, self.pos[1] - 1)
