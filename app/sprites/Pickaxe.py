import pygame
import os
from app.settings import *

class Pickaxe(pygame.sprite.Sprite):
    def __init__(self, x, y, player, nameImg='pickaxe.png'):
        super().__init__()

        self.player = player

        self.imageOrig = pygame.image.load(os.path.join('img', nameImg))
        self.imageOrig = pygame.transform.scale(self.imageOrig, (16, 16))
        # self.imageOrig = pygame.transform.rotate(self.imageOrig, -45)
        if self.player.facingSide is RIGHT:
            self.decaX = 13
        else:
            self.imageOrig = pygame.transform.flip(self.imageOrig, True, False)
            self.decaX = -13
        self.decaY = -7


        self.image = self.imageOrig
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


    def dead(self):
        pass

    def spring(self):
        pass

    def updatePickaxe(self):
        # mousePos = pygame.mouse.get_pos()
        #
        # diffx = mousePos[0]+self.mapData.cameraPlayer.view_rect.x-self.rect.centerx
        # diffy = mousePos[1]+self.mapData.cameraPlayer.view_rect.y-self.rect.centery
        #
        # self.target.rect.centerx = TARGET_DISTANCE*(diffx)/self.vectorNorm(diffx,diffy) + self.rect.centerx
        # self.target.rect.centery = TARGET_DISTANCE*(diffy)/self.vectorNorm(diffx,diffy) + self.rect.centery

        self.rect.centerx = self.player.rect.centerx + self.decaX
        self.rect.centery = self.player.rect.centery + self.decaY

        # self.target.powerx = (diffx)/self.vectorNorm(diffx,diffy)
        # self.target.powery = (diffy)/self.vectorNorm(diffx,diffy)
        #
        # angleRad = math.atan2(diffy, diffx)
        # self.target.image = pygame.transform.rotate(self.target.imageOrig, -angleRad/math.pi*180)