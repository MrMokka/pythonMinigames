import random
import pygame

from Menu.InformalGame import InformalGame
from Minesweeper.Cell import Cell

cells = []
cellSize = 20
cellGrid = (10, 10)
maxBombs = 10


def createPlayArea(screenSize) -> pygame.Rect:
    maxRectSize = pygame.Rect(0, 50, screenSize[0], screenSize[1])
    initRect = pygame.Rect(0, 0, cellSize * (cellGrid[0]), cellSize * (cellGrid[1]))
    initRect.center = (screenSize[0] / 2, screenSize[1] / 2)
    playArea = initRect.fit(maxRectSize)
    print(playArea)
    return playArea


class Minesweeper(InformalGame):

    def __init__(self, font, screenSize):
        self.roundActive = True
        self.font = pygame.font.SysFont('arial', 16)
        self.playArea = createPlayArea(screenSize)
        # self.playArea = pygame.Rect(0, 0, cellSize * (cellGrid[0]), cellSize * (cellGrid[1]))
        # self.playArea.center = (screenSize[0] / 2, screenSize[1] / 2)
        global cellSize
        cellSize = (self.playArea.width / cellGrid[0])
        self.resetGame()
        self.placeMines()

    def eventLoop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.mouseClick(pos, pygame.mouse.get_pressed())

    def resetGame(self):
        # Create cells
        for y in range(0, cellGrid[0]):
            column = []
            for x in range(0, cellGrid[1]):
                column.append(
                    Cell(x, y, self.playArea.x + (x * cellSize), self.playArea.y + (y * cellSize), cellSize, self.font))
            cells.append(column)

    def placeMines(self):
        # Add bombs to cells
        bombCount = 0
        while bombCount < maxBombs:
            x = random.randint(0, cellGrid[0] - 1)
            y = random.randint(0, cellGrid[1] - 1)
            if not cells[y][x].isMine():
                cells[y][x].setMine()
                bombCount += 1
                # Add value on neighbours
                for i in range(-1, 2):
                    for l in range(-1, 2):
                        if not (i == 0 and l == 0):
                            if (y + i) >= 0 and (x + l) >= 0:
                                if (y + i) < cellGrid[0] and (x + l) < cellGrid[1]:
                                    cells[y + i][x + l].addValue()

    def mouseClick(self, pos, button):
        clickPos = ((pos[0] - self.playArea.x) // cellSize, (pos[1] - self.playArea.y) // cellSize)
        if self.roundActive:
            cellClicked = self.getClickedCell(clickPos[0], clickPos[1])
            if cellClicked is None:
                print("Dint find cell clicked...")
            elif button[0]:
                result = cellClicked.openCell()  # 1 = open, 0 = nothing, -1 = mine
                if result == 1:
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
                cellClicked.flagCell()

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
                                    if targetCell.getValue() == 0:
                                        pass
                                        self.openNeighbours(x + baseX, y + baseY)

    def drawLoop(self, screen):
        # pygame.draw.rect(screen, (255, 0, 0), self.playArea)
        for column in cells:
            for cell in column:
                cell.draw(screen)

    def getClickedCell(self, x, y) -> Cell:
        if 0 <= x < cellGrid[0] and 0 <= y < cellGrid[1]:
            return cells[int(y)][int(x)]
        return None
