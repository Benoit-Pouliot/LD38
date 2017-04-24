import pygame
import os
from app.settings import *
from app.sprites.GUI.HUDStuff.ImageDisplay import ImageDisplay
from app.sprites.GUI.HUDStuff.ItemQtyDisplay import ItemQtyDisplay
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

        self.activeLeftItemLabel = ImageDisplay(self.image,(SCREEN_WIDTH* 0.05, 5),self.HUDFont, 'Left: ')
        self.activeRightItemLabel = ImageDisplay(self.image, (SCREEN_WIDTH * 0.15, 5), self.HUDFont, 'Right: ')

        self.dynamiteLabel = ItemQtyDisplay(self.image, (SCREEN_WIDTH * 0.39, 5), self.HUDFont, 'dynamiteLvl1')
        self.ladderLabel = ItemQtyDisplay(self.image,(SCREEN_WIDTH* 0.51, 5),self.HUDFont, 'ladder')
        self.springLabel = ItemQtyDisplay(self.image,(SCREEN_WIDTH* 0.61, 5),self.HUDFont, 'trempoHUD')

        # TODO: REMOVE ANTI-GRAVITY
        self.antiGravityLabel = ItemQtyDisplay(self.image,(SCREEN_WIDTH* 0.75, 5),self.HUDFont, 'antiGravity')

        self.moneyLabel = StatDisplay(self.image,(SCREEN_WIDTH* 0.85, 5),self.HUDFont, 'Gems')



    def update(self):
        self.image.fill(self.color2)
        self.image.fill(self.color1, self.interior)

        self.setActiveItem()
        self.updateDynamite()
        self.updateMoney()
        self.updateSpring()
        self.updateLadder()

        # TODO: REMOVE ANTI-GRAVITY
        self.updateAntiGravity()

    def setActiveItem(self):
        imageName = 'pig'
        leftMode = self.data.player.LeftClickMode
        rightMode = self.data.player.RightClickMode

        if leftMode == PLAYER_DIG_MODE:
            lvlPickaxe = self.data.lvlPickaxe
            if lvlPickaxe == 1:
                imageName = 'pickaxe'
            elif lvlPickaxe == 2:
                imageName = 'pickaxeLvl2'
            elif lvlPickaxe == 3:
                imageName = 'pickaxeLvl3'
        elif leftMode == PLAYER_DRILL_MODE:
            lvlPickaxe = self.data.lvlDrill
            if lvlPickaxe == 1:
                imageName = 'drillLvl1-a'
            elif lvlPickaxe == 2:
                imageName = 'drillLvl2-a'
            elif lvlPickaxe == 3:
                imageName = 'drillLvl3-a'
        self.activeLeftItemLabel.display(imageName)

        if rightMode == PLAYER_DYNAMITE_MODE:
            imageName = 'dynamiteLvl1'
        elif rightMode == PLAYER_LADDER_MODE:
            imageName = 'ladder'
        elif rightMode == PLAYER_SPRING_MODE:
            imageName = 'trempoHud'
        elif rightMode == PLAYER_ANTI_MODE:
            imageName = 'antiGravity'
        self.activeRightItemLabel.display(imageName)

    def updateDynamite(self):
        self.dynamiteLabel.stat = str(self.data.lvlDynamite)
        self.dynamiteLabel.display()

    def updateMoney(self):
        self.moneyLabel.stat = str(self.data.money)
        self.moneyLabel.printText()

    def updateSpring(self):
        self.springLabel.stat = str(self.data.nbSpring)
        self.springLabel.display()

    def updateLadder(self):
        self.ladderLabel.stat = str(self.data.nbLadder)
        self.ladderLabel.display()

    def updateAntiGravity(self):
        self.antiGravityLabel.stat = str(self.data.nbAntiGravity)
        self.antiGravityLabel.display()
