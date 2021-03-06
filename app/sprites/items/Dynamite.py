__author__ = 'Bobsleigh'

import pygame
import os
from app.sprites.CollisionMask import CollisionMask
from ldLib.animation.Animation import Animation
from ldLib.tools.Cooldown import Cooldown
from app.settings import *
from random import randint
from app.sprites.Explosion import Explosion

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

        self.isPhysicsApplied = True
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
        self.explosionCooldown = Cooldown(60)
        self.explosionCooldown.start()

        self.mapData = mapData

        # Sounds
        self.dictSound = {'explosion': pygame.mixer.Sound(os.path.join('music', 'ExplosionDynamite.wav'))}
        # quick set up of volume
        for key in self.dictSound:
            self.dictSound[key].set_volume(.3)

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

        if not self.mapData.player.musicMuted:
            self.dictSound['explosion'].play(0)

        for j in range(-2,3):
            for i in range(-2,3):
                if (i == -2 or j == 2 or i == 2 or j == -2):
                    a = randint(1,3)
                    if a == 2:
                        self.mapData.localTmxData.addTileXYToListToChange((self.rect.centerx - i * tileWidth, self.rect.centery - j * tileHeight), 0)
                        self.mapData.localTmxData.addTileXYToListToChange((self.rect.centerx - i * tileWidth, self.rect.centery - j * tileHeight), 0, COLLISION_LAYER)
                        self.mapData.player.destroyRedTile((self.rect.centerx - i * tileWidth)//self.mapData.tmxData.tilewidth, (self.rect.centery - j * tileHeight)//self.mapData.tmxData.tileheight)
                else:
                    self.mapData.localTmxData.addTileXYToListToChange((self.rect.centerx - i * tileWidth, self.rect.centery - j * tileHeight), 0)
                    self.mapData.localTmxData.addTileXYToListToChange((self.rect.centerx - i * tileWidth, self.rect.centery - j * tileHeight), 0, COLLISION_LAYER)
                    self.mapData.player.destroyRedTile((self.rect.centerx - i * tileWidth)//self.mapData.tmxData.tilewidth, (self.rect.centery - j * tileHeight)//self.mapData.tmxData.tileheight)

        self.mapData.localTmxData.changeAllTileInList(self.mapData.cameraPlayer)

        explosion = Explosion(self.rect.midbottom[0], self.rect.midbottom[1], 1)

        self.mapData.camera.add(explosion)
        self.mapData.allSprites.add(explosion)

        self.kill()
