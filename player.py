import pygame


class Player:
    def __init__(self, x, y):
        self.anim_count = 0
        self.speed = 4
        self.direction = 0
        self.ammo = 6
        self.health = 10
        self.x = x
        self.y = y
        self.in_air = True
        self.shot_lock = True
        self.invincible = False
        self.jump_height = 0
        self.sprites = [
            pygame.image.load('materials/images/character/combine/player_combine_right.png').convert_alpha(),
            pygame.image.load('materials/images/character/combine/player_combine_left.png').convert_alpha()
        ]
        self.bullet_icon = pygame.image.load('materials/images/character/bullet/bullet_icon.png').convert_alpha()
        self.get_hitboxes()
        self.reload_timer = pygame.USEREVENT + 1
        self.inframes_timer = pygame.USEREVENT + 2

    def move_right(self, edge):
        self.x = min(self.x + self.speed, edge)
        self.get_hitboxes()

    def move_left(self, edge):
        self.x = max(self.x - self.speed, edge)
        self.get_hitboxes()

    def single_shot(self, array):
        if not self.shot_lock and self.ammo:
            self.shot_lock = True
            self.ammo -= 1
            bullet = Bullet(direction=self.direction, x=self.x + (1 - self.direction) * 33, y=self.y + 13)
            array.append(bullet)
            if not self.ammo:
                pygame.time.set_timer(self.reload_timer, 1000, 1)

    def unlock_gun(self):
        self.shot_lock = False

    def reload(self):
        self.ammo = 6

    def take_damage(self):
        self.health -= 1
        self.invincible = True
        pygame.time.set_timer(self.inframes_timer, 1500, 1)

    def show_ammo(self, surf):
        w, h = self.bullet_icon.get_size()
        for i in range(self.ammo):
            surf.blit(self.bullet_icon, (self.x - self.direction * 15 + 2 + i * (w + 1), self.y - h - 2))

    def get_hitboxes(self):
        self.hitbox = pygame.Rect((self.x, self.y), (16, 33))
        self.head_hitbox = pygame.Rect((self.x, self.y), (16, 1))
        self.leg_hitbox = pygame.Rect((self.x - 2, self.y + 33), (20, 1))


class Bullet:
    def __init__(self, direction, x, y):
        self.speed = 12
        self.direction = direction
        self.x = x
        self.y = y
        self.sprites = [
            pygame.image.load('materials/images/character/bullet/bullet_right.png').convert_alpha(),
            pygame.image.load('materials/images/character/bullet/bullet_left.png').convert_alpha()
        ]
        self.hitbox = None
        self.get_hitbox()

    def get_hitbox(self):
        top_left = (self.x + (1 - self.direction) * 11, self.y)
        self.hitbox = pygame.Rect(top_left, (7, 7))

class Goblet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load('materials/images/character/goblet.png')
        self.hitbox = pygame.Rect((x, y), (22, 20))
