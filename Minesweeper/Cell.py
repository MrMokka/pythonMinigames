import pygame

from Minesweeper.Text import Text


class Color:
    Border = (255, 255, 255)
    BorderOpen = (150, 150, 150)
    Background = (189, 189, 189)
    MineBackground = (255, 0, 0)
    Mine = (0, 0, 0)
    Flag = (255, 100, 100)
    Value = [
        (255, 255, 255),
        (0, 0, 255),
        (0, 123, 0),
        (255, 0, 0),
        (0, 0, 123),
        (123, 0, 0),
        (0, 123, 123),
        (0, 0, 0),
        (123, 123, 123)
    ]


FlagChar = 'F'


class Cell:
    def __init__(self, indexX, indexY, posX, posY, size, font):
        self.indexX = indexX
        self.indexY = indexY
        self.x = posX
        self.y = posY
        self.size = size
        self.value = 0
        self.mine = False
        self.flagged = False
        self.open = False
        self.font = font
        self.textObj = Text(pygame.Rect(self.x, self.y, self.size, self.size), font)

    def draw(self, screen):
        outline = pygame.Rect(self.x, self.y, self.size, self.size)
        inside = pygame.Rect(self.x + 1, self.y + 1, self.size - 2, self.size - 2)
        if not self.open:
            pygame.draw.rect(screen, Color.Border, outline)
            pygame.draw.rect(screen, Color.Background, inside)
            if self.flagged:
                self.textObj.draw(screen)
        else:
            if self.mine:
                pygame.draw.rect(screen, Color.MineBackground, outline)
            else:
                pygame.draw.rect(screen, Color.BorderOpen, outline)
                pygame.draw.rect(screen, Color.Background, inside)

        if self.open:
            if self.mine:
                pygame.draw.circle(screen, Color.Mine,
                                   (self.x + (self.size / 2), self.y + (self.size / 2)),
                                   self.size / 3)
            elif self.value > 0:
                self.textObj.draw(screen)

    def setMine(self, mine=True):
        self.mine = mine

    def getValue(self):
        return self.value

    def isMine(self):
        return self.mine

    def addValue(self):
        self.value += 1
        self.textObj.setText(str(self.value))
        self.textObj.setColor(Color.Value[self.value])

    def openCell(self) -> int:  # 1 = open, -1 = mine
        self.open = True
        if self.mine:
            return -1
        return 1

    def flagCell(self, boolean=None):
        if not self.open:
            if boolean is None:
                self.flagged = not self.flagged
            else:
                self.flagged = boolean
            if self.flagged:
                self.textObj.setText(FlagChar)
                self.textObj.setColor(Color.Flag)
            else:
                self.textObj.setText(str(self.value))
                self.textObj.setColor(Color.Value[self.value])
        return self.flagged

    def isOpen(self):
        return self.open

    def isFlagged(self):
        return self.flagged

    def getIndex(self):
        return self.indexX, self.indexY

    def print(self):
        print("Cell: " + str(self.indexX) + " : " + str(self.indexY))


