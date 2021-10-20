import pygame


class Button:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def getRect(self):
        return self.rect

    def setRect(self, rect):
        self.rect = rect

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
