import pygame
import os
from app.settings import *
from app.sprites.GUI.HUDStuff.StatDisplay import StatDisplay


class HUD(pygame.sprite.Sprite):
    def __init__(self,data):
        super().__init__()

        self.data = data

        self.fontSize = HUD_FONT_SIZE
        self.HUDfont = pygame.font.SysFont(FONT_NAME, self.fontSize)

        self.image = pygame.Surface((SCREEN_WIDTH, HUD_HEIGHT))
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0

        self.borderHUD = 5

        self.interior = pygame.Rect(0, 0, self.rect.width,
                                    self.rect.height -  self.borderHUD)
        self.color1 = HUD_COLOR_1
        self.color2 = HUD_COLOR_2

        self.fontSize = HUD_FONT_SIZE
        self.HUDFont = pygame.font.SysFont(FONT_NAME, self.fontSize)

        self.moneyLabel = StatDisplay(self.image,(SCREEN_WIDTH* 0.8, 5),self.HUDFont, 'Gems')
        self.ladderLabel = StatDisplay(self.image,(SCREEN_WIDTH* 0.1, 5),self.HUDFont, 'Ladder')
        self.springLabel = StatDisplay(self.image,(SCREEN_WIDTH* 0.3, 5),self.HUDFont, 'Spring')
        self.antiGravityLabel = StatDisplay(self.image,(SCREEN_WIDTH* 0.5, 5),self.HUDFont, 'Anti-gravity')


    def update(self):
        self.image.fill(self.color2)
        self.image.fill(self.color1, self.interior)

        self.updateMoney()
        self.updateSpring()
        self.updateLadder()
        self.updateAntiGravity()

    def updateMoney(self):
        self.moneyLabel.stat = str(self.data.money)
        self.moneyLabel.printText()

    def updateSpring(self):
        self.springLabel.stat = str(self.data.nbSpring)
        self.springLabel.printText()

    def updateLadder(self):
        self.ladderLabel.stat = str(self.data.nbLadder)
        self.ladderLabel.printText()

    def updateAntiGravity(self):
        self.antiGravityLabel.stat = str(self.data.nbAntiGravity)
        self.antiGravityLabel.printText()
