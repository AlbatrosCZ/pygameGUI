import pygame

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
    def is_button_down(self, button_id): return self.actions.is_button_down(button_id)
    def is_button_up(self, button_id): return self.actions.is_button_up(button_id)
    def is_key_down(self, key_id): return self.actions.is_key_down(key_id)
    def is_key_up(self, key_id): return self.actions.is_key_up(key_id)
    def load_image(self, path):
        if path in self.images: return self.images[path]
        else: self.images[path] = pygame.image.load(path); return self.load_image(path)
    def load_font(self, font_name, font_size):
        if font_name in self.fonts:
            if font_size in self.fonts[font_name]: return self.fonts[font_name][font_size]
        else: self.fonts[font_name] = {}
        self.fonts[font_name][font_size] = pygame.font.SysFont(font_name, font_size)
        return self.load_font(font_name, font_size)
    def fill(self, color):
        self.root.fill(color)
    def loop(self, fps):
        self.clock.tick(fps)
        pygame.display.flip()
        self.actions.loop()
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
class Line:
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window: Window, plus_x: int = 0, plus_y: int = 0):
        geo_last = None
        for geo in self.geometry:
            if geo_last:
                pygame.draw.line(window.screen, self.color, [geo[0] + plus_x, geo[1] + plus_y], [geo_last[0] + plus_x, geo_last[1] + plus_y])
            geo_last = geo
class Rectangle:
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window:Window, plus_x = 0, plus_y = 0):
        geo = self.geometry.copy()
        geo[0] += plus_x; geo[1] += plus_y
        pygame.draw.rect(window.screen, self.color, geo)
class Ellipse:
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window:Window, plus_x = 0, plus_y = 0):
        geo = self.geometry.copy()
        geo[0] += plus_x; geo[1] += plus_y
        pygame.draw.ellipse(window.screen, self.color, geo)
class Polygon:
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window:Window, plus_x = 0, plus_y = 0):
        geo = self.geometry.copy()
        for point_i in range(len(geo)):
            point = geo[point_i]
            point[0] += plus_x; point[1] += plus_y
            geo[point_i] = point
        
        pygame.draw.polygon(window.screen, self.color, geo)
