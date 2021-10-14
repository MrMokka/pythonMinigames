import pygame


class Grid:
    def __init__(self):
        self.grid_lines = [((0, 200), (600, 200)),
                           ((0, 400), (600, 400)),
                           ((200, 0), (200, 600)),
                           ((400, 0), (400, 600))]


    def draw(self, screen):
        for line in self.grid_lines:
            pygame.draw.line(screen, (200, 200, 200), line[0], line[1], 2)