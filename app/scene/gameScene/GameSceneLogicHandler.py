from app.scene.gameScene.GameSceneData import GameSceneData
from app.settings import *
from ldLib.collision.collisionNotifySprite import collisionNotifySprite
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

    def handle(self): #Update, gravity and collisions must be handled in that order for jump to work
        self.applyFriction(self.player)
        # self.collisionChecker.collisionAllSprites(self.player, self.mapData, self.gameData)
        self.handleZoneCollision(self.player)
        self.checkShop()
        self.checkHighlight()
        self.data.allSprites.update()
        self.data.spritesHUD.update()
        self.applyGravity(self.player)
        self.handleSpriteTileCollision(self.player, self.data)

    def handleSpriteTileCollision(self, sprite, data):
        if sprite.isPhysicsApplied == True or sprite.isCollisionApplied == True:
            collisionNotifySprite(sprite, SOLID, data)


    def handleZoneCollision(self, player):
        inShopZone = False
        for obj in self.data.tmxData.objects:
            if self.isPlayerIsInZone(player, obj) == True:
                if obj.name == "OutZone":
                    nameNewZone = obj.LevelZone
                    nameInZone = obj.InZone

                    # Initializing new map
                    self.newMapData = GameSceneData(nameNewZone, nameInZone)
                elif obj.name == "ShopZone":
                    inShopZone = True

        if inShopZone:
            self.data.activateShop = True
        else:
            self.data.activateShop = False


    def isPlayerIsInZone(self, player, zone):

        if player.rect.centerx  >= zone.x and \
           player.rect.centerx <= zone.x + zone.width and \
           player.rect.centery >= zone.y and \
           player.rect.centery <= zone.y + zone.height:
           return True
        else:
           return False

    def applyGravity(self, sprite):
        if sprite.isPhysicsApplied == True or sprite.isGravityApplied == True:
            sprite.speedy += GRAVITY

    def applyFriction(self, sprite):
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

    def checkHighlight(self):
        mousePos = pygame.mouse.get_pos()
        for obj in self.data.notifySet:
            if obj.rect.collidepoint(mousePos):
                obj.isSelected = True
            else:
                obj.isSelected = False

    def checkShop(self):
        if self.data.activateShop:
            self.data.allSprites.add(self.data.shop)
        else:
            self.data.allSprites.remove(self.data.shop)
            for sprites in self.data.shopGroup:
                if self.data.spritesHUD.has(sprites):
                    self.data.spritesHUD.remove(sprites)
                    self.data.notifySet.remove(sprites)
