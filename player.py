import pygame


class Player:
    def __init__(self, x, y):
        self.anim_count = 0
        self.speed = 4
        self.direction = 0
        self.ammo = 6
        self.health = 5
        self.x = x
        self.y = y
        self.is_jump = False
        self.shot_lock = True
        self.jump_height = 0
        self.sprites = [
            pygame.image.load('materials/images/character/combine/player_combine_right.png').convert_alpha(),
            pygame.image.load('materials/images/character/combine/player_combine_left.png').convert_alpha()
        ]
        self.bullet_icon = pygame.image.load('materials/images/character/bullet/bullet_icon.png').convert_alpha()
        self.reload_icon = pygame.image.load('materials/images/reload_message.png').convert_alpha()
        self.hitbox = self.sprites[self.direction].get_rect(topleft=(self.x, self.y))
        self.reload_timer = pygame.USEREVENT + 1

    def move_right(self, edge):
        self.x = min(self.x + self.speed, edge)

    def move_left(self, edge):
        self.x = max(self.x - self.speed, edge)

    def jump(self, gravity, ground_level):  # заметить граунд-левел на пересечение колайдеров
        if not self.is_jump:
            self.jump_height = 7
            self.is_jump = True
        else:
            self.y = min(self.y - (self.jump_height**3)//6, ground_level)
            self.jump_height -= gravity
            if self.y == ground_level:
                self.is_jump = False
                self.jump_height = 0

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

    def show_ammo(self, surf):
        w, h = self.bullet_icon.get_size()
        for i in range(self.ammo):
            surf.blit(self.bullet_icon, (self.x + 2 + i * (w + 1), self.y - h - 2))

    def show_reload(self, surf):
        surf.blit(self.reload_icon, (980, 150))

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
