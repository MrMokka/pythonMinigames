import pygame


class Button:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.bgColor = (0, 0, 0)
        self.borderColor = (255, 255, 255)

    def getRect(self):
        return self.rect

    def setRect(self, rect):
        self.rect = rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.bgColor, self.rect)
        pygame.draw.rect(screen, self.borderColor, self.rect, 2)

    def setColors(self, bgColor, borderColor=None):
        self.bgColor = bgColor
        if borderColor is not None:
            self.borderColor = borderColor

    def getColors(self):
        return self.bgColor, self.borderColor
