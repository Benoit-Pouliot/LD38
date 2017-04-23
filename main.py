d__author__ = 'Bobsleigh'

import os
import sys

import pygame

from app.SceneHandler import SceneHandler
from app.settings import *

if __name__ == '__main__':
    #Code to check if the code is running from a PyInstaller --onefile .exe
    if getattr(sys, 'frozen', False):
         os.chdir(sys._MEIPASS)

    # Screen
    screenSize = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screenSize)

    pygame.display.set_caption("Gnome Digger")

    # Init
    pygame.mixer.pre_init(16000 , -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    pygame.font.init()

    # Icon
    surface = pygame.image.load(os.path.join('img', 'gnome_v1.png'))
    pygame.display.set_icon(surface)

    # Hide the mouse
    # pygame.mouse.set_visible(False)

    # Setup with gameData and the first scene
    sceneHandler = SceneHandler(screen)

    sceneHandler.mainLoop()


