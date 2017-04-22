from app.settings import *
from app.scene.titleScreen.TitleScreenData import TitleScreenData
from app.scene.titleScreen.TitleScreenLogicHandler import TitleScreenLogicHandler
from app.scene.whiteTitleScene.WhiteTitleSceneData import WhiteTitleSceneData
from app.scene.whiteTitleScene.WhiteTitleSceneLogicHandler import WhiteTitleSceneLogicHandler
from app.scene.platformScene.PlatformSceneLogicHandler import PlatformSceneLogicHandler
from app.scene.platformScene.PlatformSceneData import PlatformSceneData

from app.GameData import GameData

from scene.Scene import Scene


class SceneHandler:
    def __init__(self, screen):

        self.handlerRunning = True
        self.screen = screen
        self.gameData = GameData()

        titleScreenData = TitleScreenData()
        self.runningScene = Scene(self.screen, titleScreenData, TitleScreenLogicHandler(titleScreenData))

    def mainLoop(self):
        self.handlerRunning = True
        while self.handlerRunning:
            self.getNextScene()
            self.runningScene.run()

    def getNextScene(self,scene=None):
        # When we exit the scene, this code executes
        if self.runningScene.nextScene == TITLE_SCENE:
            titleScreenData = TitleScreenData()
            self.runningScene = Scene(self.screen, titleScreenData, TitleScreenLogicHandler(titleScreenData))
        elif self.runningScene.nextScene == WHITE_TITLE_SCENE:
            whiteTitleSceneData = WhiteTitleSceneData()
            self.runningScene = Scene(self.screen, whiteTitleSceneData, WhiteTitleSceneLogicHandler(whiteTitleSceneData))
        elif self.runningScene.nextScene == LEVEL_ONE_SCENE:
            self.gameData.mapData = PlatformSceneData("example_tiled", "InZone_01")
            self.runningScene = Scene(self.screen, self.gameData.mapData, PlatformSceneLogicHandler(self.gameData),self.gameData,self.gameData.mapData.player)