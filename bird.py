#the class for the bird
#Author: Lotta Rantala

import pygame

class Bird:
    def __init__(self):
        self.x = 100
        self.y = 200
        self.jump_force = 50
        self.height = self.width = 50
    
    def jump(self):
        self.y -= self.jump_force
        if self.y < -10:
            self.y = -10