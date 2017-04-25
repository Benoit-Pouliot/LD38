import os
import pygame

from app.settings import *

class ImageDisplay():
    def __init__(self,background,pos,font,statName=None, imageName='pig',textColor=HUD_FONT_COLOR):
        super().__init__()
        self.background = background
        self.statName = statName
        self.printedLine = None
        self.position = pos
        self.font = font
        self.textColor = textColor
        self.position = pos

        self.printedLine = self.font.render(self.statName, True, self.textColor)

        self.iconName = imageName
        self.icon = pygame.image.load(os.path.join('img', self.iconName + '.png'))
        self.iconPos = (0,0)
        self.setIcon()
        self.isSelected = False

        # Color
        self.color1 = COLOR_MENU_1
        self.color2 = COLOR_MENU_2

    def setIcon(self):
        resizeSizeY = 30
        imageSizeX = self.icon.get_width() * resizeSizeY / self.icon.get_height()

        self.icon = pygame.transform.scale(self.icon, (int(imageSizeX), int(resizeSizeY)))
        self.iconPos = (self.position[0]+self.printedLine.get_width(),self.position[1])

    def display(self,imageName = 'pig'):
        if imageName != self.iconName:
            self.iconName=imageName
            self.icon = pygame.image.load(os.path.join('img', self.iconName + '.png'))
            self.setIcon()
        self.background.blit(self.printedLine, self.position)
        self.background.blit(self.icon, self.iconPos)
