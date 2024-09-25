import pygame

class Hammer:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.isClick = False

    def update_hammer(self, x_pos, y_pos, isClick = None):
        self.x_pos = x_pos - 30
        self.y_pos = y_pos - 30
        if isClick is not None:
            self.isClick = isClick

    def draw_hammer(self):
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 10, 10)


        