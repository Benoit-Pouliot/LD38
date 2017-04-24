__author__ = 'Bobsleigh'

import pygame
import os
from app.settings import *
from ldLib.tools.Counter import Counter
from app.sprites.CollisionMask import CollisionMask

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, dmg=5, friendly=True):
        super().__init__()

        self.name = "explosion"

        self.frames = []

        for versionNum in range(1,4):
            self.frames.append(pygame.image.load(os.path.join('img', 'explosion_v' + str(versionNum) + '.png')))

        self.image = self.frames[0]

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 0
        self.speedy = 0

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, 60, 60)

        self.friendly = friendly
        self.isPhysicsApplied = False
        self.isGravityApplied = False
        self.isFrictionApplied = False
        self.isCollisionApplied = False

        self.jumpState = JUMP

        self.facingSide = RIGHT

        self.counter = Counter()
        self.duration = 25  #In frames

        self.attackDMG = dmg


    def update(self):
        self.counter.count()

        if self.counter.value >= 2*self.duration/3 :

            x = self.rect.centerx
            y = self.rect.centery
            self.image = self.frames[2]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y

        elif self.counter.value >= self.duration/3 :
            x = self.rect.centerx
            y = self.rect.centery
            self.image = self.frames[1]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y

        if self.counter.value >= self.duration:
            self.kill()

    def detonate(self):
        pass

    def dead(self):
        pass

    def spring(self):
        pass