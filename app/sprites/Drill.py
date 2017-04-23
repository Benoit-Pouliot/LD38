import pygame
import os
from app.settings import *

class Drill(pygame.sprite.Sprite):
    def __init__(self, x, y, player, lvlDrill=1):
        super().__init__()

        self.player = player

        if lvlDrill == 1:
            name1 = 'drillLvl1-a.png'
            name2 = 'drillLvl1-b.png'
        elif lvlDrill == 2:
            name1 = 'drillLvl2-a.png'
            name2 = 'drillLvl2-b.png'
        elif lvlDrill == 3:
            name1 = 'drillLvl3-a.png'
            name2 = 'drillLvl3-b.png'
        self.imageOrig = list()
        self.imageOrig.append(pygame.image.load(os.path.join('img', name1)))
        self.imageOrig.append(pygame.image.load(os.path.join('img', name2)))
        # self.imageOrig = pygame.transform.scale(self.imageOrig, (32, 32))

        self.decaX = []
        self.decaY = []
        if self.player.facingSide is RIGHT:
            self.decaX = [15, 13, 15, 17]
        else:
            self.imageOrig[0] = pygame.transform.flip(self.imageOrig[0], True, False)
            self.imageOrig[1] = pygame.transform.flip(self.imageOrig[1], True, False)
            self.decaX = [-15, -13, -15, -17]
        self.decaY = [3, 5, 1, 3]

        self.image = self.imageOrig[0]

        self.name = "drill"

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

        self.iter = 0
        self.iterChange = self.player.imageDigWaitNextImage/3
        self.iterState = 0
        self.iterStateMax = len(self.imageOrig)


    def dead(self):
        pass

    def spring(self):
        pass

    def updateDrill(self):


        self.iter = self.iter+1
        if self.iter > self.iterChange:
            self.iterState = (self.iterState+1) % self.iterStateMax
            self.iter = 0
            self.image = self.imageOrig[self.iterState]

        self.rect.centerx = self.player.rect.centerx + self.decaX[self.iterState]
        self.rect.centery = self.player.rect.centery + self.decaY[self.iterState]

