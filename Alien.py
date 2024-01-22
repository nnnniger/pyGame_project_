import pygame

# alien_walk_left = [
#     pygame.image.load("images/alien/alien_left/left1.png"),
#     pygame.image.load("images/alien/alien_left/left2.png"),
#     pygame.image.load("images/alien/alien_left/left3.png"),
#     pygame.image.load("images/alien/alien_left/left4.png")
#
# ]
#
# alien_walk_right = [
#     pygame.image.load("images/alien/alien_right/right1.png"),
#     pygame.image.load("images/alien/alien_right/right2.png"),
#     pygame.image.load("images/alien/alien_right/right3.png"),
#     pygame.image.load("images/alien/alien_right/right4.png")
# ]

alien_img = pygame.image.load("images/alien/alien_static.png")


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = alien_img
        self.none_image = pygame.image.load("images/none.png")
        # self.image_left = pygame.transform.flip(self.image, self.image.get_width(), 0)
        # self.image_right = self.image
        self.a_rects = [pygame.Rect(240, 340, 25, 40), pygame.Rect(716, 310, 35, 50), pygame.Rect(896, 310, 35, 50),
                        pygame.Rect(777, 130, 35, 50), pygame.Rect(659, 130, 35, 50), pygame.Rect(237, 40, 35, 50),
                        pygame.Rect(175, 40, 35, 50), pygame.Rect(1227, 370, 35, 50), pygame.Rect(1319, 370, 35, 50),
                        pygame.Rect(2006, 190, 35, 50), pygame.Rect(2096, 190, 35, 50), pygame.Rect(2007, 370, 35, 50),
                        pygame.Rect(2155, 370, 35, 50), ]
        # self.a_rect = pygame.Rect(240, 340, 25, 40)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.V = 4

        self.move_right = True
        self.move_left = False

        self.max_left_x = int(self.rect.x) - 30
        self.max_right_x = int(self.rect.x) + 30

    def update(self, player_rect, hp, bullet_rects, lsttt_of_aliens_coords, i):


        for rect in self.a_rects:
            if player_rect.colliderect(rect):
                print("collide with player")

        for rect in bullet_rects:
            for r in self.a_rects:
                if rect.colliderect(r):
                    self.image = self.none_image
                    bullet_rects.remove(rect)
                    self.a_rects.remove(r)
                    self.kill()
                    print("fall alien")
                    print(lsttt_of_aliens_coords.index(i))
                    # lsttt_of_aliens_coords.remove(lsttt_of_aliens_coords.index(i))


        return self.a_rects, bullet_rects, self.image, lsttt_of_aliens_coords

    # def update(self, scroll): [(6, 2), (8, 2), (22, 5), (26, 5), (67, 7), (70, 7), (24, 11), (30, 11), (8, 12), (41, 13), (44, 13), (67, 13), (72, 13)]
    #     # print(1)
    #     # self.rect.x -= scroll[0]
    #     # self.rect.y -= scroll[1]
    #     # self.rect.x += self.V
    #     if self.rect.x > self.max_right_x:
    #         self.image = self.image_left
    #         self.move_right = False
    #         self.move_left = True
    #     if self.rect.x < self.max_left_x:
    #         self.move_left = False
    #         self.move_right = True
    #         self.image = self.image_right
    #
    #     if self.move_right:
    #         self.rect.x += self.V
    #     else:
    #         self.rect.x -= self.V

# Aliens in
# <rect(769, 130, 35, 50)>
# <rect(673, 130, 35, 50)>
# <rect(255, 40, 35, 50)>
# <rect(177, 40, 35, 50)>
# <rect(710, 310, 35, 50)>
# <rect(898, 310, 35, 50)>
# <rect(1215, 370, 35, 50)>
# <rect(1874, 250, 35, 50)>
# <rect(1933, 370, 35, 50)>
# <rect(2029, 370, 35, 50)>
# <rect(2227, 370, 35, 50)>
# <rect(2065, 190, 35, 50)>
# <rect(2177, 190, 35, 50)>
# <rect(2283, 190, 35, 50)>
