import pygame

from Menu.InformalGame import InformalGame
from Minesweeper.Minesweeper import Minesweeper


class Menu:
    def __init__(self, screenSize):
        self.currentGame: InformalGame = Minesweeper(screenSize)

    def eventLoop(self, event):
        if not self.currentGame is None:
            self.currentGame.eventLoop(event)

    def logicLoop(self):
        if not self.currentGame is None:
            self.currentGame.logicLoop()

    def drawLoop(self, screen):
        if self.currentGame is None:
            pass # draw manu
        else:
            pass # draw game
        self.currentGame.drawLoop(screen)
