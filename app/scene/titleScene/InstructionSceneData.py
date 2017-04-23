__author__ = 'Bobsleigh'

# Imports
import pygame
import os

from ldLib.GUI.Button import Button
from ldLib.GUI.messageBox.MessageBox import MessageBox

from app.settings import *

import weakref

class InstructionSceneData:
    def __init__(self):
        self.nextScene = None

        self.notifySet = weakref.WeakSet()
        self.allSprites = pygame.sprite.Group()
        self.spritesHUD = pygame.sprite.Group()
        self.spritesBackGround = pygame.sprite.Group()

        # background
        self.background = pygame.sprite.Sprite()
        self.background.rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background.image = pygame.image.load(os.path.join('img', 'titleScreen.png'))
        self.background.rect = self.background.image.get_rect()

        self.spritesBackGround.add(self.background)

        self.player = None
        self.camera = None

        boxWidth = 0.55 * SCREEN_WIDTH
        self.createControlBox(SCREEN_WIDTH/2-boxWidth/2, 3*SCREEN_HEIGHT / 7, boxWidth,2 * SCREEN_HEIGHT / 5)

        buttonWidth = 0.55 * SCREEN_WIDTH-100
        self.backToTitleScreenButton = Button((SCREEN_WIDTH/2-buttonWidth/2, 17 * SCREEN_HEIGHT / 20), (buttonWidth, 50), 'Back to main menu',
                                              self.goToTitleScreen)
        self.spritesHUD.add(self.backToTitleScreenButton)
        self.notifySet.add(self.backToTitleScreenButton)

    def createControlBox(self,x,y,width,height):
        self.textGoal = MessageBox(x,y,width,height)
        self.textGoal.textList.append('PLEASE TEACH ME HOW TO PLAY')
        self.textGoal.textList.append('')
        self.textGoal.textList.append('PRETTY PRETTY PLEASE')


        self.allSprites.add(self.textGoal)  # Add sprite

    def goToTitleScreen(self):
        self.nextScene = TITLE_SCENE


