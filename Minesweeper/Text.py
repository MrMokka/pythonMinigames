import pygame


def drawText(screen, border, text):
    textRect = text.get_rect()
    textRect.center = border.center
    screen.blit(text, textRect)


class Text:
    def __init__(self, rect: pygame.Rect, font: pygame.font, text="", color=(0, 0, 0)):
        self.rect = rect
        self.text = text
        self.font = font
        self.color = color

    def draw(self, screen):
        drawText(screen, self.rect, self.font.render(self.text, True, self.color))

    def getRect(self):
        return self.rect

    def setRect(self, rect):
        self.rect = rect

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

    def setFont(self, font: pygame.font):
        self.font = font

    def getFont(self):
        return self.font

    def setColor(self, color):
        self.color = color


