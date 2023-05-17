import pygame
import numpy
from enemies import LowTurret, HighTurret, CircleTurret
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

        self.scene = 'menu'
        self.gravity = 1
        self.ground = 680
        self.menu_mouse_lock = True
        self.pause_mouse_lock = True
        self.icon = pygame.image.load('materials/images/simp_moment_right.png').convert_alpha()
        self.bg = pygame.image.load('materials/images/background.png').convert_alpha()
        self.cursor_icon = pygame.image.load('materials/images/cursor.png').convert_alpha()

        self.bullets_on_screen = []
        self.enemy_bullets_on_screen = []
        self.enemies_on_screen = []

        self.menu_font = pygame.font.Font('materials/fonts/RussoOne-Regular.ttf', 40)

        pygame.display.set_caption('Crystal Hunter')
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(40, 680)

    def main_menu(self):
        pygame.display.update()
        pygame.mouse.set_visible(True)

        self.screen.fill('gray')
        play_sign = self.menu_font.render('ИГРАТЬ', False, 'white')
        exit_from_game_sign = self.menu_font.render('ВЫЙТИ ИЗ ИГРЫ', False, 'white')
        sx, sy = self.screen.get_size()
        play_x, play_y = play_sign.get_size()
        exit_x, exit_y = exit_from_game_sign.get_size()
        play_pos = (sx/2 - play_x/2, sy/4)
        exit_pos = (sx/2 - exit_x/2, sy/4 + play_y + 30)
        self.screen.blit(play_sign, play_pos)
        self.screen.blit(exit_from_game_sign, exit_pos)

        mouse = pygame.mouse.get_pressed()
        play_box = play_sign.get_rect(topleft=play_pos)
        exit_box = exit_from_game_sign.get_rect(topleft=exit_pos)
        mouse_box = pygame.Rect(pygame.mouse.get_pos(), (4, 4))

        if mouse[0] and not self.menu_mouse_lock:
            self.menu_mouse_lock = True
            if play_box.colliderect(mouse_box):
                self.scene = 'gameplay'
                self.menu_mouse_lock = True
            elif exit_box.colliderect(mouse_box):
                self.running = False
                pygame.quit()
                exit()
        elif not mouse[0] and self.menu_mouse_lock:
            self.menu_mouse_lock = False

        pygame.event.get()

    def pause(self):
        pygame.display.update()
        pygame.event.get()
        pygame.mouse.set_visible(True)

        self.screen.fill('gray')
        continue_sign = self.menu_font.render('ПРОДОЛЖИТЬ', False, 'white')
        exit_to_menu = self.menu_font.render('ВЫЙТИ В МЕНЮ', False, 'white')
        sx, sy = self.screen.get_size()
        cont_x, cont_y = continue_sign.get_size()
        exit_x, exit_y = exit_to_menu.get_size()
        cont_pos = (sx / 2 - cont_x / 2, sy / 4)
        exit_pos = (sx / 2 - exit_x / 2, sy / 4 + cont_y + 30)
        self.screen.blit(continue_sign, cont_pos)
        self.screen.blit(exit_to_menu, exit_pos)

        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        cont_box = continue_sign.get_rect(topleft=cont_pos)
        exit_box = exit_to_menu.get_rect(topleft=exit_pos)
        mouse_box = pygame.Rect(pygame.mouse.get_pos(), (4, 4))

        if mouse[0] and not self.pause_mouse_lock:
            self.pause_mouse_lock = True
            if cont_box.colliderect(mouse_box):
                self.scene = 'gameplay'
                self.pause_mouse_lock = True
            elif exit_box.colliderect(mouse_box):
                self.scene = 'menu'
        elif not mouse[0] and self.pause_mouse_lock:
            self.pause_mouse_lock = False

    def main_render(self, mouse_pos):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.cursor_icon, mouse_pos)
        self.screen.blit(self.player.sprites[self.player.direction], (self.player.x, self.player.y))
        self.player.show_ammo(self.screen)

    def check_player_bullets(self):
        for bl in self.bullets_on_screen:
            if not -20 <= bl.x <= 1300:
                self.bullets_on_screen.remove(bl)
                continue
            self.screen.blit(bl.sprites[bl.direction], (bl.x, bl.y))
            bl.x += (1 - 2 * bl.direction) * bl.speed

    def check_inputs_gameplay(self):
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
            self.player.jump(self.gravity, self.ground)

        if keys[pygame.K_i]:
            self.place_enemy(0)
        if keys[pygame.K_o]:
            self.place_enemy(1)
        if keys[pygame.K_p]:
            self.place_enemy(2)

        if keys[pygame.K_ESCAPE]:
            self.player.shot_lock = True
            self.scene = 'pause'

    def check_enemies(self):
        for enemy in self.enemies_on_screen:
            self.screen.blit(enemy.sprites[enemy.direction], (enemy.x, enemy.y))
            enemy.direction = 0 if enemy.x <= self.player.x else 1
            enemy.check_reload_and_shot(self.enemy_bullets_on_screen)

    def check_enemy_bullets(self):
        for enbl in self.enemy_bullets_on_screen:
            if not -20 <= enbl.x <= 1300 or not -20 <= enbl.y <= 780:
                self.enemy_bullets_on_screen.remove(enbl)
                continue
            self.screen.blit(enbl.sprites[enbl.direction], (enbl.x, enbl.y))
            enbl.x += (1 - 2 * enbl.direction) * enbl.speed * numpy.cos(enbl.angle * numpy.pi / 180)
            enbl.y += (1 - 2 * enbl.direction) * enbl.speed * numpy.sin(enbl.angle * numpy.pi / 180)

    def place_enemy(self, var):
        mx, my = pygame.mouse.get_pos()
        if var == 0:
            self.enemies_on_screen.append(LowTurret(x=mx, y=my))
        elif var == 1:
            self.enemies_on_screen.append(HighTurret(x=mx, y=my))
        else:
            self.enemies_on_screen.append(CircleTurret(x=mx, y=my))

    def gameplay(self):
        pygame.display.update()
        pygame.mouse.set_visible(False)

        # get positions and triggers
        mx, my = pygame.mouse.get_pos()

        self.main_render((mx, my))
        self.player.direction = 0 if self.player.x <= mx else 1
        self.check_player_bullets()
        self.check_inputs_gameplay()
        self.check_enemies()
        self.check_enemy_bullets()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()

        pygame.display.flip()
        self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    while game.running:
        match game.scene:
            case 'menu':
                game.main_menu()
            case 'gameplay':
                game.gameplay()
            case 'pause':
                game.pause()
