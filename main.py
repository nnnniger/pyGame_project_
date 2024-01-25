from finish import *
from story import *

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

for i in range(1, 201):
    list_for_bg_images.append(pygame.image.load(f'images/menu_bg/{i}.png'))


def yes_action():
    terminate()


def no_action():
    is_quit = False
    start_screen()


def quit():
    screen.fill((0, 0, 0))
    show_text("Are you sure to exit?", 48, width // 2 - 185, height // 3)
    draw_button(300, 400, 100, 70, purple_normal, purple_hover, "Yes", yes_action)
    draw_button(550, 400, 90, 70, purple_normal, purple_hover, "No", no_action)
    if pygame.mouse.get_focused():
        cursor.update()
        cursor.draw(screen)


def start_screen():
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

        draw_button(435, 255, 130, 70, purple_normal, purple_hover, "Story", start_lvl1_)
        draw_button(410, 355, 180, 70, purple_normal, purple_hover, "Parkour", start_parkour)

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
    start_screen()
