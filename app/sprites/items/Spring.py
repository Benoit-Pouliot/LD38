__author__ = 'Bobsleigh'

import pygame
import os
from app.sprites.CollisionMask import CollisionMask

class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.imageOrig = pygame.image.load(os.path.join('img', 'trempo1.png'))
        self.image = self.imageOrig

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.name = "Spring"

        self.isPhysicsApplied = False
        self.isGravityApplied = True
        self.isFrictionApplied = True
        self.isCollisionApplied = True

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 5
        self.maxSpeedyUp = 18
        self.maxSpeedyDown = 15
        self.maxSpeedyUpClimbing = 6
        self.maxSpeedyDownClimbing = 6
        self.accx = 2
        self.accy = 2

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.jumpState = 0
        self.bounceSpeed = 20

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.collisionMask.rect.x = self.rect.x
        self.collisionMask.rect.y = self.rect.y

    def bounce(self):
        pass