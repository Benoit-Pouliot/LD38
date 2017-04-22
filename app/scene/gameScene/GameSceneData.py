import pyscroll
import pytmx
import pygame
import os
import weakref
import logging

from app.settings import *
from app.sprites.Player import Player
from app.sprites.Shop import Shop
from app.sprites.GUI.HUD import HUD
from app.scene.gameScene.TmxData import TmxData

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

        if TAG_BP:
            self.localTmxData.addTileXYToListToChange((5*32,27*32), 0, 2)
            self.localTmxData.addTileXYToListToChange((6*32,27*32), 0, 'Terrain_TL')
            self.localTmxData.changeAllTileInList(self.cameraPlayer)

        self.allSprites = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        self.spritesHUD = pygame.sprite.Group()

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
        self.shopGroup.add(self.shop)
        self.allSprites.add(self.shop)

        self.money = 0
        if TAG_MARIE == 1:
            self.money = 1234

        self.addHUD()

    def close(self):
        self.sceneRunning = False

    def backToMain(self):
        self.nextScene = TITLE_SCENE
        self.close()

    def reqImageName(self, nameMap):
        print(os.getcwd())
        return os.path.join('tiles_map', nameMap + ".tmx")

    def addHUD(self):
        self.HUD = HUD(self)
        self.spritesHUD.add(self.HUD)