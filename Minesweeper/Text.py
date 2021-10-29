import pygame


def drawText(screen, border, text):
    textRect = text.get_rect()
    textRect.center = border.center
    screen.blit(text, textRect)


class Text:
    def __init__(self, rect, text=""):
        self.rect = rect
        self.text = text

    def draw(self, screen):
        drawText(screen, self.rect, self.text)

    def getRect(self):
        return self.rect

    def setRect(self, rect):
        self.rect = rect

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text
