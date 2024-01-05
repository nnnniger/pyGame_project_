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
        self.image = alien_walk_left[0]
        self.rect = self.image.get_rect()
        self.speed = 3
        self.rect.x = x
        self.rect.y = y
        self.alien_movement = [0, 0]

    def update(self):
        self.rect.x += self.speed
        # # x, y, w, h = self.rect
        # # if x > screen.get_width() - self.image.get_width():
        # #     self.image = self.image_left
        # #     self.right = False
        # # if x < 0:
        # #     self.right = True
        # #     self.image = self.image_right
        #
        # if self.right:
        #     self.alien_movement[0] += 5
        # else:
        #     self.alien_movement[0] -= 5
        #
        # if self.alien_collisions['bottom'] == True:
        #     print("botommmm")
        #
        # # if self.right:
        # #     self.rect = self.rect.move(20, 0)
        # # else:
        # #     self.rect = self.rect.move(-20, 0)





