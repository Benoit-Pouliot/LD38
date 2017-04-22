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

        # POUR LA MUSIQUE
        # self.soundPaid = pygame.mixer.Sound(os.path.join('music_pcm', 'paidMoney.wav'))
        # self.soundPaid.set_volume(.25)
        # self.soundNotEM = pygame.mixer.Sound(os.path.join('music_pcm', 'notEnoughMoney.wav'))
        # self.soundNotEM.set_volume(.25)
        # self.menuSelect = pygame.mixer.Sound(os.path.join('music_pcm', 'menu_select.wav'))
        # self.menuSelect.set_volume(.25)

        #MusicFactory(SHOP_SCREEN)

    def addUpgrades(self):
        self.addUpgrade('pig','pig',self.buyPig,100,(100,100))

    def addUpgrade(self,name,imageName,method,cost,pos):
        self.upgradeList[name] = Upgrade(name,imageName,method,cost)

        item = self.upgradeList[name]

        self.data.shopGroup.add(item)
        self.data.spritesHUD.add(item)
        self.data.notifySet.add(item)

        item.rect.x = pos[0]
        item.rect.y = pos[1]

    def buy(self,item):
        if self.data.money >=self.upgradeList[item].cost:
            self.sold = True
            self.data.money -= self.upgradeList[item].cost
        if self.sold == True:
            self.sold = False
            #self.soundPaid.play()
        else:
            if TAG_MARIE == 1:
                print('Not enough money')
            #self.soundNotEM.play()

    def buyPig(self):
        self.buy('pig')

    def doNothing(self):
        pass
        # print('You did nothing')
