__author__ = 'Bobsleigh'

# Imports
import pygame
import os

from ldLib.GUI.Button import Button
from ldLib.GUI.messageBox.MessageBox import MessageBox

from app.settings import *

import weakref

class CreditSceneData:
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

        widthCreditBox = 0.5*SCREEN_WIDTH
        heightCreditBox = 0.4*SCREEN_HEIGHT

        self.createCreditBox(SCREEN_WIDTH/2-widthCreditBox/2, 3*SCREEN_HEIGHT / 7, widthCreditBox, heightCreditBox)

        buttonWidth = 0.55 * SCREEN_WIDTH - 100
        self.backToTitleScreenButton = Button((SCREEN_WIDTH / 2 - buttonWidth / 2, 17 * SCREEN_HEIGHT / 20),
                                              (buttonWidth, 50), 'Back to main menu',
                                              self.goToTitleScreen)
        self.spritesHUD.add(self.backToTitleScreenButton)
        self.notifySet.add(self.backToTitleScreenButton)

    def createCreditBox(self,x,y,width,height):
        self.textGoal = MessageBox(x,y,width,height)
        self.textGoal.textList.append('For Ludum Dare 38')
        self.textGoal.textList.append('')
        self.textGoal.textList.append('')
        self.textGoal.textList.append('Credit :')
        self.textGoal.textList.append('')
        self.textGoal.textList.append('Game and design : Bobsleigh\'s team')
        self.textGoal.textList.append('Graphics : Bobsleigh\'s team')
        self.textGoal.textList.append('Music : Bobsleigh\'s team')
        self.textGoal.textList.append('')

        self.allSprites.add(self.textGoal)  # Add sprite

    def goToTitleScreen(self):
        self.nextScene = TITLE_SCENE