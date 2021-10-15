import pygame
import os

from Menu.Menu import Menu

os.environ['SDL_VIDEO_WINDOW_POS'] = '500, -1000'

screenSize = (1000, 800)

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('Game?')
# font = pygame.font.SysFont(None, 30)

menu = Menu(screenSize)

programRunning = True

while programRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            programRunning = False
        menu.eventLoop(event)

    menu.logicLoop()

    screen.fill((255, 255, 255))

    menu.drawLoop(screen)

    pygame.display.flip()
