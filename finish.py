import sys
import pygame
from pygame import QUIT


pygame.init()
pygame.display.set_caption('Legend of Battles: Pixel Battle in Space')
WINDOW_SIZE = width, height = (1000, 700)
screen = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()

white = (255, 255, 255)
purple_normal = (128, 0, 128)
purple_hover = (186, 85, 211)
border_color = (255, 255, 255, 5)

list_for_bg_images = []

for i in range(1, 137):
    list_for_bg_images.append(pygame.image.load(f'images/dikaprio.gif/anim ({i}).png'))


def terminate():
    pygame.quit()
    sys.exit()


def show_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, white)
    screen.blit(text_surface, (x, y))


def draw_button(x, y, width, height, color_normal, color_hover, text, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, color_hover, (x, y, width, height))
        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, color_normal, (x, y, width, height))

    pygame.draw.rect(screen, border_color, (x, y, width, height), 7)
    show_text(text, 50, x + 20, y + 20)


def yes_action():
    terminate()


def no_action():
    is_quit = False
    finish()


def quit():
    screen.fill((0, 0, 0))
    show_text("Are you sure to exit?", 48, width // 2 - 185, height // 3)
    draw_button(300, 400, 100, 70, purple_normal, purple_hover, "Yes", yes_action)
    draw_button(550, 400, 90, 70, purple_normal, purple_hover, "No", no_action)
    if pygame.mouse.get_focused():
        cursor.update()
        cursor.draw(screen)


def get_mouse_pos(mouse_pos):
    cursor_sprite.rect.x = mouse_pos[0]
    cursor_sprite.rect.y = mouse_pos[1]


cursor = pygame.sprite.Group()
cursor_sprite = pygame.sprite.Sprite()
cursor_sprite.image = pygame.image.load("images/cursor.png")
cursor_sprite.rect = cursor_sprite.image.get_rect()

cursor.add(cursor_sprite)


def finish():
    bg_x, bg_y = 0, 0
    bg_anim_count = 0

    is_quit = None

    while True:
        pygame.mouse.set_visible(False)
        # print(is_quit)
        bg_image = list_for_bg_images[bg_anim_count % len(list_for_bg_images)]
        bg_image = pygame.transform.scale(bg_image, WINDOW_SIZE)

        screen.blit(bg_image, (bg_x, bg_y))
        bg_anim_count += 1

        show_text("Congratulations, you've won!", 59, 220, height // 3)
        if pygame.mouse.get_focused():
            cursor.update()
            cursor.draw(screen)

        if is_quit == True:
            quit()

        for event in pygame.event.get():
            if event.type == QUIT:
                is_quit = True
            if event.type == pygame.MOUSEMOTION:
                get_mouse_pos(event.pos)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    finish()
