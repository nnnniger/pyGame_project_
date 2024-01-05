import pygame, sys
from pygame.locals import *
from Alien import Alien
from load_func import load_map

pygame.init()
pygame.display.set_caption ('Pygame Platformer')
WINDOW_SIZE = (1000, 700)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((500, 350))
clock = pygame.time.Clock()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.flip_image = pygame.image.load("images/bullet_flip.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self in bullets_right:
            self.rect.x += 4
        else:
            self.image = self.flip_image
            self.rect.x -= 4


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
static = pygame.image.load("images/astronaut/static.png")

bullets_left = pygame.sprite.Group()
bullets_right = pygame.sprite.Group()
aliens = pygame.sprite.Group()

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

    x += 10
    y += 10
    size = 50
    font = pygame.font.SysFont(None, size)
    text_render = font.render(text, True, text_color)
    screen.blit(text_render, (x, y))

def restart_menu(action):
    while True:
        screen.fill((0, 0, 0))
        create_restart_button(action)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

def collision_test(rect, tiles):  # функция, считывающая соприкосновения
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):  # функция изменения координат
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

def start_lvl1():
    bg = pygame.image.load("images/fon2.png").convert_alpha()
    bg_x = -500

    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0

    true_scroll = [0, 0]

    player_anim_count = 0

    game_map = load_map('map2')  # Считываем карту из файла map.txt
    moon_block = pygame.image.load('dirt.png')  # блок замка

    player_rect = pygame.Rect(100, 220, 35, 50)
    player_x, player_y = player_rect.x, player_rect.y

    running = True
    gameplay = True
    while running:
        if gameplay:# game loop
            display.blit(pygame.transform.scale(bg, (1000, 500)), (bg_x, 0))
            true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 30
            true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 30
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            # bullet_x, bullet_y = player_rect.center[0], player_rect.center[1]
            # bullet_rect = pygame.Rect(bullet_x, bullet_y, 14, 7)
            # фон

            tile_rects = []
            y = 0
            for layer in game_map:
                x = 0
                for tile in layer:
                    if tile == '1':
                        # print(1)
                        display.blit(moon_block, (x * 30 - scroll[0], y * 30 - scroll[1]))
                    if tile == 'a':
                        a = Alien(aliens, x * 30 - scroll[0], y * 30 - 5 - scroll[1])
                    if tile != '0':
                        tile_rects.append(pygame.Rect(x * 30, y * 30, 30, 30))
                    x += 1
                y += 1

            display.blit(a.image, (a.rect[0], a.rect[1]))

            display.blit(static, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
            player_movement = [0, 0]
            if moving_right == True:
                player_movement[0] += 2
                display.blit(walk_right[int(str(player_anim_count)[0])], (player_rect.x - scroll[0], player_rect.y - scroll[1]))

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

            if player_rect.y >= 599:
                gameplay = False

            for event in pygame.event.get():  # отслеживаний действий игрока
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
                        b = Bullet(int(player_rect.center[0] - scroll[0]), int(player_rect.center[1] - scroll[1]))
                        if moving_left:
                            bullets_left.add(b)

                        else:
                            bullets_right.add(b)

            # aliens.update()
            # aliens.draw(display)
            # print(aliens)

            bullets_left.draw(display)
            bullets_left.update()

            bullets_right.draw(display)
            bullets_right.update()

            a.update()

            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()
            clock.tick(60)
        else:
            restart_menu(start_lvl1)
