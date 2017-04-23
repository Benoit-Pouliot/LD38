__author__ = 'Bobsleigh'

# Imports
import os
import sys

import pygame

from ldLib.GUI.Button import Button
from app.settings import *

import weakref

class TitleSceneData:
    def __init__(self):
        self.nextScene = None

        self.notifySet = weakref.WeakSet()
        self.allSprites = pygame.sprite.Group()
        self.spritesHUD = pygame.sprite.Group()
        self.spritesBackGround = pygame.sprite.Group()

        # background
        self.background = pygame.sprite.Sprite()
        self.background.rect = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        self.background.image = pygame.image.load(os.path.join('img', 'titleScreen.png'))
        self.background.rect = self.background.image.get_rect()

        self.spritesBackGround.add(self.background)

        self.player = None
        self.camera = None

        self.createStartMenu()

    def createStartMenu(self):
        buttonWidth = 300
        buttonHeight = 50
        self.startGameButton = Button((SCREEN_WIDTH/2-buttonWidth/2, 10 * SCREEN_HEIGHT / 20), (buttonWidth, buttonHeight), 'Start game',
                                       self.startGame)
        self.spritesHUD.add(self.startGameButton)
        self.notifySet.add(self.startGameButton)

        self.instructionButton = Button((SCREEN_WIDTH/2-buttonWidth/2, 12 * SCREEN_HEIGHT / 20), (buttonWidth, buttonHeight), 'Instruction',
                                      self.goToInstruction)
        self.spritesHUD.add(self.instructionButton)
        self.notifySet.add(self.instructionButton)

        self.creditButton = Button((SCREEN_WIDTH/2-buttonWidth/2, 14 * SCREEN_HEIGHT / 20), (buttonWidth, buttonHeight), 'Credit',
                                      self.goToCredit)
        self.spritesHUD.add(self.creditButton)
        self.notifySet.add(self.creditButton)

        self.exitButton = Button((SCREEN_WIDTH/2-buttonWidth/2, 16 * SCREEN_HEIGHT / 20), (buttonWidth, buttonHeight), 'Exit', sys.exit)
        self.spritesHUD.add(self.exitButton)
        self.notifySet.add(self.exitButton)

    def startGame(self):
        self.nextScene = GAME_SCENE

    def goToInstruction(self):
        self.nextScene = INSTRUCTION_SCENE

    def goToCredit(self):
        self.nextScene = CREDIT_SCENE