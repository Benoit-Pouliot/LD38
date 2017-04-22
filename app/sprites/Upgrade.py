import pygame
import os

from app.settings import *

class Upgrade(pygame.sprite.Sprite):
    def __init__(self, key,imageName, method,cost):
        super().__init__()

        self.key = key
        self.method = method
        self.cost = cost

        self.fontSize = 20
        self.upgFont = pygame.font.SysFont(FONT_NAME, self.fontSize)

        self.width = UPGRADE_SIZE
        self.height = UPGRADE_SIZE

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

        self.borderButton = 3

        self.interior = pygame.Rect(self.borderButton,self.borderButton,self.width-2*self.borderButton,self.height-2*self.borderButton)


        self.icon = pygame.image.load(os.path.join('img', imageName+'.png'))
        self.resizeIcon()
        self.iconPos = [0, 0]

        self.textCost = str(self.cost)
        self.textCostPos = [0, 0]

        self.isSelected = False

        # Color
        self.color1 = COLOR_MENU_1
        self.color2 = COLOR_MENU_2

    def update(self):

        if self.isSelected:
            self.color1 = COLOR_MENU_SELECT_1
            self.color2 = COLOR_MENU_SELECT_2
            self.printedCost = self.upgFont.render(self.textCost, True, COLOR_MENU_FONTS_SELECT)

        else:
            self.color1 = COLOR_MENU_1
            self.color2 = COLOR_MENU_2
            self.printedCost = self.upgFont.render(self.textCost, True, COLOR_MENU_FONTS)

        self.setUpgradeSpec()

        self.image.fill(self.color2)
        self.image.fill(self.color1,self.interior)
        self.image.blit(self.icon, self.iconPos)

        self.image.blit(self.printedCost,self.textCostPos)

 #blabla

    def setUpgradeSpec(self):
        self.textCost = str(self.cost)

        # Button real space
        self.textCostPos = [(self.image.get_width()-self.printedCost.get_width())/2,self.interior.bottom-1.5*self.fontSize]

        self.iconPos = [(self.image.get_width()-self.icon.get_width())/2, (self.image.get_height()*0.75 - self.icon.get_height()) * 0.5]

    def notify(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE_LEFT:
                if self.rect.collidepoint(event.pos):
                    self.method()

    def resizeIcon(self):
        resizeSizeX = 48
        imageSizeY = self.icon.get_height() * resizeSizeX / self.icon.get_width()

        self.icon = pygame.transform.scale(self.icon, (int(resizeSizeX), int(imageSizeY)))

    def useItem(self):
        # self.soundSelect.play(0)
        self.method()