import pygame
import string

from time import time as now

pygame.init()
pygame.mixer.init()

class Window:
    def __init__(self, width: int, height: int, fullscreen: bool = False):

        if fullscreen:
            self.root = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
        else:
            self.root = pygame.display.set_mode([width, height])

        self.width, self.height = self.root.get_width(), self.root.get_height()
        self.clock = pygame.time.Clock()
        
        self.images = {}
        self.fonts = {}