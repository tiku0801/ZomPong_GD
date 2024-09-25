import pygame
class Setting:
    def __init__(self) :
        self.screen_width = 800
        self.screen_height = 800
        self.fps = 30
        self.font = pygame.font.Font(None, 30)
        self.max_zom = 2
        self.zom_speed = [4,8]
        self.level_time = [45,30]