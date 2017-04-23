__author__ = 'Bobsleigh'

# Imports
import pygame

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
        self.background.rect = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        self.background.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.image.fill((50,0,0))
        self.spritesBackGround.add(self.background)

        self.player = None
        self.camera = None

        self.createControlBox(60, SCREEN_HEIGHT / 10, 0.55 * SCREEN_WIDTH, 4 * SCREEN_HEIGHT / 5)

        self.backToTitleScreenButton = Button((520, 17 * SCREEN_HEIGHT / 20), (250, 50), 'Back to main menu',
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


