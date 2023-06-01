import pygame
import os
from enemies import LowTurret, HighTurret, CircleTurret, EnemyBullet
from player import Player, Goblet, Bullet
from level import GameSolidObject, Level


class Game:
    def __init__(self):
        pygame.init()
        self.gameplay_screen_init()

        self.last_scene = ''
        self.scene = 'menu'
        self.gravity = 0.2
        self.enemy_counter = 0
        self.ground = 680
        self.menu_screen_mouse_lock = True
        self.place_objects_lock = True

        self.bg = pygame.image.load('materials/images/background.png').convert_alpha()
        self.cursor_icon = pygame.image.load('materials/images/cursor.png').convert_alpha()
        self.gear_icon = pygame.image.load('materials/images/editor_icon.png').convert_alpha()

        self.bullets_on_screen = []
        self.enemy_bullets_on_screen = []
        self.enemies_on_screen = []
        self.goblets_on_screen = []
        self.death_blocks_on_screen = []
        self.solid_blocks = []

        self.editor_placement_lock = True
        self.editor_player_pos = (0, 0)
        self.editor_current_obj = -1
        self.editor_sprites = [
            pygame.image.load('materials/images/ground/big_block.png').convert_alpha(),
            pygame.image.load('materials/images/ground/small_block.png').convert_alpha(),
            pygame.image.load('materials/images/ground/death_block.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/turrets/low_turret_left.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/turrets/high_turret_left.png').convert_alpha(),
            pygame.image.load('materials/images/enemies/turrets/circle_turret.png').convert_alpha(),
            pygame.image.load('materials/images/character/combine/player_in_editor.png').convert_alpha(),
            pygame.image.load('materials/images/character/goblet.png').convert_alpha(),
        ]
        self.editor_selection_boxes = []
        for i in range(len(self.editor_sprites)):
            box = pygame.Rect(((1281 + 60 * (i % 2), 60 * (i // 2)), (60, 60)))
            self.editor_selection_boxes.append((i, box))

        self.menu_font = pygame.font.Font('materials/fonts/RussoOne-Regular.ttf', 40)

        self.gameplay_screen_init()
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(40, 100)

    def gameplay_screen_init(self):
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Crystal Hunter')
        self.icon = pygame.image.load('materials/images/simp_moment_right.png').convert_alpha()
        pygame.display.set_icon(self.icon)

    def save_level(self):
        name = input('Введите название сохранения')
        current = Level(name=name, x=self.player.x, y=self.player.y, ammo=self.player.ammo, hp=self.player.health)
        current.enemies = self.enemies_on_screen
        current.death_blocks = self.death_blocks_on_screen
        current.solid_blocks = self.solid_blocks
        current.player_bullets = self.bullets_on_screen
        current.enemy_bullets = self.enemy_bullets_on_screen
        current.goblets = self.goblets_on_screen
        current.save()

    def load_level(self, name):
        self.restart()
        with open(f'saves/{name}.txt') as f:
            game_objects = f.readlines()
            for obj in game_objects:
                obj = obj.replace('\n', '')
                obj = obj.split('-')
                code, x, y = obj[0], float(obj[1]), float(obj[2])
                match code:
                    case '00':
                        self.player = Player(x=x, y=y, ammo=int(obj[3]), hp=int(obj[4]))
                    case '01':
                        t = obj[3]
                        match t:
                            case '0':
                                self.place_object(var='low', obj_type='enemy', pos=(x, y), en_hp=int(obj[4]))
                            case '1':
                                self.place_object(var='high', obj_type='enemy', pos=(x, y), en_hp=int(obj[4]))
                            case '2':
                                self.place_object(var='circle', obj_type='enemy', pos=(x, y), en_hp=int(obj[4]))
                    case '02':
                        t = obj[3]
                        match t:
                            case '0':
                                self.place_object(var='death_block', obj_type='death_block', pos=(x, y))
                            case '1':
                                self.place_object(var='big_block', obj_type='solid_block', pos=(x, y))
                            case '2':
                                self.place_object(var='small_block', obj_type='solid_block', pos=(x, y))
                    case '03':
                        direction = int(obj[3])
                        self.place_object(var='player_bullet', obj_type='player_bullet', pos=(x, y), direction=direction)
                    case '04':
                        direction = int(obj[3])
                        self.place_object(var='enemy_bullet', obj_type='enemy_bullet', pos=(x, y), direction=direction)
                    case '05':
                        self.place_object(var='goblet', obj_type='goblet', pos=(x, y))

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
        self.solid_blocks = []
        self.enemy_counter = 0
        self.player = Player(40, 100)
        bl = GameSolidObject(x=40, y=650, path='materials/images/ground/big_block.png', t=1)
        game.solid_blocks.append(bl)

    def main_menu(self):
        pygame.display.update()
        pygame.mouse.set_visible(True)

        self.screen.fill('gray')
        play_sign = self.menu_font.render('ИГРАТЬ', False, 'white')
        exit_from_game_sign = self.menu_font.render('ВЫЙТИ ИЗ ИГРЫ', False, 'white')
        editor_sign = self.menu_font.render('РЕДАКТОР УРОВНЕЙ', False, 'white')
        sx, sy = self.screen.get_size()
        play_x, play_y = play_sign.get_size()
        exit_x, exit_y = exit_from_game_sign.get_size()
        editor_x, editor_y = editor_sign.get_size()
        play_pos = (sx/2 - play_x/2, sy/4)
        edit_pos = (sx/2 - editor_x/2, sy/4 + 80)
        exit_pos = (sx/2 - exit_x/2, sy/4 + 160)
        self.screen.blit(play_sign, play_pos)
        self.screen.blit(editor_sign, edit_pos)
        self.screen.blit(exit_from_game_sign, exit_pos)

        mouse = pygame.mouse.get_pressed()
        play_box = play_sign.get_rect(topleft=play_pos)
        edit_box = editor_sign.get_rect(topleft=edit_pos)
        exit_box = exit_from_game_sign.get_rect(topleft=exit_pos)
        mouse_box = pygame.Rect(pygame.mouse.get_pos(), (4, 4))

        if mouse[0] and not self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = True
            if play_box.colliderect(mouse_box):
                self.scene = 'gameplay'
                self.menu_screen_mouse_lock = True
            elif edit_box.colliderect(mouse_box):
                self.scene = 'editor'
                self.init_editor()
                self.menu_screen_mouse_lock = True
            elif exit_box.colliderect(mouse_box):
                self.running = False
                pygame.quit()
                exit()
        elif not mouse[0] and self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = False

        self.check_quit_in_menus()

    def level_select(self):
        pass

    def pause(self):
        pygame.display.update()
        pygame.mouse.set_visible(True)
        self.screen.fill('gray')
        continue_sign = self.menu_font.render('ПРОДОЛЖИТЬ', False, 'white')
        save_sign = self.menu_font.render('СОХРАНИТЬ', False, 'white')
        load_sign = self.menu_font.render('ЗАГРУЗИТЬ СОХРАНЕНИЕ', False, 'white')
        exit_to_menu = self.menu_font.render('ВЫЙТИ В МЕНЮ', False, 'white')
        sx, sy = self.screen.get_size()
        cont_x, cont_y = continue_sign.get_size()
        save_x, save_y = save_sign.get_size()
        load_x, load_y = load_sign.get_size()
        exit_x, exit_y = exit_to_menu.get_size()
        cont_pos = (sx / 2 - cont_x / 2, sy / 4)
        save_pos = (sx / 2 - save_x / 2, sy / 4 + cont_y + 30)
        load_pos = (sx / 2 - load_x / 2, sy / 4 + cont_y + save_y + 60)
        exit_pos = (sx / 2 - exit_x / 2, sy / 4 + cont_y + save_y + load_y + 90)
        self.screen.blit(continue_sign, cont_pos)
        self.screen.blit(save_sign, save_pos)
        self.screen.blit(load_sign, load_pos)
        self.screen.blit(exit_to_menu, exit_pos)

        mouse = pygame.mouse.get_pressed()
        cont_box = continue_sign.get_rect(topleft=cont_pos)
        save_box = save_sign.get_rect(topleft=save_pos)
        load_box = load_sign.get_rect(topleft=load_pos)
        exit_box = exit_to_menu.get_rect(topleft=exit_pos)
        mouse_box = pygame.Rect(pygame.mouse.get_pos(), (4, 4))

        if mouse[0] and not self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = True
            if cont_box.colliderect(mouse_box):
                self.scene = self.last_scene
                self.menu_screen_mouse_lock = True
            elif exit_box.colliderect(mouse_box):
                self.restart()
                self.scene = 'menu'
                if self.last_scene == 'editor':
                    self.gameplay_screen_init()
            elif save_box.colliderect(mouse_box):
                self.save_level()
            elif load_box.colliderect(mouse_box):
                self.scene = 'loading_screen'
        elif not mouse[0] and self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = False

        self.check_quit_in_menus()

    def loading_screen(self):
        pygame.display.update()
        pygame.mouse.set_visible(True)
        mouse = pygame.mouse.get_pressed()
        mouse_box = pygame.Rect(pygame.mouse.get_pos(), (4, 4))
        self.screen.fill('gray')

        exit_sign = self.menu_font.render('ВЕРНУТЬСЯ НАЗАД', False, 'white')
        sx, sy = self.screen.get_size()
        ex, ey = exit_sign.get_size()
        self.screen.blit(exit_sign, (sx / 2 - ex / 2, 50))
        exit_box = pygame.Rect((sx / 2 - ex / 2, 50), (ex, ey))

        filenames = os.listdir('saves')
        correct_files = [file for file in filenames if file.endswith('.txt')]
        cur_x, cur_y = 100, 100
        hitboxes = []
        for savefile in correct_files:
            savefile = savefile.replace('.txt', '')
            name_sign = self.menu_font.render(savefile, False, 'white')
            self.screen.blit(name_sign, (cur_x, cur_y))
            hitboxes.append((pygame.Rect((cur_x, cur_y), name_sign.get_size()), savefile))
            cur_y += 50

        if mouse[0] and not self.menu_screen_mouse_lock:
            self.menu_screen_mouse_lock = True
            if exit_box.colliderect(mouse_box):
                self.scene = 'pause'
            for (hitbox, name) in hitboxes:
                if hitbox.colliderect(mouse_box):
                    self.load_level(name=name)
                    self.scene = 'pause'
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

    def init_editor(self):
        self.screen = pygame.display.set_mode((1400, 720))
        pygame.display.set_icon(self.gear_icon)
        pygame.display.set_caption('Editor')

    def editor_playground_render(self, surf):
        w, h = surf.get_size()
        surf.blit(self.bg, (0, 0))
        for i in range(0, w + 1, 16):
            pygame.draw.line(surf, 'gray', (i, 0), (i, h))
        for i in range(0, h + 1, 16):
            pygame.draw.line(surf, 'gray', (0, i), (w, i))
        for bl in self.solid_blocks:
            surf.blit(bl.sprite, (bl.x, bl.y))
        for db in self.death_blocks_on_screen:
            surf.blit(db.sprite, (db.x, db.y))
        for en in self.enemies_on_screen:
            surf.blit(en.sprites[1], (en.x, en.y))
        for g in self.goblets_on_screen:
            surf.blit(g.sprite, (g.x, g.y))
        player = pygame.image.load('materials/images/character/combine/player_in_editor.png').convert_alpha()
        surf.blit(player, self.editor_player_pos)
        self.screen.blit(surf, (0, 0))

    def editor_selection_panel_render(self, surf):
        surf.fill((40, 62, 197))
        for i in range(len(self.editor_sprites)):
            if i == self.editor_current_obj:
                pygame.draw.rect(surf, (92, 10, 33), (60 * (i % 2), 60 * (i // 2), (60, 60)))
            sprite = self.editor_sprites[i]
            (w, h) = sprite.get_size()
            surf.blit(sprite, (60 * (i % 2) + 30 - w/2, 60 * (i // 2) + 30 - h/2))

        self.screen.blit(surf, (1281, 0))

    def editor(self):
        pygame.display.update()
        pygame.mouse.set_visible(True)
        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        (mx, my) = pygame.mouse.get_pos()

        selection_panel = pygame.Surface((120, 720))
        playground = pygame.Surface((1280, 720))
        self.editor_playground_render(surf=playground)
        self.editor_selection_panel_render(surf=selection_panel)

        if keys[pygame.K_ESCAPE]:
            self.editor_placement_lock = True
            self.last_scene = 'editor'
            self.scene = 'pause'

        if (mouse[0] or mouse[1]) and not self.editor_placement_lock:
            self.editor_placement_lock = True
            if 0 <= mx <= 1280:
                self.editor_check_playground_inputs(playground)
            elif 1281 <= mx <= 1400:
                self.editor_check_selection_panel_inputs(selection_panel)
        elif not mouse[0] and not mouse[1] and self.editor_placement_lock:
            self.editor_placement_lock = False

        self.check_quit_in_menus()

    def main_render(self, mouse_pos):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.cursor_icon, mouse_pos)
        self.screen.blit(self.player.sprites[self.player.direction], (self.player.x - self.player.direction * 18, self.player.y))
        for bl in self.solid_blocks:
            self.screen.blit(bl.sprite, (bl.x, bl.y))
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
            if self.player.hitbox.collideobjects([b.hitbox for b in self.solid_blocks]):
                self.player.move_left(edge=1)
        if keys[pygame.K_a]:
            self.player.move_left(edge=1)
            if self.player.hitbox.collideobjects([b.hitbox for b in self.solid_blocks]):
                self.player.move_right(edge=1247)

        if not self.player.in_air:
            self.player.y += self.gravity
            self.player.get_hitboxes()
            if not self.player.leg_hitbox.collideobjects([b.hitbox for b in self.solid_blocks]):
                self.player.in_air = True
            self.player.y -= self.gravity
            self.player.get_hitboxes()

        if keys[pygame.K_SPACE] or self.player.in_air:
            if not self.player.in_air:
                self.player.jump_height = 7.19
                self.player.in_air = True
            self.player.jump_height -= self.gravity
            self.player.y -= self.player.jump_height
            self.player.get_hitboxes()
            while self.player.head_hitbox.collideobjects([b.hitbox for b in self.solid_blocks]):
                self.player.y += self.gravity
                self.player.get_hitboxes()
                self.player.jump_height = 0
                self.player.in_air = True
            while self.player.leg_hitbox.collideobjects([b.hitbox for b in self.solid_blocks]):
                self.player.y -= self.gravity
                self.player.get_hitboxes()
                self.player.jump_height = 0
                self.player.in_air = False

        placing_objects_keys = [
            keys[pygame.K_i],
            keys[pygame.K_o],
            keys[pygame.K_p],
            keys[pygame.K_m],
            keys[pygame.K_f],
            keys[pygame.K_b],
            keys[pygame.K_n]
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
                self.place_object('death_block', 'death_block')
            elif keys[pygame.K_b]:
                self.place_object('big_block', 'solid_block')
            elif keys[pygame.K_n]:
                self.place_object('small_block', 'solid_block')
        elif not any(placing_objects_keys):
            self.place_objects_lock = False

        if keys[pygame.K_ESCAPE]:
            self.player.shot_lock = True
            self.place_objects_lock = True
            self.last_scene = 'gameplay'
            self.scene = 'pause'

    def place_object(self, var, obj_type, pos=None, en_hp=6, direction=None):
        if not pos:
            x, y = pygame.mouse.get_pos()
        else:
            x, y = pos
        match var:
            case 'low':
                game_object = LowTurret(x=x, y=y, hp=en_hp)
            case 'high':
                game_object = HighTurret(x=x, y=y, hp=en_hp)
            case 'circle':
                game_object = CircleTurret(x=x, y=y, hp=en_hp)
            case 'goblet':
                game_object = Goblet(x=x, y=y)
            case 'death_block':
                game_object = GameSolidObject(x=x, y=y, path='materials/images/ground/death_block.png', t=0)
            case 'big_block':
                game_object = GameSolidObject(x=x, y=y, path='materials/images/ground/big_block.png', t=1)
            case 'small_block':
                game_object = GameSolidObject(x=x, y=y, path='materials/images/ground/small_block.png', t=2)
            case 'player_bullet':
                game_object = Bullet(direction=direction, x=x, y=y)
            case 'enemy_bullet':
                game_object = EnemyBullet(direction=direction, x=x, y=y)
        match obj_type:
            case 'enemy':
                self.enemy_counter += 1
                game_object.timer = pygame.USEREVENT + 10 + self.enemy_counter
                pygame.time.set_timer(game_object.timer, game_object.reload_time)
                self.enemies_on_screen.append(game_object)
            case 'goblet':
                self.goblets_on_screen.append(game_object)
            case 'death_block':
                self.death_blocks_on_screen.append(game_object)
            case 'solid_block':
                self.solid_blocks.append(game_object)
            case 'e_bullet':
                self.enemy_bullets_on_screen.append(game_object)
            case 'p_bullet':
                self.bullets_on_screen.append(game_object)
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
                del bullet
                continue
            if bullet.hitbox.collideobjects([b.hitbox for b in self.solid_blocks]):
                self.bullets_on_screen.remove(bullet)
                del bullet
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
            if bullet.hitbox.collideobjects([b.hitbox for b in self.solid_blocks]):
                self.enemy_bullets_on_screen.remove(bullet)
                del bullet
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
        if self.player.y > 850:
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
    block = GameSolidObject(x=40, y=650, path='materials/images/ground/big_block.png', t=1)
    game.solid_blocks.append(block)
    while game.running:
        match game.scene:
            case 'menu':
                game.main_menu()
            case 'level_select':
                game.level_select()
            case 'gameplay':
                game.gameplay()
            case 'pause':
                game.pause()
            case 'lose_screen':
                game.lose_screen()
            case 'win_screen':
                game.win_screen()
            case 'loading_screen':
                game.loading_screen()
            case 'editor':
                game.editor()
    pygame.quit()
    exit()
