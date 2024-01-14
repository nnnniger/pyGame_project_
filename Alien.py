import pygame

alien_walk_left = [
    pygame.image.load("images/alien/alien_left/left1.png"),
    pygame.image.load("images/alien/alien_left/left2.png"),
    pygame.image.load("images/alien/alien_left/left3.png"),
    pygame.image.load("images/alien/alien_left/left4.png")

]

alien_walk_right = [
    pygame.image.load("images/alien/alien_right/right1.png"),
    pygame.image.load("images/alien/alien_right/right2.png"),
    pygame.image.load("images/alien/alien_right/right3.png"),
    pygame.image.load("images/alien/alien_right/right4.png")
]



class Alien(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = alien_walk_right[0]
        self.image_left = pygame.transform.flip(self.image, self.image.get_width(), 0)
        self.image_right = self.image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.V = 4

        self.move_right = True
        self.move_left = False

        self.max_left_x = int(self.rect.x) - 30
        self.max_right_x = int(self.rect.x) + 30

    def update(self, scroll):
        # print(1)
        # self.rect.x -= scroll[0]
        # self.rect.y -= scroll[1]
        # self.rect.x += self.V
        if self.rect.x > self.max_right_x:
            self.image = self.image_left
            self.move_right = False
            self.move_left = True
        if self.rect.x < self.max_left_x:
            self.move_left = False
            self.move_right = True
            self.image = self.image_right

        if self.move_right:
            self.rect.x += self.V
        else:
            self.rect.x -= self.V


# Aliens in
# <rect(1199, 370, 35, 50)>
# <rect(1213, 370, 35, 50)>
# <rect(2129, 190, 35, 50)>
# <rect(2149, 190, 35, 50)>
# <rect(2187, 190, 35, 50)>
# <rect(2030, 370, 35, 50)>
# <rect(2056, 370, 35, 50)>
# <rect(2090, 370, 35, 50)>
# <rect(750, 130, 35, 50)>
# <rect(648, 130, 35, 50)>
# <rect(180, 40, 35, 50)>





