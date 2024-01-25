import pygame, sys
from pygame.locals import *
from Alien import Alien
from load_func import load_map
from finish import finish

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Pygame Platformer')
WINDOW_SIZE = sc_width, sc_height = (1000, 700)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
DISPLAY_SIZE = display_width, display_height = (500, 300)
display = pygame.Surface(DISPLAY_SIZE)
clock = pygame.time.Clock()

get_key_sound = pygame.mixer.Sound('sounds/get_key.mp3')
lose_sound = pygame.mixer.Sound('sounds/game_over.mp3')
game_music = pygame.mixer.Sound('sounds/game.mp3')


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, player_rect, bullet_rects):
        super().__init__()
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.flip_image = pygame.image.load("images/bullet_flip.png").convert_alpha()
        self.bullet_rects = bullet_rects
        self.b_rect = pygame.Rect(int(player_rect.center[0]), int(player_rect.center[1]), self.image.get_height(),
                                  self.image.get_width())
        self.bullet_rects.append(self.b_rect)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, bullet_rects, blts_group, a_rects):
        self.mask = pygame.mask.from_surface(self.image)
        if self in bullets_right:
            self.b_rect.x += 5
            self.rect.x += 5
        else:
            self.image = self.flip_image
            self.b_rect.x -= 5
            self.rect.x -= 5

        for b in blts_group:
            for r in a_rects:
                if b.rect.colliderect(r):
                    blts_group.remove(b)
        return blts_group



class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, lvl):
        super().__init__()
        self.key_img = pygame.image.load("images/key.png")
        self.image = self.key_img
        if lvl == 1:
            self.rect_for_collide = pygame.Rect(2420, 370, self.image.get_width(), self.image.get_height())
        elif lvl == 2:
            self.rect_for_collide = pygame.Rect(1090, 40, self.image.get_width(), self.image.get_height())
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player_rect, is_key):
        if self.rect_for_collide.colliderect(player_rect):
            is_key = True
        return is_key


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, lvl):
        super().__init__()
        self.close_portal = pygame.image.load("images/portal/close_portal.png")
        self.open_portal = pygame.image.load("images/portal/open_portal.png")
        self.image = self.close_portal
        if lvl == 1:
            self.rect_for_collide = pygame.Rect(-2, 280, self.image.get_height(), self.image.get_width())
        elif lvl == 2:
            self.rect_for_collide = pygame.Rect(0, 730, self.image.get_height(), self.image.get_width())

        self.lvl = lvl

        self.rect = self.image.get_rect()
        self.rect.bottom = y + 30
        self.rect.left = (x - self.rect.w // 2) + 35

    def update(self, player_rect, key_blit):
        if self.rect_for_collide.colliderect(player_rect):
            if key_blit != True:
                self.image = self.open_portal
                if self.lvl == 1:
                    start_lvl2_()
                elif self.lvl == 2:
                    finish()
            else:
                display_centered_text("Find the key to open the portal", (255, 255, 255))


class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/finish.png")
        self.rect_for_collide = pygame.Rect(50, 10, self.image.get_width(), self.image.get_height())
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player_rect):
        if self.rect_for_collide.colliderect(player_rect):
            finish()


