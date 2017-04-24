from app.settings import *
import pygame

class CollisionPlayer:
    def __init__(self, player, map):
        # self.soundControl = soundPlayerController
        self.tileWidth = map.tmxData.tilewidth
        self.tileHeight = map.tmxData.tileheight
        self.mapHeight = map.tmxData.height * self.tileHeight
        self.mapWidth = map.tmxData.width * self.tileWidth
        self.player = player
        self.map = map

    def collisionAllSprites(self, player, mapData):
        for sprite in mapData.allSprites:
            if sprite.name == 'player':
                if player.isPhysicsApplied == True or player.isCollisionApplied == True:
                    self.rightCollision(player, mapData)
                    self.leftCollision(player, mapData)
                    self.downCollision(player, mapData)
                    self.upCollision(player, mapData)

                    self.dealWithStuck(player, mapData)
            elif sprite.name == 'seller':
                if sprite.isPhysicsApplied == True or sprite.isCollisionApplied == True:
                    self.rightCollision(sprite, mapData)
                    self.leftCollision(sprite, mapData)
                    self.downCollision(sprite, mapData)
                    self.upCollision(sprite, mapData)

    def dealWithStuck(self, player, mapData):
        tileWidth = mapData.tmxData.tilewidth
        tileHeight = mapData.tmxData.tileheight

        upRightTileGid = self.map.tmxData.get_tile_gid((player.collisionMask.rect.right + player.speedx)/self.tileWidth, player.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER)
        downRightTileGid = self.map.tmxData.get_tile_gid((player.collisionMask.rect.right + player.speedx)/self.tileWidth, (player.collisionMask.rect.bottom-1)/self.tileHeight, COLLISION_LAYER)
        upLeftTileGid = mapData.tmxData.get_tile_gid((player.collisionMask.rect.left + player.speedx)/tileWidth, player.collisionMask.rect.top/tileHeight, COLLISION_LAYER)
        downLeftTileGid = mapData.tmxData.get_tile_gid((player.collisionMask.rect.left + player.speedx)/tileWidth, (player.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER)
        upMidTileGid = mapData.tmxData.get_tile_gid(player.collisionMask.rect.centerx/tileWidth, (player.collisionMask.rect.top + player.speedy)/tileHeight, COLLISION_LAYER)

        if upRightTileGid  == self.map.solidGID and downRightTileGid == self.map.solidGID and upLeftTileGid == self.map.solidGID and downLeftTileGid == self.map.solidGID and upMidTileGid == self.map.solidGID:
            player.rect.y -= 2*tileHeight

    def rightCollision(self,player, map):

        # mapHeight = map.tmxData.height * tileHeight
        i=0

        if player.collisionMask.rect.right + player.speedx > 0:
            if player.speedx >= self.tileWidth: #Si on va plus vite qu'une tile/seconde
                while player.collisionMask.rect.right+i*self.tileWidth < player.collisionMask.rect.right + player.speedx:
                    if player.collisionMask.rect.right+i*self.tileWidth >= self.mapWidth:
                        j=0
                        while map.tmxData.get_tile_gid((self.mapWidth - 1 - j*self.tileWidth)/self.tileWidth, player.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER) == self.map.solidGID and map.tmxData.get_tile_gid((self.mapWidth - 1- j*self.tileWidth)/self.tileWidth, (player.collisionMask.rect.bottom)/self.tileHeight, COLLISION_LAYER) == self.map.solidGID:
                            j += 1
                        player.collisionMask.rect.right = self.mapWidth-j*self.tileWidth-1
                        player.speedx = 0
                        return

                    upRightTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.right + i*self.tileWidth)/self.tileWidth, player.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER)
                    downRightTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.right + i*self.tileWidth)/self.tileWidth, (player.collisionMask.rect.bottom-1)/self.tileHeight, COLLISION_LAYER)

                    if (upRightTileGid  == self.map.solidGID or upRightTileGid == self.map.indestructibleGID or downRightTileGid  == self.map.solidGID or downRightTileGid == self.map.indestructibleGID) and player.speedx > 0 and player.facingSide == RIGHT:
                        while map.tmxData.get_tile_gid((player.collisionMask.rect.right + 1)/self.tileWidth, player.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER) != self.map.solidGID and map.tmxData.get_tile_gid((player.collisionMask.rect.right + 1)/self.tileWidth, (player.collisionMask.rect.bottom-1)/self.tileHeight, COLLISION_LAYER) != self.map.solidGID:
                            player.collisionMask.rect.right += 1
                        player.speedx = 0
                    i += 1

            else:
                upRightTileGid = self.map.tmxData.get_tile_gid((player.collisionMask.rect.right + player.speedx)/self.tileWidth, player.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER)
                downRightTileGid = self.map.tmxData.get_tile_gid((player.collisionMask.rect.right + player.speedx)/self.tileWidth, (player.collisionMask.rect.bottom-1)/self.tileHeight, COLLISION_LAYER)
                lowMidRightTileGid = self.map.tmxData.get_tile_gid((player.collisionMask.rect.right + player.speedx)/self.tileWidth, (player.collisionMask.rect.centery-10-1)/self.tileHeight, COLLISION_LAYER)
                highMidRightTileGid = self.map.tmxData.get_tile_gid((player.collisionMask.rect.right + player.speedx)/self.tileWidth, (player.collisionMask.rect.centery+10-1)/self.tileHeight, COLLISION_LAYER)

                if (upRightTileGid  == self.map.solidGID or upRightTileGid  == self.map.indestructibleGID or downRightTileGid == self.map.solidGID or downRightTileGid  == self.map.indestructibleGID or lowMidRightTileGid == self.map.solidGID or lowMidRightTileGid  == self.map.indestructibleGID or highMidRightTileGid == self.map.solidGID or highMidRightTileGid == self.map.indestructibleGID) and player.speedx > 0:
                    # while map.tmxData.get_tile_gid((player.collisionMask.rect.right + 1)/self.tileWidth, player.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER) != self.map.solidGID and map.tmxData.get_tile_gid((player.collisionMask.rect.right + 1)/self.tileWidth, (player.collisionMask.rect.bottom)/self.tileHeight, COLLISION_LAYER) != self.map.solidGID:
                    #     player.collisionMask.rect.right += 1
                    player.speedx = 0
                    player.collisionMask.rect.right += self.tileWidth - (player.collisionMask.rect.right % self.tileWidth) - 1 #On colle le player sur le mur à droite
                elif upRightTileGid  == SPIKE or downRightTileGid == SPIKE or lowMidRightTileGid == SPIKE or highMidRightTileGid == SPIKE:
                    player.dead()
                elif (upRightTileGid  == SPRING or downRightTileGid == SPRING or lowMidRightTileGid == SPRING or highMidRightTileGid == SPRING) and player.speedx > 0:
                    player.speedx = 0
                    player.collisionMask.rect.right += self.tileWidth - (player.collisionMask.rect.right % self.tileWidth) - 1 #On colle le player sur le mur à droite

    def getUpRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.collisionMask.rect.right + self.player.speedx)/self.tileWidth, self.player.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER)
    def getDownRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.collisionMask.rect.right + self.player.speedx)/self.tileWidth, (self.player.collisionMask.rect.bottom-1)/self.tileHeight, COLLISION_LAYER)
    def getLowMidRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.collisionMask.rect.right + self.player.speedx)/self.tileWidth, (self.player.collisionMask.rect.centery-10-1)/self.tileHeight, COLLISION_LAYER)
    def getHighMidRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.collisionMask.rect.right + self.player.speedx)/self.tileWidth, (self.player.collisionMask.rect.centery+10-1)/self.tileHeight, COLLISION_LAYER)
    # def getRightTilesList(self): à terminer si besoin (décomposer le nb de pts de vérification sur le sprite selon sa taille, à place de 4 fixes)
    #     tileList = []
    #     pointNumber = self.tileHeight
    #     tileList.append(self.map.tmxData.get_tile_gid((self.player.collisionMask.rect.right + self.player.speedx)/self.tileWidth, (self.player.collisionMask.rect.centery+10-1)/self.tileHeight, COLLISION_LAYER))

    def leftCollision(self,player, map):
        tileWidth = map.tmxData.tilewidth
        tileHeight = map.tmxData.tileheight
        # mapWidth = map.tmxData.width * tileWidth
        # mapHeight = map.tmxData.height * tileHeight
        i = 0

        if -player.speedx >= tileWidth:
            while player.collisionMask.rect.x-i*tileWidth > player.collisionMask.rect.x + player.speedx:
                if player.collisionMask.rect.x-i*tileWidth <= 0:
                    j=0
                    while map.tmxData.get_tile_gid((0 + j*tileWidth)/tileWidth, player.collisionMask.rect.top/tileHeight, COLLISION_LAYER) == self.map.solidGID and map.tmxData.get_tile_gid((0 + j*tileWidth)/tileWidth, (player.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER) == self.map.solidGID:
                        j += 1
                    player.collisionMask.rect.left = j*tileWidth
                    player.speedx = 0
                    return

                upLeftTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.left - i*tileWidth)/tileWidth, player.collisionMask.rect.top/tileHeight, COLLISION_LAYER)
                downLeftTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.left - i*tileWidth)/tileWidth, (player.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER)

                if (upLeftTileGid  == self.map.solidGID or downLeftTileGid  == self.map.solidGID) and player.facingSide == LEFT:
                    while map.tmxData.get_tile_gid((player.collisionMask.rect.left)/tileWidth, player.collisionMask.rect.top/tileHeight, COLLISION_LAYER) != self.map.solidGID and map.tmxData.get_tile_gid((player.collisionMask.rect.left)/tileWidth, (player.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER) != self.map.solidGID:
                        player.collisionMask.rect.left -= 1
                    player.speedx = 0
                i += 1

        else:
            upLeftTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.left + player.speedx)/tileWidth, player.collisionMask.rect.top/tileHeight, COLLISION_LAYER)
            downLeftTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.left + player.speedx)/tileWidth, (player.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER)
            lowMidLeftTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.left + player.speedx)/tileWidth, (player.collisionMask.rect.centery-10)/tileHeight, COLLISION_LAYER)
            highMidLeftTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.left + player.speedx)/tileWidth, (player.collisionMask.rect.centery+10)/tileHeight, COLLISION_LAYER)

            if (upLeftTileGid  == self.map.solidGID or upLeftTileGid  == self.map.indestructibleGID or downLeftTileGid  == self.map.solidGID or downLeftTileGid  == self.map.indestructibleGID or lowMidLeftTileGid == self.map.solidGID or lowMidLeftTileGid  == self.map.indestructibleGID or highMidLeftTileGid == self.map.solidGID or highMidLeftTileGid  == self.map.indestructibleGID) and player.speedx < 0:
                #while map.tmxData.get_tile_gid((player.collisionMask.rect.left)/tileWidth, player.collisionMask.rect.top/tileHeight, COLLISION_LAYER) != self.map.solidGID and map.tmxData.get_tile_gid((player.collisionMask.rect.left)/tileWidth, (player.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER) != self.map.solidGID:
                     #player.collisionMask.rect.left -= 1
                player.speedx = 0
                player.collisionMask.rect.left -= (player.collisionMask.rect.left % self.tileWidth) #On colle le player sur le mur de gauche
            elif upLeftTileGid  == SPIKE or downLeftTileGid  == SPIKE or lowMidLeftTileGid == SPIKE or highMidLeftTileGid == SPIKE:
                player.dead()
            elif (upLeftTileGid  == SPRING or downLeftTileGid  == SPRING or lowMidLeftTileGid == SPRING or highMidLeftTileGid == SPRING) and player.speedx < 0:
                player.speedx = 0

    def downCollision(self,player, map):
        tileWidth = map.tmxData.tilewidth
        tileHeight = map.tmxData.tileheight
        # mapWidth = map.tmxData.width * tileWidth
        # mapHeight = map.tmxData.height * tileHeight

        downLeftTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.left+1)/tileWidth, (player.collisionMask.rect.bottom + player.speedy)/tileHeight, COLLISION_LAYER)
        downRightTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.right)/tileWidth, (player.collisionMask.rect.bottom + player.speedy)/tileHeight, COLLISION_LAYER)
        downMidTileGID = map.tmxData.get_tile_gid((player.collisionMask.rect.centerx)/tileWidth, (player.collisionMask.rect.bottom + player.speedy)/tileHeight, COLLISION_LAYER)

        if downLeftTileGid == self.map.solidGID or downLeftTileGid  == self.map.indestructibleGID or downRightTileGid == self.map.solidGID or downRightTileGid  == self.map.indestructibleGID or downMidTileGID == self.map.solidGID or downMidTileGID  == self.map.indestructibleGID:
            # while map.tmxData.get_tile_gid((player.collisionMask.rect.left+1)/tileWidth, (player.collisionMask.rect.bottom)/tileHeight, COLLISION_LAYER) != self.map.solidGID and map.tmxData.get_tile_gid((player.collisionMask.rect.right)/tileWidth, (player.collisionMask.rect.bottom)/tileHeight, COLLISION_LAYER) != self.map.solidGID:
            #     player.collisionMask.rect.bottom += 1
            player.speedy = 0
            if player.jumpState != CLIMBING:
                player.jumpState = GROUNDED
        elif downLeftTileGid == SPIKE or downRightTileGid == SPIKE  or downMidTileGID == SPIKE:
            player.dead()
        elif downLeftTileGid == SPRING or downRightTileGid == SPRING  or downMidTileGID == SPRING:
            player.spring()
        else:
            if player.jumpState == GROUNDED:
                player.jumpState = JUMP


    def upCollision(self,player, map):
        tileWidth = map.tmxData.tilewidth
        tileHeight = map.tmxData.tileheight

        upLeftTileGid = map.tmxData.get_tile_gid((player.collisionMask.rect.left+1)/tileWidth, (player.collisionMask.rect.top + player.speedy)/tileHeight, COLLISION_LAYER)
        upRightTileGid = map.tmxData.get_tile_gid(player.collisionMask.rect.right/tileWidth, (player.collisionMask.rect.top + player.speedy)/tileHeight, COLLISION_LAYER)
        upMidTileGid = map.tmxData.get_tile_gid(player.collisionMask.rect.centerx/tileWidth, (player.collisionMask.rect.top + player.speedy)/tileHeight, COLLISION_LAYER)

        if upLeftTileGid == self.map.solidGID or upLeftTileGid  == self.map.indestructibleGID or upRightTileGid == self.map.solidGID or upRightTileGid  == self.map.indestructibleGID or upMidTileGid == self.map.solidGID or upMidTileGid  == self.map.indestructibleGID:
            #Coller le player sur le plafond
            while map.tmxData.get_tile_gid((player.collisionMask.rect.left+1)/tileWidth, (player.collisionMask.rect.top)/tileHeight, COLLISION_LAYER) != self.map.solidGID and map.tmxData.get_tile_gid(player.collisionMask.rect.right/tileWidth, (player.collisionMask.rect.top)/tileHeight, COLLISION_LAYER) != self.map.solidGID:
                player.collisionMask.rect.bottom -= 1
                player.rect.bottom -= 1
            player.collisionMask.rect.bottom += 1 #Redescendre de 1 pour sortir du plafond
            player.rect.bottom += 1

            # player.collisionMask.rect.top += tileHeight - (player.collisionMask.rect.top % tileHeight)
            # player.rect.top += tileHeight - (player.rect.top % tileHeight)


            player.speedy = 0

            if player.jumpState == CLIMBING:
                player.jumpState = JUMP
                player.upPressed = False
        elif upLeftTileGid == SPIKE or upRightTileGid == SPIKE:
            player.dead()
        elif upLeftTileGid == self.map.ladderGID or upRightTileGid == self.map.ladderGID or upMidTileGid == self.map.ladderGID:
            if player.jumpState != CLIMBING and player.name == "player":
                player.jumpState = CLIMBING
                player.speedx = 0
                player.speedy = 0
        else:
            if player.jumpState == CLIMBING:
                player.jumpState = JUMP
                player.upPressed = False


    def collisionWithEnemy(self, player, enemyGroup):
        collisionList = pygame.sprite.spritecollide(player, enemyGroup, False)
        for enemy in collisionList:
            player.hurt()
            # player.loseLife()
            # self.soundControl.hurt()
            pass



    def pickUpItem(self, player, itemGroup, gameMemory):
        collisionList = pygame.sprite.spritecollide(player, itemGroup, False)
        for item in collisionList:
            gameMemory.registerItemPickedUp(item)
            item.kill()

    def collisionWithSpring(self, player, springGroup):
        collisionList = pygame.sprite.spritecollide(player, springGroup, False, self.collisionWithMasks)
        for spring in collisionList:
            spring.bounce()
            player.bounce(spring.bounceSpeed)

    def collisionWithMasks(self, player, sprite):
        return player.collisionMask.rect.colliderect(sprite.collisionMask.rect)

