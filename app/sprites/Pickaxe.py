import pygame
import os
from app.settings import *

class Pickaxe(pygame.sprite.Sprite):
    def __init__(self, x, y, player, lvlPickaxe=1):
        super().__init__()

        self.player = player

        if lvlPickaxe == 1:
            nameImg = 'pickaxe.png'
        elif lvlPickaxe == 2:
            nameImg = 'pickaxeLvl2.png'
        elif lvlPickaxe == 3:
            nameImg = 'pickaxeLvl3.png'


        self.imageOrig = pygame.image.load(os.path.join('img', nameImg))
        self.imageOrig = pygame.transform.scale(self.imageOrig, (16, 16))
        # self.imageOrig = pygame.transform.rotate(self.imageOrig, -45)
        self.decaX = []
        self.decaY = []
        if self.player.facingSide is RIGHT:
            self.decaX = [0, 13, 15, 13]
            self.angle = [45, 0, -45, -70]
        else:
            self.imageOrig = pygame.transform.flip(self.imageOrig, True, False)
            self.decaX = [0, -13, -15, -13]
            self.angle = [-45, 0, 45, 70]
        self.decaY = [-14, -3, 5, 15]
        self.image = pygame.transform.rotate(self.imageOrig, self.angle[0])

        self.name = "pickaxe"

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

        self.iter = 2
        self.iterChange = self.player.imageDigWaitNextImage
        self.iterState = 0
        self.iterStateMax = len(self.decaX)


    def dead(self):
        pass

    def spring(self):
        pass

    def updatePickaxe(self):

        self.iter = self.iter+1
        if self.iter > self.iterChange:
            self.iterState = (self.iterState+1) % self.iterStateMax
            self.image = pygame.transform.rotate(self.imageOrig, self.angle[self.iterState])
            self.iter = 0

        self.rect.centerx = self.player.rect.centerx + self.decaX[self.iterState]
        self.rect.centery = self.player.rect.centery + self.decaY[self.iterState]

