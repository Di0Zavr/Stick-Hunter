import pygame
from enemies import LowTurret, HighTurret, CircleTurret
from player import Player, Goblet
from editor import GameSolidObject
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
        self.gravity = 0.26
        self.enemy_counter = 0
        self.ground = 680
        self.menu_screen_mouse_lock = True
        self.place_objects_lock = True

        self.icon = pygame.image.load('materials/images/simp_moment_right.png').convert_alpha()
        self.bg = pygame.image.load('materials/images/background.png').convert_alpha()
        self.cursor_icon = pygame.image.load('materials/images/cursor.png').convert_alpha()

        self.bullets_on_screen = []
        self.enemy_bullets_on_screen = []
        self.enemies_on_screen = []
        self.goblets_on_screen = []
        self.death_blocks_on_screen = []

        self.menu_font = pygame.font.Font('materials/fonts/RussoOne-Regular.ttf', 40)

        pygame.display.set_caption('Crystal Hunter')
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(40, 680)

    def check_quit_in_menus(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def restart(self):
        self.bullets_on_screen = []
        self.enemy_bullets_on_screen = []
        self.enemies_on_screen = []
        self.goblets_on_screen = []
        self.death_blocks_on_screen = []
        self.enemy_counter = 0
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

        if mouse[0] and not self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = True
            if play_box.colliderect(mouse_box):
                self.scene = 'gameplay'
                self.menu_screen_mouse_lock = True
            elif exit_box.colliderect(mouse_box):
                self.running = False
                pygame.quit()
                exit()
        elif not mouse[0] and self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = False

        self.check_quit_in_menus()

    def pause(self):
        pygame.display.update()
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
        cont_box = continue_sign.get_rect(topleft=cont_pos)
        exit_box = exit_to_menu.get_rect(topleft=exit_pos)
        mouse_box = pygame.Rect(pygame.mouse.get_pos(), (4, 4))

        if mouse[0] and not self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = True
            if cont_box.colliderect(mouse_box):
                self.scene = 'gameplay'
                self.menu_screen_mouse_lock = True
            elif exit_box.colliderect(mouse_box):
                self.restart()
                self.scene = 'menu'
        elif not mouse[0] and self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = False

        self.check_quit_in_menus()

    def win_screen(self):
        pygame.display.update()
        pygame.mouse.set_visible(True)

        self.screen.fill('gray')
        win_sign = self.menu_font.render('ВЫ ПОБЕДИЛИ', False, 'white')
        exit_sign = self.menu_font.render('ВЫЙТИ В МЕНЮ', False, 'white')
        sx, sy = self.screen.get_size()
        win_x, win_y = win_sign.get_size()
        exit_x, exit_y = exit_sign.get_size()
        win_pos = (sx/2 - win_x/2, sy/4)
        exit_pos = (sx/2 - exit_x/2, sy/3 + win_y + 30)
        self.screen.blit(win_sign, win_pos)
        self.screen.blit(exit_sign, exit_pos)

        mouse = pygame.mouse.get_pressed()
        exit_box = exit_sign.get_rect(topleft=exit_pos)
        mouse_box = pygame.Rect(pygame.mouse.get_pos(), (4, 4))

        if mouse[0] and not self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = True
            if exit_box.colliderect(mouse_box):
                self.restart()
                self.scene = 'menu'
        elif not mouse[0] and self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = False

        self.check_quit_in_menus()

    def lose_screen(self):
        pygame.display.update()
        pygame.mouse.set_visible(True)

        self.screen.fill('gray')
        you_lose_sign = self.menu_font.render('ВЫ ПРОИГРАЛИ', False, 'white')
        exit_sign = self.menu_font.render('ВЫЙТИ', False, 'white')
        sx, sy = self.screen.get_size()
        lose_x, lose_y = you_lose_sign.get_size()
        exit_x, exit_y = exit_sign.get_size()
        lose_pos = (sx / 2 - lose_x / 2, sy / 4 + 20)
        exit_pos = (sx / 2 - exit_x / 2, sy / 2 - 20)
        self.screen.blit(you_lose_sign, lose_pos)
        self.screen.blit(exit_sign, exit_pos)

        mouse = pygame.mouse.get_pressed()
        exit_box = exit_sign.get_rect(topleft=exit_pos)
        mouse_box = pygame.Rect(pygame.mouse.get_pos(), (4, 4))

        if mouse[0] and not self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = True
            if exit_box.colliderect(mouse_box):
                self.restart()
                self.scene = 'menu'
        elif not mouse[0] and self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = False

        self.check_quit_in_menus()

    def main_render(self, mouse_pos):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.cursor_icon, mouse_pos)
        self.screen.blit(self.player.sprites[self.player.direction], (self.player.x, self.player.y))
        self.player.show_ammo(self.screen)

    def check_inputs_gameplay(self):
        keys = pygame.key.get_pressed()
        mouse_click = pygame.mouse.get_pressed()

        if mouse_click[0] or keys[pygame.K_l]:
            self.player.single_shot(array=self.bullets_on_screen)
        else:
            self.player.unlock_gun()

        if keys[pygame.K_d]:
            self.player.move_right(edge=1247)
        if keys[pygame.K_a]:
            self.player.move_left(edge=1)
        if keys[pygame.K_SPACE] or self.player.is_jump:
            self.player.jump(self.gravity, self.ground)

        self.player.get_hitbox()

        placing_objects_keys = [
            keys[pygame.K_i],
            keys[pygame.K_o],
            keys[pygame.K_p],
            keys[pygame.K_m],
            keys[pygame.K_f]
        ]

        if not self.place_objects_lock:
            if keys[pygame.K_i]:
                self.place_object('low', 'enemy')
            elif keys[pygame.K_o]:
                self.place_object('high', 'enemy')
            elif keys[pygame.K_p]:
                self.place_object('circle', 'enemy')
            elif keys[pygame.K_m]:
                self.place_object('goblet', 'goblet')
            elif keys[pygame.K_f]:
                self.place_object('death_block', 'solid_object')
        elif not any(placing_objects_keys):
            self.place_objects_lock = False

        if keys[pygame.K_ESCAPE]:
            self.player.shot_lock = True
            self.place_objects_lock = True
            self.scene = 'pause'

    def place_object(self, var, obj_type):
        mx, my = pygame.mouse.get_pos()
        match var:
            case 'low':
                game_object = LowTurret(x=mx, y=my)
            case 'high':
                game_object = HighTurret(x=mx, y=my)
            case 'circle':
                game_object = CircleTurret(x=mx, y=my)
            case 'goblet':
                game_object = Goblet(x=mx, y=my)
            case 'death_block':
                game_object = GameSolidObject(x=mx, y=my, path='materials/images/ground/death_block.png')
        match obj_type:
            case 'enemy':
                self.enemy_counter += 1
                game_object.timer = pygame.USEREVENT + 10 + self.enemy_counter
                pygame.time.set_timer(game_object.timer, game_object.reload_time)
                self.enemies_on_screen.append(game_object)
            case 'goblet':
                self.goblets_on_screen.append(game_object)
            case 'solid_object':
                self.death_blocks_on_screen.append(game_object)
        self.place_objects_lock = True

    def check_enemies(self):
        for enemy in self.enemies_on_screen:
            if enemy.health <= 0:
                self.enemies_on_screen.remove(enemy)
                del enemy
                continue
            self.screen.blit(enemy.sprites[enemy.direction], (enemy.x, enemy.y))
            enemy.direction = 0 if self.player.x >= enemy.x else 1
            enemy.get_hitbox()
            if not self.player.invincible and self.player.hitbox.colliderect(enemy.hitbox):
                self.player.take_damage()

    def check_player_bullets(self):
        for bullet in self.bullets_on_screen:
            if not -20 <= bullet.x <= 1300:
                self.bullets_on_screen.remove(bullet)
                continue
            self.screen.blit(bullet.sprites[bullet.direction], (bullet.x, bullet.y))
            bullet.x += (1 - 2 * bullet.direction) * bullet.speed
            bullet.get_hitbox()
            for enemy in self.enemies_on_screen:
                if enemy.hitbox.colliderect(bullet.hitbox):
                    enemy.health -= 1
                    self.bullets_on_screen.remove(bullet)
                    del bullet
                    break

    def check_enemy_bullets(self):
        for bullet in self.enemy_bullets_on_screen:
            if not (-20 <= bullet.x <= 1300):
                self.enemy_bullets_on_screen.remove(bullet)
                continue
            self.screen.blit(bullet.sprites[bullet.direction], (bullet.x, bullet.y))
            bullet.x += (1 - 2 * bullet.direction) * bullet.speed
            bullet.get_hitbox()
            if not self.player.invincible and self.player.hitbox.colliderect(bullet.hitbox):
                self.player.take_damage()
                self.enemy_bullets_on_screen.remove(bullet)
                del bullet

    def check_gameplay_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            if event.type == self.player.reload_timer:
                self.player.reload()
            for enemy in self.enemies_on_screen:
                if event.type == enemy.timer:
                    enemy.shot(self.enemy_bullets_on_screen)
                    break
            if self.player.invincible:
                if event.type == self.player.inframes_timer:
                    self.player.invincible = False

    def check_losing(self):
        for db in self.death_blocks_on_screen:
            self.screen.blit(db.sprite, (db.x, db.y))
            if db.hitbox.colliderect(self.player.hitbox):
                self.player.health = 0
        if self.player.health <= 0:
            self.scene = 'lose_screen'
            self.restart()
            self.player.shot_lock = True
            self.place_objects_lock = True

    def check_winning(self):
        for goblet in self.goblets_on_screen:
            self.screen.blit(goblet.sprite, (goblet.x, goblet.y))
            if goblet.hitbox.colliderect(self.player.hitbox):
                self.scene = 'win_screen'
                self.restart()
                self.player.shot_lock = True
                self.place_objects_lock = True

    def gameplay(self):
        pygame.display.update()
        pygame.mouse.set_visible(False)

        # get positions and triggers
        mx, my = pygame.mouse.get_pos()
        self.player.direction = 0 if self.player.x <= mx else 1

        self.main_render((mx, my))
        self.check_inputs_gameplay()
        self.check_enemies()
        self.check_player_bullets()
        self.check_enemy_bullets()
        self.check_gameplay_events()
        self.check_losing()
        self.check_winning()

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
            case 'lose_screen':
                game.lose_screen()
            case 'win_screen':
                game.win_screen()
    pygame.quit()
    exit()