def collisionBulletWall(bullet, map):
    tileWidth = map.tmxData.tilewidth
    tileHeight = map.tmxData.tileheight
    mapWidth = map.tmxData.width * tileWidth
    mapHeight = map.tmxData.height * tileHeight

    if (bullet.rect.top < tileHeight or bullet.rect.bottom > mapHeight - tileHeight) or (bullet.rect.left < tileWidth or bullet.rect.right > mapWidth - tileWidth):
        bullet.kill()
        return

    if bullet.speedx > 0:
        upRightTileGid = map.tmxData.get_tile_gid((bullet.rect.right + bullet.speedx)/tileWidth, bullet.rect.top/tileHeight, COLLISION_LAYER)
        downRightTileGid = map.tmxData.get_tile_gid((bullet.rect.right + bullet.speedx)/tileWidth, (bullet.rect.bottom-1)/tileHeight, COLLISION_LAYER)

        if (upRightTileGid  == self.map.solidGID or downRightTileGid  == self.map.solidGID):
            bullet.kill()

    elif bullet.speedx < 0:
        upLeftTileGid = map.tmxData.get_tile_gid((bullet.rect.left + bullet.speedx)/tileWidth, bullet.rect.top/tileHeight, COLLISION_LAYER)
        downLeftTileGid = map.tmxData.get_tile_gid((bullet.rect.left + bullet.speedx)/tileWidth, (bullet.rect.bottom)/tileHeight, COLLISION_LAYER)

        if (upLeftTileGid  == self.map.solidGID or downLeftTileGid  == self.map.solidGID) and bullet.speedx < 0:
            bullet.kill()

    if (bullet.rect.top < tileHeight or bullet.rect.bottom > mapHeight - tileHeight) or (bullet.rect.left < tileWidth or bullet.rect.right > mapWidth - tileWidth):
        bullet.kill()
        return

    if bullet.speedx > 0:
        upRightTileGid = map.tmxData.get_tile_gid((bullet.rect.right + bullet.speedx)/tileWidth, bullet.rect.top/tileHeight, COLLISION_LAYER)
        downRightTileGid = map.tmxData.get_tile_gid((bullet.rect.right + bullet.speedx)/tileWidth, (bullet.rect.bottom-1)/tileHeight, COLLISION_LAYER)

        if (upRightTileGid  == self.map.solidGID or downRightTileGid  == self.map.solidGID):
            bullet.kill()

    elif bullet.speedx < 0:
        upLeftTileGid = map.tmxData.get_tile_gid((bullet.rect.left + bullet.speedx)/tileWidth, bullet.rect.top/tileHeight, COLLISION_LAYER)
        downLeftTileGid = map.tmxData.get_tile_gid((bullet.rect.left + bullet.speedx)/tileWidth, (bullet.rect.bottom)/tileHeight, COLLISION_LAYER)

        if (upLeftTileGid  == self.map.solidGID or downLeftTileGid  == self.map.solidGID) and bullet.speedx < 0:
            bullet.kill()

