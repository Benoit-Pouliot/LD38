import os
import pygame

from app.settings import *
from ldLib.GUI.messageBox.MessageBox import MessageBox

class WinZone(pygame.sprite.Sprite):
    def __init__(self,data):
        super().__init__()

        self.image = pygame.Surface([SCREEN_WIDTH*4/5, SCREEN_WIDTH*2/5], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH/10
        self.rect.y = SCREEN_HEIGHT/10


        self.mapData = data

        message = 'You got to the bottom! You win the game!'
        self.createWinBox(SCREEN_WIDTH/2-200, SCREEN_HEIGHT/2-150, 400, 100, message)

    def update(self):
        pass

    def createWinBox(self,x,y,width,height, message):
        self.textWin = MessageBox(x,y,width,height)
        self.textWin.textList.append(message)
        self.textWin.isPhysicsApplied = False
        self.textWin.isCollisionApplied = False

        self.mapData.winGroup.add(self.textWin)