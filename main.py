from pygame import QUIT
from story import *
from endless import *

pygame.init()
pygame.display.set_caption('Start menu')
WINDOW_SIZE = (1000, 700)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

white = (255, 255, 255)
purple_normal = (128, 0, 128)
purple_hover = (186, 85, 211)
border_color = (255, 255, 255, 5)

list_for_bg_images = []

for i in range(1, 201):
    list_for_bg_images.append(pygame.image.load(f'images/menu_bg/{i}.png'))


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

def start_screen():
    bg_x, bg_y = 0, 0
    bg_anim_count = 0

    while True:
        bg_image = list_for_bg_images[bg_anim_count % len(list_for_bg_images)]
        bg_image = pygame.transform.scale(bg_image, WINDOW_SIZE)

        screen.blit(bg_image, (bg_x, bg_y))
        bg_anim_count += 1

        draw_button(435, 255, 130, 70, purple_normal, purple_hover, "Story", start_lvl1)
        draw_button(410, 355, 180, 70, purple_normal, purple_hover, "Endless", start_endless)

        for event in pygame.event.get():  # отслеживаний действий игрока
            if event.type == QUIT:
                terminate()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    start_screen()