def collisionBulletEnemy(bullet, map):
    collisionList = pygame.sprite.spritecollide(bullet, map.enemyGroup, False)
    for enemy in collisionList:
        bullet.detonate()

def collisionGrenadeEnemy(grenade, map):
    collisionList = pygame.sprite.spritecollide(grenade, map.enemyGroup, False)
    for enemy in collisionList:
        grenade.detonate()

def collisionBulletPlayer(map, player):
    collisionList = pygame.sprite.spritecollide(player, map.enemyBullet, False)
    for bullet in collisionList:
        player.hurt()
        bullet.kill()

def printTile(tile):
    if tile == self.map.solidGID:
        print('self.map.solidGID')
    elif tile == SPIKE:
        print('SPIKE')
    elif tile == SPRING:
        print('SPRING')
    else:
        print(tile)

def collisionExplosionEnemy(explosion, mapData):
    circle = Circle((explosion.collisionMask.rect.centerx, explosion.collisionMask.rect.centery),explosion.collisionMask.rect.width/2)

    for enemy in mapData.enemyGroup:
        if collisionCircleRect(circle, enemy.rect):
            enemy.hurt()


def collisionCircleRect(circle, rect):
    circleDistancex = abs(circle.x - rect.centerx)
    circleDistancey = abs(circle.y - rect.centery)

    if (circleDistancex > (rect.width/2 + circle.r)):
        return False
    if (circleDistancey > (rect.height/2 + circle.r)):
        return False

    if (circleDistancex <= (rect.width/2)):
        return True
    if (circleDistancey <= (rect.height/2)):
        return True

    cornerDistance_sq = (circleDistancex - rect.width/2)**2 + (circleDistancey - rect.height/2)**2

    return (cornerDistance_sq <= (circle.r**2))

def printTopTile(tile):
    if tile == self.map.solidGID:
        print("self.map.solidGID")
    elif tile == SPIKE:
        print("SPIKE")
    elif tile == SPRING:
        print("SPRING")
    elif tile == self.map.ladderGID:
        print("self.map.ladderGID")

def printJumpState(state):
    if state == GROUNDED:
        print("GROUNDED")
    elif state == JUMP:
        print("JUMP")
    elif state == CLIMBING:
        print("CLIMBING")

