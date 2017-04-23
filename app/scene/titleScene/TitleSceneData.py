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
        self.background.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.image.fill((0,50,50))
        self.spritesBackGround.add(self.background)

        self.player = None
        self.camera = None

        self.createStartMenu()

    def createStartMenu(self):
        self.startGameButton = Button((400, 6 * SCREEN_HEIGHT / 20), (300, 50), 'Start game',
                                       self.startGame)
        self.spritesHUD.add(self.startGameButton)
        self.notifySet.add(self.startGameButton)

        self.instructionButton = Button((400, 9 * SCREEN_HEIGHT / 20), (300, 50), 'Instruction',
                                      self.goToInstruction)
        self.spritesHUD.add(self.instructionButton)
        self.notifySet.add(self.instructionButton)

        self.creditButton = Button((400, 12 * SCREEN_HEIGHT / 20), (300, 50), 'Credit',
                                      self.goToCredit)
        self.spritesHUD.add(self.creditButton)
        self.notifySet.add(self.creditButton)

        self.exitButton = Button((400, 15 * SCREEN_HEIGHT / 20), (300, 50), 'Exit', sys.exit)
        self.spritesHUD.add(self.exitButton)
        self.notifySet.add(self.exitButton)

    def startGame(self):
        self.nextScene = GAME_SCENE

    def goToInstruction(self):
        self.nextScene = INSTRUCTION_SCENE

    def goToCredit(self):
        self.nextScene = CREDIT_SCENE