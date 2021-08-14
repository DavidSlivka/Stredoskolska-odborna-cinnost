from settings import *


class Base:
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.VEL = 7
        self.WIDTH = BASE_IMG.get_width()
        self.x2 = self.WIDTH
        self.IMG = BASE_IMG

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self):
        screen.blit(self.IMG, (self.x1, self.y))
        screen.blit(self.IMG, (self.x2, self.y))