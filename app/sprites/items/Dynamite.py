__author__ = 'Bobsleigh'

import pygame
import os
from app.sprites.CollisionMask import CollisionMask
from ldLib.animation.Animation import Animation
from ldLib.tools.Cooldown import Cooldown
from app.settings import *

class Dynamite(pygame.sprite.Sprite):
    def __init__(self, x, y, mapData):
        super().__init__()

        self.imageOrig = pygame.image.load(os.path.join('img', 'dynamiteLvl1.png'))
        self.image = self.imageOrig

        self.imageList = []
        self.imageList.append(pygame.image.load(os.path.join('img', 'trempo2.png')))
        self.imageList.append(pygame.image.load(os.path.join('img', 'trempo1.png')))
        self.imageList.append(pygame.image.load(os.path.join('img', 'trempo3.png')))

        self.animation = Animation(self.image, self.imageList, 5)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.name = "Dynamite"

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

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width/2, self.rect.height)
        self.collisionMask.centerx = self.rect.centerx
        self.collisionMask.centery = self.rect.centery

        self.jumpState = 0
        self.explosionCooldown = Cooldown(30)
        self.explosionCooldown.start()

        self.mapData = mapData

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.collisionMask.rect.centerx = self.rect.centerx
        self.collisionMask.rect.centery = self.rect.centery

        self.explosionCooldown.update()
        if self.explosionCooldown.isZero:
            self.detonate()

    def detonate(self):
        tileWidth = self.mapData.tmxData.tilewidth
        tileHeight = self.mapData.tmxData.tileheight

        for i in range(-1,1):
            for j in range(-1,1):
                self.mapData.localTmxData.addTileXYToListToChange((self.rect.centerx - i * tileWidth, self.rect.centery - j * tileHeight), 0)
                self.mapData.localTmxData.addTileXYToListToChange((self.rect.centerx - i * tileWidth, self.rect.centery - j * tileHeight), 0, COLLISION_LAYER)
                self.mapData.localTmxData.changeAllTileInList(self.mapData.cameraPlayer)

        self.kill()


        pass