import random
import pygame
import sys

from Menu.InformalGame import InformalGame
from Minesweeper.Cell import Cell
from Minesweeper.Button import Button

cells = []
cellSize = 20
cellGrid = (10, 10)  # Don't make too large please..
mineCells = []
maxBombs = 10

sys.setrecursionlimit(cellGrid[0] * cellGrid[1])


def createPlayArea(screenSize) -> pygame.Rect:
    maxRectSize = pygame.Rect(0, 80, screenSize[0], screenSize[1] - 100)
    initRect = pygame.Rect(0, 0, cellSize * (cellGrid[0]), cellSize * (cellGrid[1]))
    playArea = initRect.fit(maxRectSize)
    playArea.width += 1
    playArea.height += 1
    print(playArea)
    return playArea


class Minesweeper(InformalGame):

    def __init__(self, screenSize):
        self.roundActive = True
        self.playArea = createPlayArea(screenSize)
        # self.playArea = pygame.Rect(0, 0, cellSize * (cellGrid[0]), cellSize * (cellGrid[1]))
        # self.playArea.center = (screenSize[0] / 2, screenSize[1] / 2)
        global cellSize
        cellSize = int(self.playArea.width / cellGrid[0])
        print("CellSize: " + str(cellSize))
        print("CellGrid: " + str(cellGrid[0]))
        self.font = pygame.font.SysFont('arial', int(cellSize / 2))
        self.resetGame()
        self.cellsOpened = 0
        self.resetButton = Button(10, 10, 40, 40)

    def eventLoop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.mouseClick(pos, pygame.mouse.get_pressed())

    def resetGame(self):
        global cells
        cells = []
        for y in range(0, cellGrid[1]):
            column = []
            for x in range(0, cellGrid[0]):
                column.append(
                    Cell(x, y, self.playArea.x + (x * cellSize), self.playArea.y + (y * cellSize), cellSize, self.font))
            cells.append(column)
        self.cellsOpened = 0
        self.roundActive = True
        self.placeMines()

    def placeMines(self):
        # Add bombs to cells
        bombCount = 0
        while bombCount < maxBombs:
            x = random.randint(0, cellGrid[0] - 1)
            y = random.randint(0, cellGrid[1] - 1)
            if not cells[y][x].isMine():
                cells[y][x].setMine()
                mineCells.append(cells[y][x])
                bombCount += 1
                # Add value on neighbours
                for i in range(-1, 2):
                    for l in range(-1, 2):
                        if not (i == 0 and l == 0):
                            if (y + i) >= 0 and (x + l) >= 0:
                                if (y + i) < cellGrid[1] and (x + l) < cellGrid[0]:
                                    cells[y + i][x + l].addValue()

    def mouseClick(self, pos, button):
        if self.checkButtonsClicked(pos, button):
            return
        clickPos = ((pos[0] - self.playArea.x) // cellSize, (pos[1] - self.playArea.y) // cellSize)
        if self.roundActive:
            cellClicked = self.getClickedCell(clickPos[0], clickPos[1])
            if cellClicked is None:
                print("Dint find cell clicked...")
            elif button[0]:
                result = cellClicked.openCell()  # 1 = open, 0 = nothing, -1 = mine
                if result == 1:
                    self.cellsOpened += 1
                    if cellClicked.getValue() == 0:
                        cellPos = cellClicked.getIndex()
                        self.openNeighbours(cellPos[0], cellPos[1])
                elif result == -1:
                    # Game Over
                    self.roundActive = False
                    for column in cells:
                        for cell in column:
                            if cell.isMine():
                                cell.openCell()
            elif button[2]:
                cellClicked.flagCell(None)
            if self.cellsOpened == (cellGrid[0] * cellGrid[1]) - maxBombs:  # Gamve over, victory
                for cell in mineCells:
                    cell.flagCell(True)
                self.roundActive = False
                print("Game Completed!")

    def openNeighbours(self, baseX, baseY):
        for y in range(-1, 2):
            for x in range(-1, 2):
                if not (x == 0 and y == 0):
                    if (y + baseY) >= 0 and (x + baseX) >= 0:
                        if (y + baseY) < cellGrid[1] and (x + baseX) < cellGrid[0]:
                            targetCell = cells[y + baseY][x + baseX]
                            if not targetCell.isMine():
                                if not targetCell.isOpen():
                                    targetCell.openCell()
                                    self.cellsOpened += 1
                                    if targetCell.getValue() == 0:
                                        pass
                                        self.openNeighbours(x + baseX, y + baseY)

    def checkButtonsClicked(self, pos, button):
        x, y = pos
        if button[0]:
            if self.resetButton.rect.collidepoint(x, y):
                self.resetGame()
                print("Game reset!")
                return True
            return False
        return False

    def drawLoop(self, screen):
        # pygame.draw.rect(screen, (255, 0, 0), self.playArea)
        for column in cells:
            for cell in column:
                cell.draw(screen)
        # pygame.draw.rect(screen, (255, 0, 0), self.playArea)
        self.resetButton.draw(screen)

    def getClickedCell(self, x, y) -> Cell:
        if 0 <= x < cellGrid[0] and 0 <= y < cellGrid[1]:
            return cells[int(y)][int(x)]
        return None
