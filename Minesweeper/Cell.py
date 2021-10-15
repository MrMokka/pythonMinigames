import pygame


class Color:
    Border = (255, 255, 255)
    BorderOpen = (150, 150, 150)
    Background = (189, 189, 189)
    MineBackground = (255, 0, 0)
    Mine = (0, 0, 0)
    Flag = (255, 0, 0)
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

    def draw(self, screen):
        outline = pygame.Rect(self.x, self.y, self.size, self.size)
        inside = pygame.Rect(self.x + 1, self.y + 1, self.size - 2, self.size - 2)
        if not self.open:
            pygame.draw.rect(screen, Color.Border, outline)
            pygame.draw.rect(screen, Color.Background, inside)
            if self.flagged:
                self.drawText(screen, outline, self.font.render(FlagChar, True, Color.Flag))
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
                self.drawText(screen, outline, self.font.render(str(self.value), True, Color.Value[self.value]))
                # textRect = text.get_rect()
                # textRect.center = outline.center
                # screen.blit(text, textRect)
                    # (self.x + (self.width / 3),
                    #  self.y + (self.height / 3)))

    def drawText(self, screen, border, text):
        textRect = text.get_rect()
        textRect.center = border.center
        screen.blit(text, textRect)

    def setMine(self, mine=True):
        self.mine = mine

    def getValue(self):
        return self.value

    def isMine(self):
        return self.mine

    def addValue(self):
        self.value += 1

    def openCell(self) -> int:  # 1 = open, 0 = nothing, -1 = mine
        if self.open or self.flagged:
            return 0
        self.open = True
        if self.mine:
            return -1
        return 1

    def flagCell(self, boolean):
        if not self.open:
            if boolean is None:
                self.flagged = not self.flagged
            else:
                self.flagged = boolean

    def isOpen(self):
        return self.open

    def getIndex(self):
        return self.indexX, self.indexY

    def print(self):
        print("Cell: " + str(self.indexX) + " : " + str(self.indexY))
