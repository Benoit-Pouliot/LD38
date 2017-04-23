__author__ = 'Bobsleigh'

__author__ = 'Bobsleigh'

import pygame
import os

class RedTileMask(pygame.sprite.Sprite):
    def __init__(self, x, y, life, maxLife):
        super().__init__()

        self.surface = pygame.Surface((32, 32))
        self.surface.fill((255,0,0))
        self.surface.set_alpha(255 - life * (255/maxLife))
        self.image = self.surface

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.name = "RedTileMask"

        self.life = life
        self.maxLife = maxLife

        self.isPhysicsApplied = False
        self.isGravityApplied = False
        self.isFrictionApplied = False
        self.isCollisionApplied = False

        # self.speedx = 0
        # self.speedy = 0
        # self.maxSpeedx = 5
        # self.maxSpeedyUp = 18
        # self.maxSpeedyDown = 15
        # self.maxSpeedyUpClimbing = 6
        # self.maxSpeedyDownClimbing = 6
        # self.accx = 2
        # self.accy = 2

        # self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width/2, self.rect.height)
        # self.collisionMask.centerx = self.rect.centerx
        # self.collisionMask.centery = self.rect.centery
        #
        # self.jumpState = 0

