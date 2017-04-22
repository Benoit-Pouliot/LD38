from app.settings import *

#To initialize my pet
import os
import pygame


# All the global data for the game and player
class GameData:
    def __init__(self, scene=None):

        self.mapData = None
        self.currentLevel = 1

        # self.initLevel(6)