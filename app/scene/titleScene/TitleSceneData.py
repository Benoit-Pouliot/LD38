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

        # Création du background
        self.background = pygame.sprite.Sprite()
        self.background.rect = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        self.background.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.image.fill((50,50,50))
        self.allSprites.add(self.background)

        self.camera = None

        self.createStartMenu()

    def createStartMenu(self):
        self.startGameButton = Button((400, 5 * SCREEN_HEIGHT / 20), (300, 50), 'Go to white Title Screen',
                                       self.startGame)
        self.spritesHUD.add(self.startGameButton)
        self.notifySet.add(self.startGameButton)

        self.exitButton = Button((400, 15 * SCREEN_HEIGHT / 20), (300, 50), 'Exit', sys.exit)
        self.spritesHUD.add(self.exitButton)
        self.notifySet.add(self.exitButton)

    def startGame(self):
        self.nextScene = GAME_SCENE