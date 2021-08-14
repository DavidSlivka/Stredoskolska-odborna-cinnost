import pygame
import random
import os
import neat
import csv
import pandas as pd
from matplotlib import pyplot as plt


pygame.font.init()
pygame.init()
clock = pygame.time.Clock()
plt.style.use('ggplot')

WIDTH = 300
HEIGHT = 500
GROUND = int(HEIGHT*0.9)
generation = 0

BIRD_IMGS = [pygame.image.load(os.path.join('imgs', 'BIRD-1.png')), pygame.image.load(os.path.join('imgs', 'BIRD-2.png')),
             pygame.image.load(os.path.join('imgs', 'BIRD-3.png')), pygame.image.load(os.path.join('imgs', 'BIRD-2.png'))]

PIPE_BOTTOM = pygame.image.load(os.path.join('imgs', 'PIPE-img.png'))
PIPE_TOP = pygame.image.load(os.path.join('imgs', 'PIPE-top.png'))

BASE_IMG = pygame.image.load(os.path.join('imgs', 'BASE-img.png'))

BG_IMG = pygame.image.load(os.path.join('imgs', 'BG-img.png'))
BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))

FONT = pygame.font.SysFont('Cooper black', 35)
file = 'score.csv'

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
