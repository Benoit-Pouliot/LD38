import pygame
import os

from app.sprites.CollisionMask import CollisionMask
from ldLib.tools.Animation import Animation
from app.settings import *

class Seller(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.name = "vendor"
        self.image = pygame.image.load(os.path.join('img', 'vendor.png'))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.speedx = 0
        self.speedy = 0

        # Needed to handle collisions...
        self.isGravityApplied = True
        self.isPhysicsApplied = False
        self.isCollisionApplied = True
        self.jumpState = JUMP

        # For animation purpose, sete multiple image
        self.frames = [self.image]
        self.animation = Animation(self, self.frames, -1)
        image1 = self.image
        image2 = pygame.image.load(os.path.join('img', 'vendorWink.png'))
        image3 = pygame.image.load(os.path.join('img', 'vendorFlip.png'))
        image4 = pygame.image.load(os.path.join('img', 'vendorWinkFlip.png'))


        self.animation.setAnimation([image1, image1,image2, image1,image3, image3,image4,image3], 30)

    def update(self):
        self.animation.update(self)
        self.collisionMask.rect = self.rect

        self.rect.x += self.speedx
        self.rect.y += self.speedy