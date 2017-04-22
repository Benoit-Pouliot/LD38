from ldLib.scene.LogicHandler import LogicHandler
from app.settings import *
import pygame


class TitleSceneLogicHandler(LogicHandler):
    def __init__(self,data):
        super().__init__(data)

    def handle(self):
        super().handle()
        self.checkHighlight()

    def checkHighlight(self):
        mousePos = pygame.mouse.get_pos()
        for obj in self.data.notifySet:
            if obj.rect.collidepoint(mousePos):
                obj.isSelected = True
            else:
                obj.isSelected = False
