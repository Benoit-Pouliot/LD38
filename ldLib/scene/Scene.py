import pygame

from scene.EventHandler import EventHandler
from scene.Drawer import Drawer


class Scene:
    def __init__(self,screen,data,logicHandler,gameData=None, player = None):
        # Screen
        self.gameData = gameData
        self.nextScene = None

        self.screen = screen
        self.data = data
        self.player = player

        if player != None:
            self.data.allSprites.add(self.player)
            self.data.notifySet.add(self.player)

        if self.data.camera != None:
            self.camera = self.data.camera
            if player != None:
                self.data.camera.add(self.player)
        else:
            self.camera = None

        self.eventHandler = EventHandler()
        self.logicHandler = logicHandler
        self.drawer = Drawer()

    def mainLoop(self):
        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandler.eventHandle(self.data.notifySet)
            self.logicHandler.handle()
            if self.data.camera == None:
                self.drawer.draw(self.screen, self.data.allSprites, self.data.spritesHUD, self.player)
            else:
                self.drawer.draw(self.screen, self.data.camera, self.data.spritesHUD, self.player)
            self.nextScene = self.data.nextScene
            if self.nextScene != None:
                self.sceneRunning = False

    def run(self):
        self.mainLoop()