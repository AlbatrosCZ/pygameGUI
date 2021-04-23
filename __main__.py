import pygame
import string

from time import time as now

pygame.init()
pygame.mixer.init()

class Window:
    def __init__(self, width: int, height: int, fullscreen: bool = False):
        if fullscreen: self.root = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
        else: self.root = pygame.display.set_mode([width, height])
        self.width, self.height = self.root.get_width(), self.root.get_height()
        self.clock = pygame.time.Clock()
        self.images = {}; self.fonts = {}
        self.actions = ActionListener()
class ActionListener:
    def __init__(self):
        self.button_down    = {}; self.button_up      = []
        self.key_down       = {}; self.key_up         = []
        self.escape         = False; self.expose         = False
        self.minimalize     = False
        self.cursor_motion  = {"x" : 0, "y" : 0}
    def loop(self):
        self.expose = False; self.escape = False
        self.button_up = []; self.key_up = []
        self.cursor_motion["x"], self.cursor_motion["y"] = (0, 0)
        for event in pygame.event.get(): 
            if event.type == 1:
                if event.state == 6: self.minimalize = event.gain == 1
            elif event.type == 2: self.key_down[event.key] = [now(), event.unicode]
            elif event.type == 3: self.key_down[event.key] = False; self.key_up.append(event.key)
            elif event.type == 4: self.cursor_motion["x"], self.cursor_motion["y"] = event.rel
            elif event.type == 5: self.button_down[event.button] = now()
            elif event.type == 6: self.button_down[event.button] = False; self.button_up.append(event.button)
            elif event.type == 17: self.expose = True
            elif event.type == 12: self.escape = True
    def is_button_down(self, button_id):
        if button_id not in self.button_down: return False
        return self.button_down[button_id]
    def is_key_down(self, key_id):
        if key_id not in self.key_down: return False
        return self.key_down[key_id]
    def is_button_up(self, button_id): return button_id in self.button_up
    def is_key_up(self, key_id): return key_id in self.key_up

