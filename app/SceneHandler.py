from app.settings import *
from app.scene.titleScene.TitleSceneData import TitleSceneData
from app.scene.titleScene.TitleSceneLogicHandler import TitleSceneLogicHandler
from app.scene.titleScene.InstructionSceneData import InstructionSceneData
from app.scene.titleScene.CreditSceneData import CreditSceneData
from app.scene.gameScene.GameSceneLogicHandler import GameSceneLogicHandler
from app.scene.gameScene.GameSceneData import GameSceneData

from app.GameData import GameData

from ldLib.scene.Scene import Scene
from app.settings import *

class SceneHandler:
    def __init__(self, screen):

        self.handlerRunning = True
        self.screen = screen
        self.gameData = GameData()

        self.gameData.data = TitleSceneData()
        self.runningScene = Scene(self.screen, self.gameData, TitleSceneLogicHandler(self.gameData))

    def mainLoop(self):
        self.handlerRunning = True
        while self.handlerRunning:
            self.getNextScene()
            self.runningScene.run()

    def getNextScene(self,scene=None):
        # When we exit the scene, this code executes
        if self.runningScene.nextScene == TITLE_SCENE:
            self.gameData.data = TitleSceneData()
            self.runningScene = Scene(self.screen, self.gameData, TitleSceneLogicHandler(self.gameData))
        elif self.runningScene.nextScene == INSTRUCTION_SCENE:
            self.gameData.data = InstructionSceneData()
            self.runningScene = Scene(self.screen, self.gameData, TitleSceneLogicHandler(self.gameData))
        elif self.runningScene.nextScene == CREDIT_SCENE:
            self.gameData.data = CreditSceneData()
            self.runningScene = Scene(self.screen, self.gameData, TitleSceneLogicHandler(self.gameData))
        elif self.runningScene.nextScene == GAME_SCENE:


            # self.gameData.data = GameSceneData("tiled_map1", "InZone_01")

            self.gameData.data = GameSceneData("world", "InZone_01")

            self.runningScene = Scene(self.screen, self.gameData, GameSceneLogicHandler(self.gameData))