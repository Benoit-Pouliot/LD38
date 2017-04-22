# Imports
import os
import sys
import pygame

from app.sprites.Upgrade import Upgrade

from app.settings import *


class Shop(pygame.sprite.Sprite):
    def __init__(self,data):
        super().__init__()

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

        # POUR LA MUSIQUE
        # self.soundPaid = pygame.mixer.Sound(os.path.join('music_pcm', 'paidMoney.wav'))
        # self.soundPaid.set_volume(.25)
        # self.soundNotEM = pygame.mixer.Sound(os.path.join('music_pcm', 'notEnoughMoney.wav'))
        # self.soundNotEM.set_volume(.25)
        # self.menuSelect = pygame.mixer.Sound(os.path.join('music_pcm', 'menu_select.wav'))
        # self.menuSelect.set_volume(.25)

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
        self.addUpgrade('spring','pig',self.buySpring,516,SHOP_REPEATABLE)
        self.addUpgrade('ladder', 'pig', self.buyLadder, 888, SHOP_REPEATABLE)
        self.addUpgrade('antiGravity', 'pig', self.buyAntiGravity, 77, SHOP_REPEATABLE)

        self.addUpgrade('pickaxe', 'pig', self.buyPickaxe, 1, SHOP_AVAILABLE)
        self.addUpgrade('drill', 'pig', self.buyDrill, 2, SHOP_AVAILABLE)
        self.addUpgrade('dynamite', 'pig', self.buyDynamite, 3, SHOP_AVAILABLE)

    # Unlock what needs to be unlocked
        self.upgradeList['spring'].unlock = True
        self.upgradeList['ladder'].unlock = True
        self.upgradeList['antiGravity'].unlock = True

        self.upgradeList['pickaxe'].unlock = True
        self.upgradeList['dynamite'].unlock = True

    def addUpgrade(self,name,imageName,method,cost,boughtState):
        self.upgradeList[name] = Upgrade(name,imageName,method,cost,boughtState)
        item = self.upgradeList[name]
        self.data.shopGroup.add(item)
        self.data.notifySet.add(item)

    def checkNewLink(self,name):
        if name == 'pickaxe':
            self.upgradeList['drill'].unlock = True

    def buy(self,item):
        myUpgrade = self.upgradeList[item]
        if myUpgrade.unlock and myUpgrade.boughtState !=SHOP_SOLD_OUT:
            if self.data.money >=myUpgrade.cost:
                self.sold = True
                self.data.money -= myUpgrade.cost
            if self.sold == True:
                if myUpgrade.boughtState != SHOP_REPEATABLE:
                    myUpgrade.boughtState = SHOP_SOLD_OUT
                self.checkNewLink(item)
                self.sold = False

                #self.soundPaid.play()
            else:
                if TAG_MARIE == 1:
                    print('Not enough money')
                #self.soundNotEM.play()

    def buySpring(self):
        self.buy('spring')

    def buyAntiGravity(self):
        self.buy('antiGravity')

    def buyLadder(self):
        self.buy('ladder')

    def buyPickaxe(self):
        self.buy('pickaxe')

    def buyDrill(self):
        self.buy('drill')

    def buyDynamite(self):
        self.buy('dynamite')

    def doNothing(self):
        pass
        # print('You did nothing')
