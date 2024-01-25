import pygame

alien_img = pygame.image.load("images/alien/alien_static.png")


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = alien_img
        self.none_image = pygame.image.load("images/none.png")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player_rect, hp, bullet_rects, lst_of_aliens_coords, i, a_rects):
        for rect in a_rects:
            if player_rect.colliderect(rect):
                hp -= 1

        for rect in bullet_rects:
            for r in a_rects:
                if rect.colliderect(r):
                    lst_of_aliens_coords = lst_of_aliens_coords[1::]
                    print(i)
                    self.image = self.none_image
                    bullet_rects.remove(rect)

                    a_rects.remove(r)
                    print("fall alien")

        return bullet_rects, lst_of_aliens_coords, hp
