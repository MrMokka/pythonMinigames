import random
import pygame
import sys

from Menu import InformalGame
from Minesweeper.Cell import Cell
from Minesweeper.Button import Button
from Minesweeper.Text import Text

cells = []
cellSize = 20
cellGrid = (16, 16)  # Don't make too large please..
mineCells = []
maxBombs = 30

sys.setrecursionlimit(cellGrid[0] * cellGrid[1])


def createPlayArea(screenSize) -> pygame.Rect:
    maxRectSize = pygame.Rect(0, 80, screenSize[0], screenSize[1] - 100)
    initRect = pygame.Rect(0, 0, cellSize * (cellGrid[0]), cellSize * (cellGrid[1]))
    playArea = initRect.fit(maxRectSize)
    playArea.width += 1
    playArea.height += 1
    print("Play area: " + str(playArea))
    return playArea


def drawText(screen, border, text):
    textRect = text.get_rect()
    textRect.center = border.center
    screen.blit(text, textRect)


class Minesweeper(InformalGame.InformalGame):

    def __init__(self, screenSize):
        self.roundActive = True
        self.playArea = createPlayArea(screenSize)
        global cellSize
        cellSize = int(self.playArea.width / cellGrid[0])
        print("CellSize: " + str(cellSize))
        self.font = pygame.font.SysFont('arial', int(cellSize / 2))
        self.cellsOpened = 0
        self.resetButton = Button(10, 10, 40, 40)
        self.resetButton.setColors((255, 0, 0))
        self.bombCounter = 0
        self.bombCounterText = Text(pygame.Rect(300, 10, 200, 40), pygame.font.SysFont('arial', 18), "Bombs left: 0")

        self.resetGame()

    def eventLoop(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouseClick(pos, pygame.mouse.get_pressed())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.mouseClick(pos, [True, False, False])
            if event.key == pygame.K_x:
                self.mouseClick(pos, [False, False, True])

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
        self.bombCounter = maxBombs
        self.resetButton.setColors((255, 0, 0))
        self.bombCounterText.setText("Bombs left: " + str(self.bombCounter))

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
                if not cellClicked.isOpen() and not cellClicked.isFlagged():
                    result = cellClicked.openCell()  # 1 = open, -1 = mine
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
                didFlag = cellClicked.flagCell()  # 1 = flagged, 0 = not flagged
                if didFlag:
                    self.bombCounter -= 1
                else:
                    self.bombCounter += 1
                self.bombCounterText.setText("Bombs left: " + str(self.bombCounter))
            if self.cellsOpened == (cellGrid[0] * cellGrid[1]) - maxBombs:  # Gamve over, victory
                self.resetButton.setColors((0, 255, 0))
                for cell in mineCells:
                    cell.flagCell(True)
                self.roundActive = False
                self.bombCounter = 0
                self.bombCounterText.setText("Bombs left: " + str(self.bombCounter))
                print("Game Completed!")

    def openNeighbours(self, baseX, baseY):
        for y in range(-1, 2):
            for x in range(-1, 2):
                if not (x == 0 and y == 0):
                    if (y + baseY) >= 0 and (x + baseX) >= 0:
                        if (y + baseY) < cellGrid[1] and (x + baseX) < cellGrid[0]:
                            targetCell = cells[y + baseY][x + baseX]
                            if not targetCell.isMine() and not targetCell.isOpen() and not targetCell.isFlagged():
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
        self.bombCounterText.draw(screen)
        # drawText(screen, self.bombCounterText, "Bombs: " + str(self.bombCounterText))

    def getClickedCell(self, x, y) -> Cell:
        if 0 <= x < cellGrid[0] and 0 <= y < cellGrid[1]:
            return cells[int(y)][int(x)]
        return None
