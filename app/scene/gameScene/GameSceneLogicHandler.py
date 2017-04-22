from app.scene.gameScene.GameSceneData import GameSceneData
from app.settings import *
import pygame

class GameSceneLogicHandler:
    def __init__(self, gameData):

        self.sceneRunning = True
        self.endState = None
        self.newMapData = None
        self.gameData = gameData
        self.data = gameData.data
        self.player = gameData.data.player
        # self.collisionChecker = CollisionPlayerPlatform(self.player, self.mapData)

    def handle(self):
        # self.applyGravity(self.mapData.allSprites)
        # self.applyFriction(self.mapData.allSprites)
        # self.collisionChecker.collisionAllSprites(self.player, self.mapData, self.gameData)
        # self.handleZoneCollision(self.player)
        self.data.allSprites.update()

    def handleZoneCollision(self, player):
        for obj in self.data.tmxData.objects:
            if self.isPlayerIsInZone(player, obj) == True:
                if obj.name == "OutZone":
                    nameNewZone = obj.LevelZone
                    nameInZone = obj.InZone

                    # Initializing new map
                    self.newMapData = GameSceneData(nameNewZone, nameInZone)

    def isPlayerIsInZone(self, player, zone):

        if player.rect.centerx  >= zone.x and \
           player.rect.centerx <= zone.x + zone.width and \
           player.rect.centery >= zone.y and \
           player.rect.centery <= zone.y + zone.height:
           return True
        else:
           return False

    def applyGravity(self, allSprites):
        for sprite in allSprites:
            if sprite.isPhysicsApplied == True or sprite.isGravityApplied == True:
                sprite.speedy += GRAVITY

    def applyFriction(self, allSprites):
        for sprite in allSprites:
            if sprite.isPhysicsApplied == True or sprite.isFrictionApplied == True:
                pass
                if sprite.speedx > 0 and sprite.speedx - FRICTION > 0:
                    sprite.speedx -= FRICTION
                elif sprite.speedx > 0:
                    sprite.speedx = 0

                if sprite.speedx < 0 and sprite.speedx + FRICTION < 0:
                    sprite.speedx += FRICTION
                elif sprite.speedx < 0:
                    sprite.speedx = 0