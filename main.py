import pygame
import enemies
from player import Player
player_sizes = (34, 33)
bullet_sizes = (18, 7)
turret_sizes = [
    (50, 24),
    (50, 33),
    (40, 17)
]
enemy_bullet_sizes = (15, 8)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 760))

        self.gravity = 1
        self.icon = pygame.image.load('materials/images/simp_moment_right.png').convert_alpha()
        self.bg = pygame.image.load('materials/images/background.png').convert_alpha()
        self.cursor_icon = pygame.image.load('materials/images/cursor.png').convert_alpha()

        self.bullets_on_screen = []
        self.enemy_bullets_on_screen = []
        self.enemies_on_screen = []

        pygame.display.set_caption('Crystal Hunter')
        pygame.display.set_icon(self.icon)
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(40, 680)

    def main_rander(self, mouse_pos):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.cursor_icon, mouse_pos)
        self.screen.blit(self.player.sprites[self.player.direction], (self.player.x, self.player.y))
        self.player.show_ammo(self.screen)

    def check_bullets(self):
        for bl in self.bullets_on_screen:
            if not -20 <= bl.x <= 1300:
                self.bullets_on_screen.remove(bl)
                continue
            self.screen.blit(bl.sprites[bl.direction], (bl.x, bl.y))
            bl.x += (1 - 2 * bl.direction) * bl.speed

    def check_inputs(self):
        keys = pygame.key.get_pressed()
        mouse_click = pygame.mouse.get_pressed()

        if not self.player.ammo:
            self.player.reload(surf=self.screen)

        if mouse_click[0]:
            self.player.single_shot(array=self.bullets_on_screen)
        else:
            self.player.unlock_gun()

        if keys[pygame.K_d]:
            self.player.move_right(edge=1247)
        if keys[pygame.K_a]:
            self.player.move_left(edge=1)
        if keys[pygame.K_SPACE] or self.player.is_jump:
            self.player.jump(self.gravity)

    def gameplay(self):
        while self.running:
            pygame.display.update()

            # get positions and triggers
            mx, my = pygame.mouse.get_pos()

            self.main_rander((mx, my))
            self.player.direction = 0 if self.player.x <= mx else 1
            self.check_bullets()
            self.check_inputs()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        exit()


if __name__ == '__main__':
    game = Game()
    game.gameplay()
