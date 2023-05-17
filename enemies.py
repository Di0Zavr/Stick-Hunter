import pygame
import random

class EnemyBullet:
    def __init__(self, direction, x, y, angle=0):
        self.speed = 5
        self.direction = direction
        self.angle = angle
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
        self.shot_timer = pygame.USEREVENT + 1
        self.direction = 0
        self.x = x
        self.y = y
        self.reload = random.randint(1000, 4000)
        pygame.time.set_timer(self.shot_timer, self.reload)

    def check_reload_and_shot(self, array):
        for enemy_event in pygame.event.get():
            if enemy_event.type == self.reload:
                bullet = EnemyBullet(direction=self.direction, x=self.x + (1 - self.direction) * 50, y=self.y - 1)
                array.append(bullet)

class HighTurret:
    def __init__(self, x, y):
        self.sprites = [
            pygame.image.load('materials/images/enemies/turrets/high_turret_right.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/turrets/high_turret_left.png').convert_alpha()
        ]
        self.shot_timer = pygame.USEREVENT + 1
        self.direction = 0
        self.x = x
        self.y = y
        self.reload = random.randint(1000, 4000)
        pygame.time.set_timer(self.shot_timer, self.reload)

    def check_reload_and_shot(self, array):
        for enemy_event in pygame.event.get():
            if enemy_event.type == self.shot_timer:
                bullet = EnemyBullet(direction=self.direction, x=self.x + (1 - self.direction) * 50, y=self.y - 1)
                array.append(bullet)

class CircleTurret:
    def __init__(self, x, y):
        self.sprites = [
            pygame.image.load('materials/images/enemies/turrets/circle_turret.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/turrets/circle_turret.png').convert_alpha()
        ]
        self.shot_timer = pygame.USEREVENT + 1
        self.direction = 0
        self.x = x
        self.y = y
        self.reload = random.randint(2000, 5000)
        pygame.time.set_timer(self.shot_timer, self.reload)

    def check_reload_and_shot(self, array):
        for enemy_event in pygame.event.get():
            if enemy_event.type == self.reload:
                bullets = [
                    EnemyBullet(direction=0, x=self.x + 33, y=self.y + 3, angle=0),
                    EnemyBullet(direction=0, x=self.x + 24, y=self.y - 8, angle=45),
                    EnemyBullet(direction=0, x=self.x + 16, y=self.y - 9, angle=90),
                    EnemyBullet(direction=0, x=self.x + 3, y=self.y - 8, angle=135),
                    EnemyBullet(direction=0, x=self.x - 8, y=self.y + 3, angle=180)
                    ]
                array.extend(bullets)
