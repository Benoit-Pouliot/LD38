import logging
import os
import weakref

import pygame
import pyscroll
import pytmx

from app.settings import *
from app.sprites.GUI.HUD import HUD
from app.sprites.Player import Player
from app.sprites.Shop import Shop
from ldLib.tools.TmxData import TmxData


class GameSceneData:
    def __init__(self,mapName="WorldMap", nameInZone="StartPointWorld",screenSize=(SCREEN_WIDTH,SCREEN_HEIGHT)):
        self.nextScene = None
        self.notifySet = weakref.WeakSet()

        # Beginning MAP DATA
        self.nameMap = mapName

        # A set-up to shut down the logger 'orthographic' in pyscroll
        logger = logging.getLogger('orthographic')
        logger.setLevel(logging.ERROR)

        self.tmxData = pytmx.util_pygame.load_pygame(self.reqImageName(self.nameMap))
        self.tiledMapData = pyscroll.data.TiledMapData(self.tmxData)
        self.cameraPlayer = pyscroll.BufferedRenderer(self.tiledMapData, screenSize, clamp_camera=True)
        # self.soundController = soundPlayerController()

        # Local TmxData : Usefull to modify the tmxData
        self.localTmxData = TmxData(self.tmxData)

        self.solidGID = self.localTmxData.get_gidFromTileType(SOLID)
        self.indestructibleGID = self.localTmxData.get_gidFromTileType(INDESTRUCTIBLE)
        self.ladderGID = self.localTmxData.get_gidFromTileType(LADDER)

        self.allSprites = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        self.springGroup = pygame.sprite.Group()
        self.spritesHUD = pygame.sprite.Group()
        self.spritesBackGround = pygame.sprite.Group()

                # if obj.type == "item":
                #     item = iFactory.create(obj)
                #     self.allSprites.add(item)
                #     self.itemGroup.add(item)

        # Put camera in mapData
        self.camera = pyscroll.PyscrollGroup(map_layer=self.cameraPlayer, default_layer=SPRITE_LAYER)
        self.camera.add(self.allSprites)

        # Spawn point of the player
        valBool = False
        for obj in self.tmxData.objects:
            if obj.name == "InZone":
                if obj.StartPoint == nameInZone:
                    self.spawmPointPlayerx = obj.x
                    self.spawmPointPlayery = obj.y
                    valBool = True

        self.player = Player(self.spawmPointPlayerx, self.spawmPointPlayery, self)

        self.allSprites.add(self.player)
        self.notifySet.add(self.player)
        self.camera.add(self.player)

        # Fin du mapData

        #Create Shop
        self.shopGroup = pygame.sprite.Group()
        self.shop = Shop(self)
        self.activateShop = False

        # Player inventory
        self.money = 0
        self.nbSpring = 200
        self.nbLadder = 0
        self.nbAntiGravity = 0
        self.lvlPickaxe = 1
        self.lvlDrill = 0
        self.lvlDynamite = 0

        if TAG_MARIE == 1:
            self.money = 12345678
            self.nbSpring = 3
            self.nbLadder = 2
            self.nbAntiGravity = 1

        self.addHUD()

    def close(self):
        self.sceneRunning = False

    def backToMain(self):
        self.nextScene = TITLE_SCENE
        self.close()

    def reqImageName(self, nameMap):
        return os.path.join('tiles_map', nameMap + ".tmx")

    def addHUD(self):
        self.HUD = HUD(self)
        self.spritesHUD.add(self.HUD)