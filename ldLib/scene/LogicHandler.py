import pygame

class LogicHandler:
    def __init__(self,data):
        self.data = data
        self.nextScene = None

    def handle(self):
        self.data.allSprites.update()
        self.data.spritesHUD.update()