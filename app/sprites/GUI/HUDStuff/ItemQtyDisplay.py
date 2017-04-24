import os
import pygame

from app.settings import *

class ItemQtyDisplay():
    def __init__(self,background,pos,font,imageName,textColor=HUD_FONT_COLOR):
        super().__init__()
        self.background = background
        self.stat = None
        self.printedLine = None
        self.font = font
        self.textColor = textColor

        self.icon = pygame.image.load(os.path.join('img', imageName + '.png'))
        self.iconPos = pos
        self.setIcon()
        self.isSelected = False

        # Color
        self.color1 = COLOR_MENU_1
        self.color2 = COLOR_MENU_2

    def setIcon(self):
        resizeSizeY = 25
        imageSizeX = self.icon.get_width() * resizeSizeY / self.icon.get_height()

        self.icon = pygame.transform.scale(self.icon, (int(imageSizeX), int(resizeSizeY)))

        self.textPos = (self.iconPos[0]+self.icon.get_width(),self.iconPos[1])

    def display(self):
        self.background.blit(self.icon, self.iconPos)
        self.printedLine = self.font.render(' X ' + self.stat, True, self.textColor)
        self.background.blit(self.printedLine, self.textPos)
