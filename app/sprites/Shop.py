# Imports
import os
import sys
import pygame

from app.sprites.Upgrade import Upgrade

from app.settings import *


class Shop(pygame.sprite.Sprite):
    def __init__(self,data):
        super().__init__()

        self.name = 'shop'

        self.image = pygame.Surface([SCREEN_WIDTH*4/5, SCREEN_WIDTH*2/5], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH/10
        self.rect.y = SCREEN_HEIGHT/10

        self.data = data

        self.upgradeList = {}

        self.addUpgrades()

        self.sold = False

        self.positionUpgrade()

        self.isGravityApplied = False
        self.isPhysicsApplied = False
        self.isCollisionApplied = False

        # POUR LA MUSIQUE
        # self.soundPaid = pygame.mixer.Sound(os.path.join('music_pcm', 'paidMoney.wav'))
        # self.soundPaid.set_volume(.25)
        # self.soundNotEM = pygame.mixer.Sound(os.path.join('music_pcm', 'notEnoughMoney.wav'))
        # self.soundNotEM.set_volume(.25)
        # self.menuSelect = pygame.mixer.Sound(os.path.join('music_pcm', 'menu_select.wav'))
        # self.menuSelect.set_volume(.25)

        self.dictSound = {'buy': pygame.mixer.Sound(os.path.join('music', 'Achat.wav')),
                          'notenoughtmoney': pygame.mixer.Sound(os.path.join('music', 'PasAssezDargent.wav'))}
        # quick set up of volume
        for key in self.dictSound:
            self.dictSound[key].set_volume(.1)

        #MusicFactory(SHOP_SCREEN)
    def update(self):
        self.positionUpgrade()

    def positionUpgrade(self):
        itemPosLeft = SCREEN_WIDTH/8-10
        itemPosTop = SCREEN_HEIGHT/8

        #Clear upgrade of sprite group and notify set
        for sprites in self.data.shopGroup:
            if self.data.spritesHUD.has(sprites):
                self.data.spritesHUD.remove(sprites)
                self.data.notifySet.remove(sprites)

        for key in self.upgradeList:
            item = self.upgradeList[key]
            if item.unlock and item.boughtState != SHOP_SOLD_OUT:
                item.rect.x = itemPosLeft
                item.rect.y = itemPosTop
                self.data.spritesHUD.add(item)
                self.data.notifySet.add(item)

                itemPosLeft+= UPGRADE_SIZE+10

    def addUpgrades(self):
        self.addUpgrade('spring','trempo1',self.buySpring,SPRING_COST,SHOP_REPEATABLE)
        self.addUpgrade('ladder', 'ladder', self.buyLadder, LADDER_COST, SHOP_REPEATABLE)

        # self.addUpgrade('antiGravity', 'antiGravity', self.buyAntiGravity, ANTI_GRAVITY_COST, SHOP_REPEATABLE)

        self.addUpgrade('pickaxeLvl2', 'pickaxeLvl2', self.buyPickaxe2, PICKAXE_LVL_COST[2], SHOP_AVAILABLE)
        self.addUpgrade('pickaxeLvl3', 'pickaxeLvl3', self.buyPickaxe3, PICKAXE_LVL_COST[3], SHOP_AVAILABLE)
        self.addUpgrade('pickaxeLvl4', 'pickaxeLvl4', self.buyPickaxe4, PICKAXE_LVL_COST[4], SHOP_AVAILABLE)

        self.addUpgrade('drillLvl1', 'drillLvl1-a', self.buyDrill1, DRILL_LVL_COST[1], SHOP_AVAILABLE)
        self.addUpgrade('drillLvl2', 'drillLvl2-a', self.buyDrill2, DRILL_LVL_COST[2], SHOP_AVAILABLE)
        self.addUpgrade('drillLvl3', 'drillLvl3-a', self.buyDrill3, DRILL_LVL_COST[3], SHOP_AVAILABLE)

        self.addUpgrade('dynamiteLvl1', 'dynamiteLvl1', self.buyDynamite1, DYNAMITE_LVL_COST, SHOP_REPEATABLE)

        # Unlock what needs to be unlocked
        self.upgradeList['spring'].unlock = True
        self.upgradeList['ladder'].unlock = True

        # self.upgradeList['antiGravity'].unlock = True

        self.upgradeList['pickaxeLvl2'].unlock = True
        self.upgradeList['drillLvl1'].unlock = True
        self.upgradeList['dynamiteLvl1'].unlock = True

    def addUpgrade(self,name,imageName,method,cost,boughtState):
        self.upgradeList[name] = Upgrade(name,imageName,method,cost,boughtState)
        item = self.upgradeList[name]
        self.data.shopGroup.add(item)

    def checkNewLink(self,name):
        if name == 'pickaxeLvl2':
            self.upgradeList['pickaxeLvl3'].unlock = True
        if name == 'pickaxeLvl3':
            self.upgradeList['pickaxeLvl4'].unlock = True
        if name == 'drillLvl1':
            self.upgradeList['drillLvl2'].unlock = True
        if name == 'drillLvl2':
            self.upgradeList['drillLvl3'].unlock = True

    def buy(self,item):
        myUpgrade = self.upgradeList[item]
        if myUpgrade.unlock and myUpgrade.boughtState !=SHOP_SOLD_OUT:
            if self.data.money >=myUpgrade.cost:
                self.sold = True
                self.data.money -= myUpgrade.cost
                if not self.data.player.musicMuted:
                    self.dictSound['buy'].play(0)
            if self.sold == True:
                if myUpgrade.boughtState != SHOP_REPEATABLE:
                    myUpgrade.boughtState = SHOP_SOLD_OUT
                self.checkNewLink(item)

                #self.soundPaid.play()
            else:
                if not self.data.player.musicMuted:
                    self.dictSound['notenoughtmoney'].play(0)
                #self.soundNotEM.play()

    def buySpring(self):
        self.buy('spring')
        if self.sold:
            self.data.nbSpring += 3
            self.data.player.RightClickMode = PLAYER_SPRING_MODE
            self.sold = False

    def buyAntiGravity(self):
        self.buy('antiGravity')
        if self.sold:
            self.data.nbAntiGravity += 10
            self.data.player.RightClickMode = PLAYER_ANTI_MODE
            self.sold = False

    def buyLadder(self):
        self.buy('ladder')
        if self.sold:
            self.data.nbLadder += 10
            self.data.player.RightClickMode = PLAYER_LADDER_MODE
            self.sold = False

    def buyPickaxe2(self):
        self.buy('pickaxeLvl2')
        if self.sold:
            self.data.lvlPickaxe += 1
            self.data.player.LeftClickMode = PLAYER_DIG_MODE
            self.data.player.setStrength()
            self.sold = False

    def buyPickaxe3(self):
        self.buy('pickaxeLvl3')
        if self.sold:
            self.data.lvlPickaxe += 1
            self.data.player.LeftClickMode = PLAYER_DIG_MODE
            self.data.player.setStrength()
            self.sold = False

    def buyPickaxe4(self):
        self.buy('pickaxeLvl4')
        if self.sold:
            self.data.lvlPickaxe += 1
            self.data.player.LeftClickMode = PLAYER_DIG_MODE
            self.data.player.setStrength()
            self.sold = False

    def buyDrill1(self):
        self.buy('drillLvl1')
        if self.sold:
            self.data.lvlDrill += 1
            self.data.player.LeftClickMode = PLAYER_DRILL_MODE
            self.data.player.setStrength()
            self.sold = False

    def buyDrill2(self):
        self.buy('drillLvl2')
        if self.sold:
            self.data.lvlDrill += 1
            self.data.player.LeftClickMode = PLAYER_DRILL_MODE
            self.data.player.setStrength()
            self.sold = False

    def buyDrill3(self):
        self.buy('drillLvl3')
        if self.sold:
            self.data.lvlDrill += 1
            self.data.player.LeftClickMode = PLAYER_DRILL_MODE
            self.data.player.setStrength()
            self.sold = False

    def buyDynamite1(self):
        self.buy('dynamiteLvl1')
        if self.sold:
            self.data.nbDynamite += 1
            self.data.player.RightClickMode = PLAYER_DYNAMITE_MODE
            self.data.player.setStrength()
            self.sold = False

    # def buyDynamite2(self):
    #     self.buy('dynamiteLvl2')
    #     if self.sold:
    #         self.data.lvlDynamite += 1
    #         self.data.player.setStrength()
    #         self.sold = False

    def doNothing(self):
        pass
        # print('You did nothing')
