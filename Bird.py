from settings import *


class Bird:
    def __init__(self):
        self.x = WIDTH//4
        self.y = HEIGHT//2
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.img_count = 0
        self.img = BIRD_IMGS[0]
        self.gravity = 10
        self.MAX_ROT = 20
        self.ROT_VEL = 15
        self.ANIM_TIME = 5
        self.ANIM_EPOCH = 20

    def jump(self):
        self.vel = -9
        self.tick_count = 0

    def draw(self):
        self.img_count += 1
        self.img_count %= self.ANIM_EPOCH
        self.img = BIRD_IMGS[int(self.img_count/self.ANIM_TIME)]

        if self.tilt <= -70:
            self.img = BIRD_IMGS[1]

        # rotates a bird image
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(int(self.x), int(self.y))).center)
        screen.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def move(self):
        self.tick_count += 1

        shift = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if shift >= self.gravity:
            shift = self.gravity

        if shift < 0:
            shift -= 2

        self.y += shift

        # tilting the bird
        if shift < 0 or self.y < self.y + 30:
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT
        else:
            if self.tilt >= -90:
                self.tilt -= self.ROT_VEL
