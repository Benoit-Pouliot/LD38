__author__ = 'Bobsleigh'

__author__ = 'Bobsleigh'

import pygame
import os
from app.settings import *

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, nameImg='pig.png'):
        super().__init__()

        self.imageOrig = pygame.image.load(os.path.join('img', nameImg))
        self.imageOrig = pygame.transform.scale(self.imageOrig, (16, 16))
        self.imageOrig = pygame.transform.rotate(self.imageOrig, -45)
        self.image = self.imageOrig
        self.name = "target"

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speedx = 0
        self.speedy = 0

        self.isPhysicsApplied = False
        self.isGravityApplied = False
        self.isFrictionApplied = False
        self.isCollisionApplied = False

        self.powerx = 0
        self.powery = 0

    def dead(self):
        pass

    def spring(self):
        pass