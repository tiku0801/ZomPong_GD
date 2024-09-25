import pygame
from enum import Enum
#x0 75, 335, 595
#x = 96, 356, 671
#y = 170, 420, 670

class STATUS(Enum):
    APPEARING = 0
    HIT = 1
    DISAPPEARING = 2
    DELETED = 3
    MISSED = 4
    WAITING = 5


class Zombie:
    def __init__(self, x_pos, y_pos):
        self.max_height = 158
        self.height = 0
        self.width = 102
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.status = STATUS.WAITING
        # self.status = STATUS.APPEARING
        self.exist_time = 0 #second
        self.speed = 2 #frame

    def move(self):
        # if self.status == STATUS.WAITING:
        if self.status == STATUS.APPEARING:
            if self.height + self.speed < self.max_height :
                self.height += self.speed
            else:
                if self.exist_time > 3 :
                    self.status = STATUS.DISAPPEARING

    def check_hit(self, x_mouse, y_mouse):
        if self.status == STATUS.APPEARING or self.status == STATUS.DISAPPEARING:
            if self.x_pos <= x_mouse and x_mouse <=self.x_pos + self.width and self.y_pos >= y_mouse and y_mouse >=self.y_pos - self.height:
                return True
        return False
    
    def disappear(self):
        if self.status == STATUS.DISAPPEARING or self.status == STATUS.HIT:
            if self.height - self.speed >= 0:
                self.height -= self.speed 
            
    def draw_zom(self):
        # self.rect = pygame.Rect(self.x_pos, self.y_pos - self.height, self.width, self.height)
        if self.status == STATUS.HIT and self.height == 0:
            self.status = STATUS.DELETED
        if self.status == STATUS.DISAPPEARING and self.height == 0:
            self.status = STATUS.MISSED

    
