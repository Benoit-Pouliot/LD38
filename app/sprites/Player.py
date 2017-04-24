import pygame
import os

from app.settings import *
from app.sprites.CollisionMask import CollisionMask
from app.sprites.Target import Target
from app.sprites.Pickaxe import Pickaxe
from app.sprites.Drill import Drill
from app.sprites.items.Spring import Spring
from app.sprites.items.Dynamite import Dynamite
from app.sprites.RedTileMask import RedTileMask

from ldLib.tools.Cooldown import Cooldown
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, mapData):
        super().__init__()

        self.name = "player"

        self.imageBase = pygame.image.load(os.path.join('img', 'gnome_v1.png'))

        # Here we load all images
        self.imageShapeStillRight = pygame.image.load(os.path.join('img', 'gnome_side_v2.png'))
        self.imageShapeStillLeft = pygame.transform.flip(self.imageShapeStillRight, True, False)

        self.imageShapeWalkRight = list()
        self.imageShapeWalkRight.append(pygame.image.load(os.path.join('img', 'gnome_walk2.png')))
        self.imageShapeWalkRight.append(self.imageShapeStillRight)
        self.imageShapeWalkRight.append(pygame.image.load(os.path.join('img', 'gnome_walk1.png')))
        self.imageShapeWalkRight.append(self.imageShapeStillRight)

        self.imageShapeDigRight = list()
        self.imageShapeDigRight.append(pygame.image.load(os.path.join('img', 'gnome_pickaxe1.png')))
        self.imageShapeDigRight.append(pygame.image.load(os.path.join('img', 'gnome_pickaxe2.png')))
        self.imageShapeDigRight.append(pygame.image.load(os.path.join('img', 'gnome_pickaxe3.png')))
        self.imageShapeDigRight.append(pygame.image.load(os.path.join('img', 'gnome_walk1.png')))

        self.imageShapeDrillRight = list()
        self.imageShapeDrillRight.append(pygame.image.load(os.path.join('img', 'gnome_drill1.png')))
        self.imageShapeDrillRight.append(pygame.image.load(os.path.join('img', 'gnome_pickaxe3.png')))
        self.imageShapeDrillRight.append(pygame.image.load(os.path.join('img', 'gnome_drill2.png')))
        self.imageShapeDrillRight.append(pygame.image.load(os.path.join('img', 'gnome_pickaxe3.png')))

        self.imageShapeClimb = list()
        self.imageShapeClimb.append(pygame.image.load(os.path.join('img', 'gnome_climb1.png')))
        self.imageShapeClimb.append(pygame.image.load(os.path.join('img', 'gnome_climb2.png')))

        self.imageShapeJumpRight = list()
        self.imageShapeJumpRight.append(pygame.image.load(os.path.join('img', 'gnome_pickaxe1.png')))
        # self.imageShapeJumpRight.append(pygame.image.load(os.path.join('img', 'gnome_pickaxe1.png')))


        self.imageShapeWalkLeft = list()
        for k in range(0, len(self.imageShapeWalkRight)):
            self.imageShapeWalkLeft.append(pygame.transform.flip(self.imageShapeWalkRight[k], True, False))

        self.imageShapeDigLeft = list()
        for k in range(0, len(self.imageShapeDigRight)):
            self.imageShapeDigLeft.append(pygame.transform.flip(self.imageShapeDigRight[k], True, False))

        self.imageShapeDrillLeft = list()
        for k in range(0, len(self.imageShapeDrillRight)):
            self.imageShapeDrillLeft.append(pygame.transform.flip(self.imageShapeDrillRight[k], True, False))

        self.imageShapeJumpLeft = list()
        for k in range(0, len(self.imageShapeJumpRight)):
            self.imageShapeJumpLeft.append(pygame.transform.flip(self.imageShapeJumpRight[k], True, False))


        self.imageShapeLeft = None
        self.imageShapeRight = None

        self.setShapeImage()
        self.image = self.imageShapeRight

        self.imageTransparent = pygame.Surface((1,1))
        self.imageTransparent.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #To dodge rounding problems with rect
        self.x = x
        self.y = y
        self.pastFrameX = x
        self.pastFrameY = y

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 5
        self.maxSpeedyUp = 18
        self.maxSpeedyDown = 15
        self.maxSpeedyUpClimbing = 6
        self.maxSpeedyDownClimbing = 6
        self.accx = 2
        self.accy = 2
        self.jumpSpeed = -10

        self.isPhysicsApplied = False
        self.isGravityApplied = True
        self.isFrictionApplied = True
        self.isCollisionApplied = True
        self.jumpState = JUMP
        self.facingSide = RIGHT

        self.life = 1
        self.lifeMax = 1
        self.lifeMaxCap = 5
        self.isInvincible = False
        self.invincibleFrameCounter = [0,0] #Timer,flashes nb
        self.invincibleTimer = 20 #Must be even number
        self.invincibleNbFlashes = 5

        self.rightPressed = False
        self.leftPressed = False
        self.upPressed = False
        self.downPressed = False
        self.leftMousePressed = False
        self.rightMousePressed = False

        self.mapData = mapData

        self.isAlive = True
        self.springList = []

        self.target = Target(0, 0)
        invPix = pygame.Surface([1,1], pygame.SRCALPHA, 32)
        invPix = invPix.convert_alpha()
        self.target.imageOrig = invPix
        self.mapData.camera.add(self.target)

        self.LeftClickMode = PLAYER_DIG_MODE

        self.pickaxeCooldown = Cooldown(DIG_COOLDOWN)
        self.drillCooldown = Cooldown(DRILL_COOLDOWN)
        self.springCooldown = Cooldown(30)
        self.dynamiteCooldown = Cooldown(30)

        self.pickaxeObj = None
        self.drillObj = None

        self.pickaxeStrength=1
        self.drillStrength=0

        #Link your own sounds here
        #self.soundSpring = pygame.mixer.Sound(os.path.join('music_pcm', 'LvlUpFail.wav'))
        #self.soundBullet = pygame.mixer.Sound(os.path.join('music_pcm', 'Gun.wav'))
        #self.soundGetHit = pygame.mixer.Sound(os.path.join('music_pcm', 'brokenGlass.wav'))
        #self.soundSpring.set_volume(1)
        #self.soundBullet.set_volume(.3)
        #self.soundGetHit.set_volume(.3)

        # Image counter
        self.imageIterStateRight = 0
        self.imageIterStateLeft = 0
        self.imageWaitNextImage = 6
        self.imageIterWait = 0

        self.imageIterStateDig = 0
        self.imageDigWaitNextImage = DIG_COOLDOWN//4
        self.imageDigIterWait = 0

        self.imageIterStateDrill = 0
        self.imageDrillWaitNextImage = DRILL_COOLDOWN//4
        self.imageDrillIterWait = 0

        self.imageIterStateClimb = 0
        self.imageClimbWaitNextImage = 16
        self.imageClimbIterWait = 0

        self.imageIterStateJump = 0
        self.imageJumpWaitNextImage = 4
        self.imageJumpIterWait = 0

        self.modifierCMX = 11
        self.modifierCMY = 8
        self.collisionMask = CollisionMask(self.rect.x + self.modifierCMX, self.rect.y+self.modifierCMY, self.rect.width-2*self.modifierCMX, self.rect.height-self.modifierCMY)

        # music
        self.musicChanged = True
        self.musicMode = MUSIC_OFF
        self.musicMuted = False
        self.musicType = MUSIC_TYPE1
        self.musicName = {MUSIC_TYPE1: 'Main.mp3',
                          MUSIC_TYPE2: 'SubTheme.mp3'}

        # Sounds
        self.dictSound = {'spring': pygame.mixer.Sound(os.path.join('music', 'Trempo2.wav')),
                          'buy': pygame.mixer.Sound(os.path.join('music', 'Achat.wav')),
                          'pause': pygame.mixer.Sound(os.path.join('music', 'BruitPause.wav')),
                          'drill': pygame.mixer.Sound(os.path.join('music', 'Drill.wav')),
                          'explosion': pygame.mixer.Sound(os.path.join('music', 'ExplosionDynamite.wav')),
                          'notenoughtmoney': pygame.mixer.Sound(os.path.join('music', 'PasAssezDargent.wav')),
                          'pickaxe': pygame.mixer.Sound(os.path.join('music', 'Pickaxe.wav')),
                          'teleport': pygame.mixer.Sound(os.path.join('music', 'TuyeauVersLeHaut.wav'))}
        # quick set up of volume
        for key in self.dictSound:
            self.dictSound[key].set_volume(.3)
        self.dictSound['spring'].set_volume(.3)
        self.dictSound['pickaxe'].set_volume(.1)
        self.dictSound['drill'].set_volume(.1)


    def setShapeImage(self):
        self.imageShapeLeft = pygame.transform.flip(self.imageBase, True, False)
        self.imageShapeRight = self.imageBase

    def setPastFramePos(self):
        self.rect.x = self.pastFrameX
        self.rect.y = self.pastFrameY

    def update(self):
        self.pastFrameX = self.rect.x
        self.pastFrameY = self.rect.y
        self.capSpeed()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # self.updateAnimation()
        # if self.speedx > 0:
        #     self.image = self.imageShapeRight
        #     self.facingSide = RIGHT
        # if self.speedx < 0:
        #     self.image = self.imageShapeLeft
        #     self.facingSide = LEFT

        self.invincibleUpdate()
        self.updateCollisionMask()
        self.updatePressedKeys()
        self.updateJumpState()
        self.updateTarget()
        self.updateCooldowns()

        self.updateMusic()
        self.updateAnimation()


    def updateAnimation(self):
        # Animation movement
        self.imageIterWait = min(self.imageIterWait+1, 2*self.imageWaitNextImage)

        # Hack, we add the iterator for climbing only in movement
        if self.speedx != 0 or self.speedy != 0:
            self.imageClimbIterWait = min(self.imageClimbIterWait+1, 2*self.imageClimbWaitNextImage)

        # Hack, we add the iterator for jumping only in movement
        if self.speedx != 0 or self.speedy != 0:
            self.imageJumpIterWait = min(self.imageJumpIterWait+1, 2*self.imageJumpWaitNextImage)

        # Hack
        if self.pickaxeCooldown.isZero:
            self.imageIterStateDig = 0
            self.imageDigIterWait = 0
        if self.drillCooldown.isZero:
            self.imageIterStateDrill = 0
            self.imageDrillIterWait = 0


        # Only if in drilling
        if self.leftMousePressed and self.LeftClickMode == PLAYER_DRILL_MODE:
            if self.imageDrillIterWait >= self.imageDrillWaitNextImage:
                if self.facingSide == RIGHT:
                    self.imageIterStateDrill = (self.imageIterStateDrill+1) % len(self.imageShapeDrillRight)
                    self.image = self.imageShapeDrillRight[self.imageIterStateDrill]
                else:
                    self.imageIterStateDrill = (self.imageIterStateDrill+1) % len(self.imageShapeDrillRight)
                    self.image = self.imageShapeDrillLeft[self.imageIterStateDrill]
                self.imageDrillIterWait = 0
            else:
                self.imageDrillIterWait = self.imageDrillIterWait+1
        # Only if in digging
        elif self.LeftClickMode == PLAYER_DIG_MODE and not self.pickaxeCooldown.isZero:
            if self.imageDigIterWait >= self.imageDigWaitNextImage:
                if self.facingSide == RIGHT:
                    self.imageIterStateDig = (self.imageIterStateDig+1) % len(self.imageShapeDigRight)
                    self.image = self.imageShapeDigRight[self.imageIterStateDig]
                else:
                    self.imageIterStateDig = (self.imageIterStateDig+1) % len(self.imageShapeDigRight)
                    self.image = self.imageShapeDigLeft[self.imageIterStateDig]
                self.imageDigIterWait = 0
            else:
                self.imageDigIterWait = self.imageDigIterWait+1
        elif self.jumpState == CLIMBING:
            if self.imageClimbIterWait >= self.imageClimbWaitNextImage:
                self.imageIterStateClimb = (self.imageIterStateClimb+1) % len(self.imageShapeClimb)
                self.image = self.imageShapeClimb[self.imageIterStateClimb]
                self.imageClimbIterWait = 0
        elif self.jumpState == JUMP and self.speedx >= -1 and self.speedx <= 1:
            if self.imageJumpIterWait >= self.imageJumpWaitNextImage:
                self.imageIterStateJump = (self.imageIterStateJump+1) % len(self.imageShapeJumpRight)
                if self.facingSide == RIGHT:
                    self.image = self.imageShapeJumpRight[self.imageIterStateJump]
                else:
                    self.image = self.imageShapeJumpLeft[self.imageIterStateJump]
                self.imageJumpIterWait = 0
        elif self.speedx == 0:
            self.imageIterStateRight = 0
            self.imageIterStateLeft = 0
            if self.facingSide == RIGHT:
                self.image = self.imageShapeStillRight
            else:
                self.image = self.imageShapeStillLeft
        elif self.speedx <= 1 and self.speedx > 0:
            self.imageIterStateRight = 0
            self.imageIterStateLeft = 0
            self.image = self.imageShapeStillRight
            self.facingSide = RIGHT
        elif self.speedx >= -1 and self.speedx < 0:
            self.imageIterStateRight = 0
            self.imageIterStateLeft = 0
            self.image = self.imageShapeStillLeft
            self.facingSide = LEFT
        elif self.speedx > 1:
            self.imageIterStateLeft = 0
            self.facingSide = RIGHT
            if self.imageIterWait >= self.imageWaitNextImage:
                self.imageIterStateRight = (self.imageIterStateRight+1) % len(self.imageShapeWalkRight)
                self.image = self.imageShapeWalkRight[self.imageIterStateRight]
                self.imageIterWait = 0
        else: # self.speedx < -1:
            self.imageIterStateRight = 0
            self.facingSide = LEFT
            if self.imageIterWait >= self.imageWaitNextImage:
                self.imageIterStateLeft = (self.imageIterStateLeft+1) % len(self.imageShapeWalkLeft)
                self.image = self.imageShapeWalkLeft[self.imageIterStateLeft]
                self.imageIterWait = 0

    def updateCooldowns(self):
        if not self.pickaxeCooldown.isZero:
            self.mine()
        self.pickaxeCooldown.update()

        if not self.drillCooldown.isZero:
            self.drill()
        if self.drillCooldown.isZero and self.drillObj is not None:
            self.drillObj.kill()
            self.drillObj = None
        self.drillCooldown.update()
        self.springCooldown.update()
        self.dynamiteCooldown.update()

    def updateTarget(self):
        mousePos = pygame.mouse.get_pos()

        diffx = mousePos[0]+self.mapData.cameraPlayer.view_rect.x-self.rect.centerx
        diffy = mousePos[1]+self.mapData.cameraPlayer.view_rect.y-self.rect.centery

        self.target.rect.centerx = TARGET_DISTANCE*(diffx)/self.vectorNorm(diffx,diffy) + self.rect.centerx
        self.target.rect.centery = TARGET_DISTANCE*(diffy)/self.vectorNorm(diffx,diffy) + self.rect.centery

        self.target.powerx = (diffx)/self.vectorNorm(diffx,diffy)
        self.target.powery = (diffy)/self.vectorNorm(diffx,diffy)

        angleRad = math.atan2(diffy, diffx)
        self.target.image = pygame.transform.rotate(self.target.imageOrig, -angleRad/math.pi*180)

        # self.image = self.rot_center(self.imageBase, -angleRad/math.pi*180)
        #self.image = pygame.transform.rotate(self.imageBase, -angleRad/math.pi*180)

    def vectorNorm(self,x,y):
        return math.sqrt(x**2+y**2+EPS)

    def capSpeed(self):
        if self.jumpState == CLIMBING:
            if self.speedy > 0 and self.speedy > self.maxSpeedyDownClimbing:
                self.speedy = self.maxSpeedyDownClimbing
            if self.speedy < 0 and self.speedy < -self.maxSpeedyUpClimbing:
                self.speedy = -self.maxSpeedyUpClimbing

        if self.speedx > 0 and self.speedx > self.maxSpeedx:
            self.speedx = self.maxSpeedx
        if self.speedx < 0 and self.speedx < -self.maxSpeedx:
            self.speedx = -self.maxSpeedx
        if self.speedy > 0 and self.speedy > self.maxSpeedyDown:
            self.speedy = self.maxSpeedyDown
        if self.speedy < 0 and self.speedy < -self.maxSpeedyUp:
            self.speedy = -self.maxSpeedyUp

    def jump(self):
        if self.jumpState == GROUNDED:
            self.speedy = self.jumpSpeed
            self.jumpState = JUMP

    def updateSpeedRight(self):
        self.speedx += self.accx

    def updateSpeedLeft(self):
        self.speedx -= self.accx

    def updateSpeedUp(self):
        if self.jumpState == CLIMBING:
            self.speedy -= self.accy

    def updateSpeedDown(self):
        if self.jumpState == CLIMBING:
            self.speedy += self.accy

    def updateCollisionMask(self):
        self.collisionMask.rect.x = self.rect.x+self.modifierCMX
        self.collisionMask.rect.y = self.rect.y+self.modifierCMY

    def updateJumpState(self):
        if self.jumpState == CLIMBING:
            self.isGravityApplied = False
        else:
            self.isGravityApplied = True

    def gainLife(self):
        if self.life < self.lifeMax:
            self.life = self.lifeMax

    def gainLifeMax(self):
        if self.lifeMax < self.lifeMaxCap:
            self.lifeMax += 1
            self.life = self.lifeMax
        else:
            self.lifeMax = self.lifeMaxCap
            self.life = self.lifeMax

    def knockedBack(self):
        #Can break collision ATM
        if self.speedx == 0:
            self.speedx = self.maxSpeedx

        self.speedx = (-self.speedx/abs(self.speedx)) * self.maxSpeedx
        self.speedy = (-self.speedy/abs(self.speedx)) * self.maxSpeedx

    def invincibleOnHit(self):
        self.isInvincible = True
        self.invincibleFrameCounter[0] = 1

    def invincibleUpdate(self):
        if self.invincibleFrameCounter[0] > 0 and self.invincibleFrameCounter[1] < self.invincibleNbFlashes:
            self.invincibleFrameCounter[0] += 1
            if self.invincibleFrameCounter[0]== self.invincibleTimer:
                self.invincibleFrameCounter[0] = 1
                self.invincibleFrameCounter[1] +=1

        elif self.invincibleFrameCounter[1] == self.invincibleNbFlashes:
            self.isInvincible = False
            self.invincibleFrameCounter = [0,0]
        self.visualFlash()

    def createSpring(self):
        #self.stop()
        self.destroyStackedSpring()
        if self.mapData.nbSpring > 0 and self.springCooldown.isZero:

            x = self.target.rect.x - (self.target.rect.x % self.mapData.tmxData.tileheight)
            y = self.target.rect.y + (self.mapData.tmxData.tileheight - (self.target.rect.y % self.mapData.tmxData.tileheight) )

            spring = Spring(x, y)
            spring.rect.y -= spring.rect.height
            currentTile = self.mapData.tmxData.get_tile_gid(spring.rect.x/self.mapData.tmxData.tilewidth, spring.rect.y/self.mapData.tmxData.tileheight, COLLISION_LAYER)
            if currentTile == self.mapData.solidGID or currentTile == self.mapData.indestructibleGID:
                spring.kill()
                return
            col = pygame.sprite.spritecollide(spring, self.mapData.springGroup, False)
            if not col:
                self.mapData.allSprites.add(spring)
                self.mapData.springGroup.add(spring)
                self.mapData.camera.add(spring)
                self.mapData.nbSpring -= 1
                self.springList.append(spring)
                self.springCooldown.start()
                if not self.musicMuted:
                    self.dictSound['spring'].play(0)

    def destroyStackedSpring(self):
        for spring in self.mapData.springGroup.sprites():
            count = 0
            for otherSpring in self.mapData.springGroup.sprites():
                if spring.rect.x == otherSpring.rect.x and spring.rect.y == otherSpring.rect.y:
                    count += 1
                    if count == 2:
                        spring.kill()
                        break

    def createLadder(self):
        x = self.target.rect.centerx - (self.target.rect.centerx % self.mapData.tmxData.tileheight)
        y = self.target.rect.centery + (self.mapData.tmxData.tileheight - (self.target.rect.centery % self.mapData.tmxData.tileheight) )

        currentTile = self.mapData.tmxData.get_tile_gid(self.target.rect.centerx/self.mapData.tmxData.tilewidth, self.target.rect.centery/self.mapData.tmxData.tileheight, COLLISION_LAYER)

        if self.mapData.nbLadder > 0 and currentTile != self.mapData.solidGID and currentTile != self.mapData.indestructibleGID and currentTile != self.mapData.ladderGID:
            self.mapData.localTmxData.addTileXYToListToChange((self.target.rect.centerx,self.target.rect.centery), LADDER_TILE)
            self.mapData.localTmxData.addTileXYToListToChange((self.target.rect.centerx,self.target.rect.centery), LADDER, COLLISION_LAYER)
            self.mapData.localTmxData.changeAllTileInList(self.mapData.cameraPlayer)
            self.mapData.nbLadder -= 1

    def createDynamite(self):
        if self.mapData.nbDynamite > 0 and self.dynamiteCooldown.isZero:
            x = self.target.rect.centerx
            y = self.target.rect.centery

            currentTile = self.mapData.tmxData.get_tile_gid(x/self.mapData.tmxData.tilewidth, y/self.mapData.tmxData.tileheight, COLLISION_LAYER)

            if currentTile != self.mapData.solidGID and currentTile != self.mapData.indestructibleGID:
                dynamite = Dynamite(x, y, self.mapData)
                dynamite.rect.centerx = x
                dynamite.rect.centery = y

                col = pygame.sprite.spritecollide(dynamite, self.mapData.springGroup, False)
                if not col:
                    self.mapData.allSprites.add(dynamite)
                    self.mapData.camera.add(dynamite)
                    self.mapData.nbDynamite -= 1
                    self.dynamiteCooldown.start()

    def bounce(self, speed):
        self.speedy = -speed

        if not self.musicMuted:
            self.dictSound['spring'].play(0)
            # occupied = pygame.sprite.spritecollideany(barricade, self.mapData.enemyGroup)
            # if occupied is None:
            #     occupied = pygame.sprite.spritecollideany(barricade, self.mapData.obstacleGroup)
            #
            # if occupied is None:
            #     self.soundBarricade.play()
            #     self.mapData.camera.add(barricade)
            #     self.mapData.allSprites.add(barricade)
            #     self.mapData.obstacleGroup.add(barricade)
            #
            #     self.mapData.allSprites.add(barricade.lifeBar)
            #     self.mapData.camera.add(barricade.lifeBar, layer=CAMERA_HUD_LAYER)
            #
            #     self.barricadeCharges -= 1
            #
            #     if self.barricadeCooldown.isZero:
            #         self.barricadeCooldown.start()
            # else:
            #     barricade.destroy()

    def dead(self):
        self.isAlive = False

    def pickedPowerUpMaxHealth(self):
        self.gainLifeMax()

    def pickedPowerUpHealth(self):
        self.gainLife()

    def visualFlash(self):
        if self.invincibleFrameCounter[0] == 5:
            self.imageShapeLeft = self.imageTransparent
            self.imageShapeRight = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter[0] == 15:
            self.setShapeImage()
            if self.facingSide == RIGHT:
                self.image = self.imageShapeRight
            else:
                self.image = self.imageShapeLeft

    def spring(self):
        self.jumpState = JUMP
        self.speedy = -self.maxSpeedyUp

    def hurt(self):
        if not self.isInvincible:
            self.invincibleOnHit()
            self.visualFlash()

    def mine(self):

        if self.pickaxeCooldown.value == 1:
            if self.pickaxeObj is not None:
                self.pickaxeObj.kill()
                self.pickaxeObj = None

        if self.pickaxeCooldown.value == self.pickaxeCooldown.max-1:
            posX = self.target.rect.centerx/self.mapData.tmxData.tilewidth
            posY = self.target.rect.centery/self.mapData.tmxData.tileheight
            targetTile = self.mapData.tmxData.get_tile_gid(posX, posY, COLLISION_LAYER)

            if targetTile == self.mapData.solidGID:
                if not self.musicMuted:
                    self.dictSound['pickaxe'].play(0)
                if self.mapData.tileLife[self.target.rect.centerx//self.mapData.tmxData.tilewidth][self.target.rect.centery//self.mapData.tmxData.tileheight].life > self.pickaxeStrength:
                    self.mapData.tileLife[self.target.rect.centerx//self.mapData.tmxData.tilewidth][self.target.rect.centery//self.mapData.tmxData.tileheight].life -= self.pickaxeStrength
                    self.addRedTile(self.target.rect.centerx//self.mapData.tmxData.tilewidth, self.target.rect.centery//self.mapData.tmxData.tileheight, self.mapData.tileLife[self.target.rect.centerx//self.mapData.tmxData.tilewidth][self.target.rect.centery//self.mapData.tmxData.tileheight].life, self.mapData.tileLife[self.target.rect.centerx//self.mapData.tmxData.tilewidth][self.target.rect.centery//self.mapData.tmxData.tileheight].maxLife)
                else:

                    self.getGems(posX, posY)
                    self.mapData.tileLife[self.target.rect.centerx//self.mapData.tmxData.tilewidth][self.target.rect.centery//self.mapData.tmxData.tileheight].life = 0

                    self.mapData.localTmxData.addTileXYToListToChange((self.target.rect.centerx,self.target.rect.centery), 0)
                    self.mapData.localTmxData.addTileXYToListToChange((self.target.rect.centerx,self.target.rect.centery), 0, COLLISION_LAYER)
                    self.mapData.localTmxData.changeAllTileInList(self.mapData.cameraPlayer)
                    self.destroyRedTile(self.target.rect.centerx//self.mapData.tmxData.tilewidth, self.target.rect.centery//self.mapData.tmxData.tileheight)

            if self.facingSide == RIGHT:
                self.image = self.imageShapeDigRight[self.imageIterStateDig]
            else:
                self.image = self.imageShapeDigLeft[self.imageIterStateDig]
            self.pickaxeObj = Pickaxe(0, 0, self,self.mapData.lvlPickaxe)
            self.mapData.camera.add(self.pickaxeObj)

        if self.pickaxeCooldown.value < self.pickaxeCooldown.max-1 and self.pickaxeObj is not None:
            self.pickaxeObj.updatePickaxe()
        if self.pickaxeCooldown.value == 1:
            if self.pickaxeObj is not None:
                self.pickaxeObj.kill()
                self.pickaxeObj = None


    def addRedTile(self, posx, posy, life, maxLife):
        x = posx * self.mapData.tmxData.tilewidth
        y = posy * self.mapData.tmxData.tileheight

        for mask in self.mapData.redTileMaskGroup.sprites():
            if mask.rect.x == x and mask.rect.y == y and mask.life > life:
                mask.kill()

        redTileMask = RedTileMask(x, y, life, maxLife)
        self.mapData.redTileMaskGroup.add(redTileMask)
        self.mapData.camera.add(redTileMask)

    def destroyRedTile(self, posx, posy):
        x = posx * self.mapData.tmxData.tilewidth
        y = posy * self.mapData.tmxData.tileheight

        for mask in self.mapData.redTileMaskGroup.sprites():
            if mask.rect.x == x and mask.rect.y == y:
                mask.kill()

    def drill(self):
        # We add the sprite
        if self.drillCooldown.value == self.drillCooldown.max-1:
            if self.facingSide == RIGHT:
                self.image = self.imageShapeDrillRight[self.imageIterStateDig]
            else:
                self.image = self.imageShapeDrillLeft[self.imageIterStateDig]

            if self.drillObj is not None:
                self.drillObj.kill()
                self.drillObj = None
            self.drillObj = Drill(0, 0, self, self.mapData.lvlDrill)
            self.mapData.camera.add(self.drillObj)
            if not self.musicMuted:
                    self.dictSound['drill'].play(0, int(DRILL_COOLDOWN/FPS*1000))

        if self.drillCooldown.value < self.drillCooldown.max-1 and self.drillObj is not None:
            self.drillObj.updateDrill()

        if self.drillCooldown.value == 1:
            if self.facingSide == RIGHT:
                widthSide = self.mapData.tmxData.tilewidth
            else:
                widthSide = -self.mapData.tmxData.tilewidth

            posX = (self.rect.centerx+widthSide)/self.mapData.tmxData.tilewidth
            posY = self.rect.centery/self.mapData.tmxData.tileheight
            sideTile = self.mapData.tmxData.get_tile_gid(posX, posY, COLLISION_LAYER)
            if sideTile == self.mapData.solidGID:
                if self.mapData.tileLife[(self.rect.centerx+widthSide)//self.mapData.tmxData.tilewidth][self.rect.centery//self.mapData.tmxData.tileheight].life > self.drillStrength:
                    self.mapData.tileLife[(self.rect.centerx+widthSide)//self.mapData.tmxData.tilewidth][self.rect.centery//self.mapData.tmxData.tileheight].life -= self.drillStrength
                    self.addRedTile((self.rect.centerx+widthSide)//self.mapData.tmxData.tilewidth, self.rect.centery//self.mapData.tmxData.tileheight, self.mapData.tileLife[(self.rect.centerx+widthSide)//self.mapData.tmxData.tilewidth][self.rect.centery//self.mapData.tmxData.tileheight].life, self.mapData.tileLife[(self.rect.centerx+widthSide)//self.mapData.tmxData.tilewidth][self.rect.centery//self.mapData.tmxData.tileheight].maxLife)
                else:
                    ## get the gems1
                    self.getGems(posX, posY)
                    self.mapData.tileLife[(self.rect.centerx+widthSide)//self.mapData.tmxData.tilewidth][self.rect.centery//self.mapData.tmxData.tileheight].life = 0
                    self.mapData.localTmxData.addTileXYToListToChange(((self.rect.centerx+widthSide),self.rect.centery), 0)
                    self.mapData.localTmxData.addTileXYToListToChange(((self.rect.centerx+widthSide),self.rect.centery), 0, COLLISION_LAYER)
                    self.mapData.localTmxData.changeAllTileInList(self.mapData.cameraPlayer)
                    self.destroyRedTile((self.rect.centerx+widthSide)//self.mapData.tmxData.tilewidth, self.rect.centery//self.mapData.tmxData.tileheight)

    def getGems(self, x, y):
        targetTileType = self.mapData.localTmxData.get_tileType(x, y, TERRAIN_LAYER)
        try:
            nameGem = ID_GEM[targetTileType - NB_TSET]
            if nameGem == 'GOLD1': self.mapData.money += VAL_GOLD1
            elif nameGem == 'GOLD2': self.mapData.money += VAL_GOLD2
            elif nameGem == 'PINK1': self.mapData.money += VAL_PINK1
            elif nameGem == 'PINK2': self.mapData.money += VAL_PINK2
            elif nameGem == 'GREEN1': self.mapData.money += VAL_GREEN1
            elif nameGem == 'GREEN2': self.mapData.money += VAL_GREEN2
            elif nameGem == 'RED1': self.mapData.money += VAL_RED1
            elif nameGem == 'RED2': self.mapData.money += VAL_RED2
        except KeyError:
            pass

    def setStrength(self):
        self.pickaxeStrength = PICKAXE_STRENGTH_LEVEL[self.mapData.lvlPickaxe]
        self.drillStrength = DRILL_STRENGTH_LEVEL[self.mapData.lvlDrill]
        self.dynamiteStrength = DYNAMITE_STRENGTH_LEVEL[self.mapData.lvlDynamite]

    def updateMusic(self):

        if self.musicType == MUSIC_TYPE1 and self.rect.centery > MUSIC_HEIGHT_SWITCH:
            self.musicType = MUSIC_TYPE2
            self.musicMode = MUSIC_OFF
            self.musicChanged = True
        if self.musicType == MUSIC_TYPE2 and self.rect.centery < MUSIC_HEIGHT_SWITCH:
            self.musicType = MUSIC_TYPE1
            self.musicMode = MUSIC_OFF
            self.musicChanged = True
        if self.musicChanged:
            self.musicChanged = False
            if self.musicMode == MUSIC_OFF:
                self.musicMode = MUSIC_ON
                pygame.mixer.music.load(os.path.join('music', self.musicName[self.musicType]))
                if not self.musicMuted:
                    pygame.mixer.music.set_volume(0.5)
                elif self.musicMuted:
                    pygame.mixer.music.set_volume(0)
                pygame.mixer.music.play(-1)
            elif not self.musicMuted:
                pygame.mixer.music.set_volume(0.5)
            elif self.musicMuted:
                pygame.mixer.music.set_volume(0)

    def notify(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.updateSpeedRight()
                self.rightPressed = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.updateSpeedLeft()
                self.leftPressed = True
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.jump()
                self.updateSpeedUp()
                self.upPressed = True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.updateSpeedDown()
                self.downPressed = True
            elif event.key == pygame.K_SPACE:
                self.jump()
            elif event.key == pygame.K_c:
                self.createLadder()
            elif event.key == pygame.K_v:
                self.createDynamite()
            elif event.key == pygame.K_1:
                self.LeftClickMode = PLAYER_DIG_MODE
            elif event.key == pygame.K_2:
                if self.mapData.lvlDrill is not 0:
                    self.LeftClickMode = PLAYER_DRILL_MODE
            # elif event.key == pygame.K_3:
            #     self.LeftClickMode = PLAYER_DYNAMITE_MODE
            elif event.key == pygame.K_m:
                if not self.musicMuted:
                    self.musicMuted = True
                    self.musicChanged = True
                elif self.musicMuted:
                    self.musicMuted = False
                    self.musicChanged = True


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE_LEFT:
                self.leftMousePressed = True
            elif event.button == MOUSE_RIGHT:
                self.rightMousePressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == MOUSE_LEFT:
                self.leftMousePressed = False
            elif event.button == MOUSE_RIGHT:
                self.rightMousePressed = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.rightPressed = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.leftPressed = False
            elif event.key == pygame.K_UP  or event.key == pygame.K_w:
                self.upPressed = False
            elif event.key == pygame.K_DOWN  or event.key == pygame.K_s:
                self.downPressed = False

    def updatePressedKeys(self):
        if self.rightPressed:
            self.updateSpeedRight()
        if self.leftPressed:
            self.updateSpeedLeft()
        if self.upPressed:
            self.updateSpeedUp()
        if self.downPressed:
            self.updateSpeedDown()
        if self.leftMousePressed:
            if self.LeftClickMode == PLAYER_DIG_MODE:
                if self.pickaxeCooldown.isZero:
                    self.pickaxeCooldown.start()
            if self.LeftClickMode == PLAYER_DRILL_MODE:
                if self.drillCooldown.isZero:
                    self.drillCooldown.start()
        if self.rightMousePressed:
            self.createSpring()

