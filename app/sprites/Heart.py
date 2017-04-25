__author__ = 'Bobsleigh'

import pygame
import os
from app.sprites.CollisionMask import CollisionMask
from ldLib.animation.Animation import Animation

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.imageOrig = pygame.image.load(os.path.join('img', 'heart.png'))
        self.image = self.imageOrig

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.name = "Heart"

        self.isPhysicsApplied = False
        self.isGravityApplied = False
        self.isFrictionApplied = False
        self.isCollisionApplied = False

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 5
        self.maxSpeedyUp = 18
        self.maxSpeedyDown = 15
        self.maxSpeedyUpClimbing = 6
        self.maxSpeedyDownClimbing = 6
        self.accx = 2
        self.accy = 2

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width/2, self.rect.height)
        self.collisionMask.centerx = self.rect.centerx
        self.collisionMask.centery = self.rect.centery

        self.jumpState = 0





