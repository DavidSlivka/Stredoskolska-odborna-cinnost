from settings import *


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.BOTTOM_PIPE = PIPE_BOTTOM
        self.TOP_PIPE = PIPE_TOP
        self.GAP = int(HEIGHT*0.25)
        self.VEL = 7
        self.passed = False
        self.set_height()

    def move(self):
        self.x -= self.VEL

    def set_height(self):
        # calculates a height of pipe from range 50 to 300
        self.height = random.randrange(int(HEIGHT*0.1), int(HEIGHT-(HEIGHT*0.1+HEIGHT-GROUND+self.GAP)))
        # calculates position of top & bottom pipe
        self.bottom = self.height + self.GAP
        self.top = self.height - self.TOP_PIPE.get_height()

    def get_top_mask(self):
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        return top_mask

    def get_bottom_mask(self):
        bottom_mask = pygame.mask.from_surface(self.BOTTOM_PIPE)
        return bottom_mask

    def draw(self):
        screen.blit(self.TOP_PIPE, (self.x, self.top))
        screen.blit(self.BOTTOM_PIPE, (self.x, self.bottom))
