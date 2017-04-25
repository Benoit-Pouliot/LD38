import logging
import os
import weakref

import pygame
import pyscroll
import pytmx

from app.settings import *
from app.sprites.GUI.HUD import HUD
from app.sprites.Player import Player
from app.sprites.Seller import Seller
from app.sprites.WinZone import WinZone
from app.sprites.Shop import Shop
from app.sprites.Heart import Heart
from ldLib.tools.TmxData import TmxData
from app.sprites.Woman import Woman

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

        self.tileLife = [[] for i in range(self.tmxData.width)]

        # self.soundController = soundPlayerController()

        # Local TmxData : Usefull to modify the tmxData
        self.localTmxData = TmxData(self.tmxData)

        for i in range(self.tmxData.width):
            for j in range(self.tmxData.height):
                self.tileLife[i].append(self.tileTypeToTileLife(self.localTmxData.get_tileTypeFromGid(self.tmxData.get_tile_gid(i, j, TERRAIN_LAYER))))

        self.solidGID = self.localTmxData.get_gidFromTileType(SOLID)
        self.indestructibleGID = self.localTmxData.get_gidFromTileType(INDESTRUCTIBLE)
        self.ladderGID = self.localTmxData.get_gidFromTileType(LADDER)
        self.ladderTileGID = self.localTmxData.get_gidFromTileType(LADDER_TILE)

        self.allSprites = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        self.redTileMaskGroup = pygame.sprite.Group()
        self.springGroup = pygame.sprite.Group()
        self.dynamiteGroup = pygame.sprite.Group()
        self.spritesHUD = pygame.sprite.Group()
        self.spritesBackGround = pygame.sprite.Group()

                # if obj.type == "item":
                #     item = iFactory.create(obj)
                #     self.allSprites.add(item)
                #     self.itemGroup.add(item)

        # Put camera in mapData
        self.camera = pyscroll.PyscrollGroup(map_layer=self.cameraPlayer, default_layer=SPRITE_LAYER)

        # Spawn point of the player
        valBool = False
        for obj in self.tmxData.objects:
            if obj.name == "InZone":
                if obj.StartPoint == nameInZone:
                    self.spawmPointPlayerx = obj.x
                    self.spawmPointPlayery = obj.y
                    valBool = True
            elif obj.name == "SpawnSeller":
                self.seller = Seller(obj.x,obj.y)
                self.allSprites.add(self.seller)

        # Update camera
        self.camera.add(self.allSprites)

        self.player = Player(self.spawmPointPlayerx, self.spawmPointPlayery, self)
        self.woman = Woman(59*self.tmxData.tilewidth, 107*self.tmxData.tileheight)
        self.camera.add(self.woman)



        self.allSprites.add(self.player)
        self.notifySet.add(self.player)
        self.camera.add(self.player)

        # Fin du mapData

        #Create Shop
        self.shopGroup = pygame.sprite.Group()
        self.shop = Shop(self)
        self.activateShop = False

        #Create WinZone
        self.winGroup = pygame.sprite.Group()
        self.winZone = WinZone(self)
        self.activateWinZone = False

        self.heart = Heart(59.25*self.tmxData.tilewidth, 106.3*self.tmxData.tileheight)
        self.camera.add(self.heart)
        self.winGroup.add(self.heart)

        # Player inventory
        self.money = 0
        self.nbSpring = 0
        self.nbLadder = 10
        self.nbAntiGravity = 0
        self.nbDynamite = 0
        self.lvlPickaxe = 1
        self.lvlDrill = 0

        if TAG_MARIE == 1:
            self.money = 10000
            self.nbSpring = 10
            self.nbLadder = 10
            self.nbAntiGravity = 10
            self.lvlPickaxe = 1
            self.lvlDrill = 0
            self.player.setStrength()


        if TAG_BP:
            self.money = 100000
            self.nbSpring = 300
            self.nbLadder = 200
            self.nbAntiGravity = 100
            self.lvlPickaxe = 1
            self.lvlDrill = 1

        if TAG_PHIL:
            self.money = 10000
            self.nbSpring = 10
            self.nbLadder = 10
            self.nbAntiGravity = 10
            self.lvlPickaxe = 1
            self.lvlDrill = 0
            self.player.setStrength()


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

    def tileTypeToTileLife(self, tileType):
        #return TileLife(1)
        if tileType == 53: #Dirt
            return TileLife(TILE_DIRT)
        elif tileType == 51 or tileType == 57: #Gold in dirt
            return TileLife(TILE_DIRT_GOLD)
        elif tileType == 52 or tileType == 58: #Pink gold in dirt
            return TileLife(TILE_DIRT_PINK)
        elif tileType == 63: #Rock
            return TileLife(TILE_ROCK)
        elif tileType == 59 or tileType == 77: #Pink gold in rock
            return TileLife(TILE_ROCK_PINK)
        elif tileType == 65 or tileType == 71: #Topaze in rock
            return TileLife(TILE_ROCK_GREEN)
        elif tileType == 69: #Blue rock
            return TileLife(TILE_BLUE)
        elif tileType == 70 or tileType == 75: #Topaze in blue rock
            return TileLife(TILE_BLUE_GREEN)
        elif tileType == 76 or tileType == 81: #Red diamond in blue rock
            return TileLife(TILE_BLUE_RED)
        else:
            return TileLife(1)

class TileLife:
    def __init__(self, maxLife):
        self.maxLife = maxLife
        self.life = maxLife