class Health(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.one = pygame.image.load("images/health/one_hp.png")
        self.two = pygame.image.load("images/health/two_hp.png")
        self.three = pygame.image.load("images/health/three_hp.png")
        self.image = self.three

    def update(self, hp):
        if hp == 2:
            self.image = self.two
        elif hp == 1:
            self.image = self.one


walk_left = [
    pygame.image.load("images/astronaut/astronaut_left/left1.png").convert(),
    pygame.image.load("images/astronaut/astronaut_left/left2.png").convert(),
    pygame.image.load("images/astronaut/astronaut_left/left3.png").convert(),
    pygame.image.load("images/astronaut/astronaut_left/left4.png").convert()
]
walk_right = [

    pygame.image.load("images/astronaut/astronaut_right/right1.png").convert(),
    pygame.image.load("images/astronaut/astronaut_right/right2.png").convert(),
    pygame.image.load("images/astronaut/astronaut_right/right3.png").convert(),
    pygame.image.load("images/astronaut/astronaut_right/right4.png").convert()
]
static = pygame.image.load("images/astronaut/static.png").convert_alpha()

bullets_left = pygame.sprite.Group()
bullets_right = pygame.sprite.Group()

aliens = pygame.sprite.Group()

list_of_aliens_coords = [(100, 220)]

tiles_group = pygame.sprite.Group()


def get_mouse_pos(mouse_pos):
    cursor_sprite.rect.x = mouse_pos[0]
    cursor_sprite.rect.y = mouse_pos[1]


cursor = pygame.sprite.Group()
cursor_sprite = pygame.sprite.Sprite()
cursor_sprite.image = pygame.image.load("images/cursor.png")
cursor_sprite.rect = cursor_sprite.image.get_rect()

cursor.add(cursor_sprite)


def display_centered_text(text, color):
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(display_width // 2, display_height // 4))
    display.blit(text_surface, text_rect)


def create_restart_button(action):
    WHITE = (255, 255, 255)
    LIGHT_GREEN = (0, 255, 0)
    DARK_GREEN = (8, 117, 8)
    width = 180
    height = 50
    x = WINDOW_SIZE[0] // 2 - width // 2
    y = WINDOW_SIZE[1] // 2 - height // 2
    inactive_color = LIGHT_GREEN
    active_color = DARK_GREEN
    text = "RESTART"
    text_color = WHITE
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 5)
    x += 10
    y += 10
    size = 50
    font = pygame.font.SysFont(None, size)
    text_render = font.render(text, True, text_color)
    screen.blit(text_render, (x, y))


def restart_menu(action):
    lose_sound.play()
    while True:
        screen.fill((0, 0, 0))
        create_restart_button(action)

        if pygame.mouse.get_focused():
            cursor.update()
            cursor.draw(screen)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                get_mouse_pos(event.pos)


def show_count_of_bullets(c):
    image = pygame.image.load("images/bullet_big_size.png")
    font = pygame.font.SysFont(None, 25)
    count_of_bullets_text = font.render(f": {str(c)}", True, (86, 143, 58))
    display.blit(count_of_bullets_text, (31, 25))
    display.blit(image, (0, 24))


def collision_test(rect, tiles):
    hit_list = []

    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types


def terminate():
    pygame.quit()
    sys.exit()


def damage():
    damage = pygame.Surface((1000, 700))
    damage.fill((255, 0, 0))
    damage.set_alpha(128)
    display.blit(damage, (0, 0))


def start_lvl1_():
    bg = pygame.image.load("images/fon2.png").convert_alpha()
    bg_x = -500

    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0

    true_scroll = [0, 0]

    player_anim_count = 0

    game_map = load_map('map_for_lvl1')
    moon_block = pygame.image.load('images/dirt.png')

    moon_sprite = pygame.sprite.Sprite()
    moon_sprite.image = moon_block

    player_rect = pygame.Rect(80, 280, 35, 50)

    hp = 3
    health = Health()

    count_of_bullets = 15

    is_key = False
    key_blit = True
    running = True
    gameplay = True
    bullets_rects = list()
    a_rects = [pygame.Rect(240, 340, 25, 40), pygame.Rect(716, 310, 35, 50), pygame.Rect(896, 310, 35, 50),
               pygame.Rect(777, 130, 35, 50), pygame.Rect(659, 130, 35, 50), pygame.Rect(237, 40, 35, 50),
               pygame.Rect(175, 40, 35, 50), pygame.Rect(1227, 370, 35, 50), pygame.Rect(1319, 370, 35, 50),
               pygame.Rect(2006, 190, 35, 50), pygame.Rect(2096, 190, 35, 50), pygame.Rect(2007, 370, 35, 50),
               pygame.Rect(2155, 370, 35, 50)]

    lst_of_aliens_coords = [(6, 2), (8, 2), (22, 5), (26, 5), (67, 7), (70, 7), (24, 11), (30, 11), (8, 12), (41, 13),
                            (44, 13), (67, 13), (72, 13)]
    game_music.play(-1)

    while running:
        if gameplay:
            pygame.mouse.set_visible(False)
            display.blit(pygame.transform.scale(bg, (1000, 500)), (bg_x, 0))
            true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 30
            true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 30
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            tile_rects = []
            y = 0
            for layer in game_map:
                x = 0
                for tile in layer:
                    if tile == '1':
                        display.blit(moon_block, (x * 30 - scroll[0], y * 30 - scroll[1]))
                    if tile == "p":
                        portal = Portal(x * 30 - scroll[0], y * 30 - scroll[1], 1)
                    if tile == "k":
                        key = Key(x * 30 - scroll[0], y * 30 - scroll[1], 1)
                    if tile == '1':
                        tile_rects.append(pygame.Rect(x * 30, y * 30, 30, 30))
                        moon_sprite.rect = pygame.Rect(x * 30, y * 30, 30, 30)
                        tiles_group.add(moon_sprite)

                    x += 1
                y += 1

            display.blit(static, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

            for i in lst_of_aliens_coords:
                print(i)
                a = Alien(i[0] * 30 - scroll[0], i[1] * 30 - scroll[1] - 5)
                display.blit(a.image, (a.rect.x, a.rect.y))
                bullet_rects, lst_of_aliens_coords, hp \
                    = a.update(player_rect, hp, bullets_rects, lst_of_aliens_coords, i, a_rects)
                # print(lst_of_aliens_coords, i)
                # print(a_rects)

            player_movement = [0, 0]
            if moving_right == True:
                player_movement[0] += 2
                display.blit(walk_right[int(str(player_anim_count)[0])],
                             (player_rect.x - scroll[0], player_rect.y - scroll[1]))

            if moving_left == True:
                if player_rect.x >= 0:
                    player_movement[0] -= 2
                    display.blit(walk_left[int(str(player_anim_count)[0])],
                                 (player_rect.x - scroll[0], player_rect.y - scroll[1]))

            player_movement[1] += vertical_momentum
            vertical_momentum += 0.2
            if vertical_momentum > 5:
                vertical_momentum = 5

            if player_anim_count >= 3:
                player_anim_count = 0
            else:
                player_anim_count += 0.1

            player_rect, collisions = move(player_rect, player_movement, tile_rects)

            if collisions['bottom'] == True:
                air_timer = 0
                vertical_momentum = 0
            else:
                air_timer += 1

            if player_rect.y >= 450:
                hp -= 1

            display.blit(health.image, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT or event.key == K_d:
                        moving_right = True
                    if event.key == K_LEFT or event.key == K_a:
                        moving_left = True
                    if event.key == K_UP or event.key == K_w:
                        if air_timer < 6:
                            vertical_momentum = -5

                if event.type == KEYUP:
                    if event.key == K_RIGHT or event.key == K_d:
                        moving_right = False
                    if event.key == K_LEFT or event.key == K_a:
                        moving_left = False
                    if event.key == K_SPACE:
                        if count_of_bullets > 0:

                            b = Bullet(int(player_rect.center[0] - scroll[0]), int(player_rect.center[1] - scroll[1]),
                                       player_rect, bullets_rects)
                            count_of_bullets -= 1
                            if moving_left:
                                bullets_left.add(b)
                            else:
                                bullets_right.add(b)

            show_count_of_bullets(count_of_bullets)

            if hp <= 0:
                gameplay = False

            portal.update(player_rect, key_blit)

            display.blit(portal.image, (portal.rect.x, portal.rect.y))

            if key.update(player_rect, is_key) == True:
                key_blit = False

            if key_blit:
                display.blit(key.image, (key.rect.x, key.rect.y))

            bullets_left.draw(display)
            bullets_left.update(bullet_rects, bullets_left, a_rects)

            bullets_right.draw(display)
            bullets_right.update(bullet_rects, bullets_right, a_rects)

            health.update(hp)
            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()
            clock.tick(60)
        else:
            restart_menu(start_lvl1_)


def start_lvl2_():
    bg = pygame.image.load("images/fon2.png").convert_alpha()
    bg_x = -500

    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0

    true_scroll = [0, 0]

    player_anim_count = 0
    a = 1

    game_map = load_map('map_for_lvl2')  # Считываем карту из файла map.txt
    moon_block = pygame.image.load('images/fire_block.png')  # блок замка

    moon_sprite = pygame.sprite.Sprite()
    moon_sprite.image = moon_block

    player_rect = pygame.Rect(105, 730, 35, 50)

    hp = 3
    health = Health()

    count_of_bullets = 10

    is_key = False
    key_blit = True
    running = True
    gameplay = True
    bullets_rects = list()
    a_rects = [pygame.Rect(625, 700, 35, 50), pygame.Rect(536, 730, 35, 50), pygame.Rect(777, 520, 35, 50),
               pygame.Rect(118, 340, 35, 50), pygame.Rect(28, 340, 35, 50), pygame.Rect(28, 340, 35, 50),
               pygame.Rect(325, 70, 35, 50), pygame.Rect(441, 40, 35, 50), pygame.Rect(625, 70, 35, 50),
               pygame.Rect(1015, 40, 35, 50)]
    lst_of_aliens_coords_for_lvl_2_ = [(15, 2), (34, 2), (11, 3), (21, 3), (39, 11), (1, 12), (4, 12), (26, 18),
                                       (21, 24), (18, 25)]
    game_music.play(-1)

    while running:
        if gameplay:
            pygame.mouse.set_visible(False)
            display.blit(pygame.transform.scale(bg, (1000, 500)), (bg_x, 0))
            true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 30
            true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 30
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            tile_rects = []
            y = 0
            for layer in game_map:
                x = 0
                for tile in layer:
                    if tile == '1':
                        display.blit(moon_block, (x * 30 - scroll[0], y * 30 - scroll[1]))
                        tile_rects.append(pygame.Rect(x * 30, y * 30, 30, 30))
                        moon_sprite.rect = pygame.Rect(x * 30, y * 30, 30, 30)
                        tiles_group.add(moon_sprite)
                    if tile == "p":
                        portal = Portal(x * 30 - scroll[0], y * 30 - scroll[1], 2)
                    if tile == "k":
                        key = Key(x * 30 - scroll[0], y * 30 - scroll[1], 2)


                    x += 1
                y += 1

            display.blit(static, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

            for i in lst_of_aliens_coords_for_lvl_2_:
                a = Alien(i[0] * 30 - scroll[0], i[1] * 30 - scroll[1] - 5)
                display.blit(a.image, (a.rect.x, a.rect.y))
                bullet_rects, lst_of_aliens_coords_for_lvl_2_, hp \
                    = a.update(player_rect, hp, bullets_rects, lst_of_aliens_coords_for_lvl_2_, i, a_rects)

            player_movement = [0, 0]
            if moving_right == True:
                player_movement[0] += 2
                display.blit(walk_right[int(str(player_anim_count)[0])],
                             (player_rect.x - scroll[0], player_rect.y - scroll[1]))

            if moving_left == True:
                if player_rect.x >= 0:
                    player_movement[0] -= 2
                    display.blit(walk_left[int(str(player_anim_count)[0])],
                                 (player_rect.x - scroll[0], player_rect.y - scroll[1]))

            player_movement[1] += vertical_momentum
            vertical_momentum += 0.2
            if vertical_momentum > 5:
                vertical_momentum = 5

            if player_anim_count >= 3:
                player_anim_count = 0
            else:
                player_anim_count += 0.1

            player_rect, collisions = move(player_rect, player_movement, tile_rects)

            if collisions['bottom'] == True:
                air_timer = 0
                vertical_momentum = 0
            else:
                air_timer += 1

            if player_rect.y >= 799:
                hp -= 1

            display.blit(health.image, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT or event.key == K_d:
                        moving_right = True
                    if event.key == K_LEFT or event.key == K_a:
                        moving_left = True
                    if event.key == K_UP or event.key == K_w:
                        if air_timer < 6:
                            vertical_momentum = -5

                if event.type == KEYUP:
                    if event.key == K_RIGHT or event.key == K_d:
                        moving_right = False
                    if event.key == K_LEFT or event.key == K_a:
                        moving_left = False
                    if event.key == K_SPACE:
                        if count_of_bullets > 0:

                            b = Bullet(int(player_rect.center[0] - scroll[0]), int(player_rect.center[1] - scroll[1]),
                                       player_rect, bullets_rects)
                            count_of_bullets -= 1
                            if moving_left:
                                bullets_left.add(b)
                            else:
                                bullets_right.add(b)

            show_count_of_bullets(count_of_bullets)

            if hp <= 0:
                gameplay = False

            portal.update(player_rect, key_blit)

            display.blit(portal.image, (portal.rect.x, portal.rect.y))

            if key.update(player_rect, is_key) == True:
                key_blit = False

            if key_blit:
                display.blit(key.image, (key.rect.x, key.rect.y))

            bullets_left.draw(display)
            bullets_left.update(bullet_rects, bullets_left, a_rects)

            bullets_right.draw(display)
            bullets_right.update(bullet_rects, bullets_right, a_rects)

            health.update(hp)
            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()
            clock.tick(60)
        else:
            restart_menu(start_lvl2_)


def start_parkour():
    bg = pygame.image.load("images/fon2.png").convert_alpha()
    bg_x = -500

    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0
    true_scroll = [0, 0]
    player_anim_count = 0
    game_map = load_map('map_for_parkour')
    moon_block = pygame.image.load('images/dirt.png')
    moon_sprite = pygame.sprite.Sprite()
    moon_sprite.image = moon_block
    player_rect = pygame.Rect( 35, 850, 35, 50)
    running = True
    gameplay = True
    game_music.play(-1)
    while running:
        if gameplay:
            pygame.mouse.set_visible(False)
            display.blit(pygame.transform.scale(bg, (1000, 500)), (bg_x, 0))
            true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 30
            true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 30
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            tile_rects = []
            y = 0
            for layer in game_map:
                x = 0
                for tile in layer:
                    if tile == '1':
                        display.blit(moon_block, (x * 30 - scroll[0], y * 30 - scroll[1]))
                        tile_rects.append(pygame.Rect(x * 30, y * 30, 30, 30))
                        moon_sprite.rect = pygame.Rect(x * 30, y * 30, 30, 30)
                        tiles_group.add(moon_sprite)
                    if tile == 'f':
                        f = Finish(x * 30 - scroll[0], y * 30 - scroll[1])
                        display.blit(f.image, (x * 30 - scroll[0], y * 30 - scroll[1] - 20))
                    x += 1
                y += 1

            display.blit(static, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

            player_movement = [0, 0]
            if moving_right == True:
                player_movement[0] += 2
                display.blit(walk_right[int(str(player_anim_count)[0])],
                             (player_rect.x - scroll[0], player_rect.y - scroll[1]))

            if moving_left == True:
                if player_rect.x >= 0:
                    player_movement[0] -= 2
                    display.blit(walk_left[int(str(player_anim_count)[0])],
                                 (player_rect.x - scroll[0], player_rect.y - scroll[1]))

            player_movement[1] += vertical_momentum
            vertical_momentum += 0.2
            if vertical_momentum > 5:
                vertical_momentum = 5

            if player_anim_count >= 3:
                player_anim_count = 0
            else:
                player_anim_count += 0.1

            player_rect, collisions = move(player_rect, player_movement, tile_rects)

            if collisions['bottom'] == True:
                air_timer = 0
                vertical_momentum = 0
            else:
                air_timer += 1

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT or event.key == K_d:
                        moving_right = True
                    if event.key == K_LEFT or event.key == K_a:
                        moving_left = True
                    if event.key == K_UP or event.key == K_w:
                        if air_timer < 6:
                            vertical_momentum = -5

                if event.type == KEYUP:
                    if event.key == K_RIGHT or event.key == K_d:
                        moving_right = False
                    if event.key == K_LEFT or event.key == K_a:
                        moving_left = False

            f.update(player_rect)

            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()
            clock.tick(60)
        else:
            restart_menu(start_lvl1_)


if __name__ == "__main__":
    start_lvl1_()
