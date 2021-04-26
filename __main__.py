import pygame

from time import time as now

pygame.init()
pygame.mixer.init()

def __pass(): pass
def use(args, names, default):
    for name in names:
        if name in args:
            return name
    return default
def mouse_on(x, y, width, height):
    mouse = pygame.mouse.get_pos()
    if x < mouse[0] < x + width and y < mouse[1] < y + height: return True
    else: return False
def convert(screen, image, x, y, opacity = 255, angle = 0):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = [x, y]).center)
    image, [x, y] = rotated_image, new_rect.topleft
    temp = pygame.Surface((image.get_width(), image.get_height())).convert()
    temp.blit(screen, (-x, -y))
    temp.blit(image, (0, 0))
    temp.set_alpha(opacity)        
    return temp, x, y
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
    def draw(self, window: Window, plus_x:int = 0, plus_y:int = 0):
        geo_last = None
        for geo in self.geometry:
            if geo_last: pygame.draw.line(window.screen, self.color, [geo[0] + plus_x, geo[1] + plus_y], [geo_last[0] + plus_x, geo_last[1] + plus_y])
            geo_last = geo
class Rectangle:
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window:Window, plus_x:int = 0, plus_y:int = 0):
        geo = self.geometry.copy()
        geo[0] += plus_x; geo[1] += plus_y
        pygame.draw.rect(window.screen, self.color, geo)
class Ellipse:
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window:Window, plus_x:int = 0, plus_y:int = 0):
        geo = self.geometry.copy()
        geo[0] += plus_x; geo[1] += plus_y
        pygame.draw.ellipse(window.screen, self.color, geo)
class Polygon:
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window:Window, plus_x:int = 0, plus_y:int = 0):
        geo = self.geometry.copy()
        for point_i in range(len(geo)):
            point = geo[point_i]
            point[0] += plus_x; point[1] += plus_y
            geo[point_i] = point
        
        pygame.draw.polygon(window.screen, self.color, geo)
class Image:
    def __init__(self, path, geometry, alpha = 255, angle = 0):
        self.path = path
        self.geometry = geometry
        self.alpha = alpha
        self.angle = angle
    def draw(self, window:Window, plus_x:int = 0, plus_y:int = 0):
        img = window.load_image(self.path)
        geo = self.geometry.copy()
        geo[0] += plus_x; geo[1] += plus_y
        try: img = pygame.transform.scale(img, (geo[2], geo[3]))
        except: pass
        img, x, y = convert(window.screen, img, geo[0], geo[1], self.alpha, self.angle)
        window.screen.blit(img, [x, y])
class Text:
    def __init__(self, text, geometry, alpha = 255, angle = 0, color = (0, 0, 0), font = "Arial"):
        self.text = text
        self.geometry = geometry
        self.alpha = alpha
        self.angle = angle
        self.color = color
        self.font = font 
    def draw(self, window:Window, plus_x:int = 0, plus_y:int = 0):
        geo = self.geometry.copy()
        geo[0] += plus_x; geo[1] += plus_y
        font = window.load_font(self.font, geo[2])
        text = font.render(self.text, True, self.color)
        text, x, y = convert(window.screen, text, geo[0], geo[1], self.alpha, self.angle)
        window.screen.blit(text, (x, y))
    def get_size(self, window:Window):
        geo = self.geometry.copy()
        font = window.load_font(self.font, geo[2])
        text = font.render(self.text, True, self.color)
        text, x, y = convert(window.screen, text, geo[0], geo[1], self.alpha, self.angle)
        return [text.get_width(), text.get_height()]
class ImageButton:
    def __init__(self, geometry, path:str, text:str, font:str= "Arial", fg:tuple = (0, 0, 0), function =__pass, **args):
        args["None"] = None
        self.geometry = geometry
        self.text = text
        self.font = font
        self.color = {"fg_def": fg, "fg_hover": use(args, ["fg_hover"], "None"), "fg_activate": use(args, ["fg_activate"], None)}
        self.path = {"def":path, "hover": use(args, ["path_hover"], "None"), "activate": use(args, ["path_activate"], "None")}
        self.function = function
        self.__actual = "def"
    def draw(self, window: Window, plus_x:int = 0, plus_y:int = 0):
        geo = self.geometry
        if mouse_on(geo[0] + plus_x, geo[1] + plus_y, geo[2], geo[3]):
            self.__update(window, "hover")
            if window.is_button_down(1):
                self.__update(window, "activate")
            elif window.is_button_up(1):
                self.function()
        else:
            self.__update(window, "def")
        window.blit(self.__bg, [self.geometry[0] + plus_x, self.geometry[1] + plus_y])
    def __update(self, window, use):
        if self.path[use] == None:
            self.__image = window.load_image(self.path["def"])
        else:
            self.__image = window.load_image(self.path[use])
        self.__image = pygame.transform.scale(self.__image, (self.geometry[2], self.geometry[3]))
        self.__bg = pygame.Surface(self.geometry[2], self.geometry[3])
        self.__bg.blit(self.__image, [0, 0])
        if self.color[f"fg_{use}"] == None:
            self.__fg = window.load_font(self.font, self.geometry[3]).render(self.text, True, self.color[f"fg_def"])
        else:
            self.__fg = window.load_font(self.font, self.geometry[3]).render(self.text, True, self.color[f"fg_{use}"])
        self.__bg.blit(self.__fg, [0, 0])
class ButtonImage:
    def __init__(self, geometry, path:str, function = __pass, **args):
        self.geometry = geometry
        args["None"] = None
        self.path = {"path":path, "hover":use(args, ["path_hover"], "None"), "activate":use(args, ["path_activate"], "None")}
        self.__image = Image(self.path["path"], self.geometry)
        self.function = function
    def draw(self, window: Window, plus_x:int = 0, plus_y:int = 0):
        geo = self.geometry
        if mouse_on(geo[0] + plus_x, geo[1] + plus_y, geo[2], geo[3]):
            self.__update("hover")
            if window.is_button_down(1):
                self.__update("activate")
            elif window.is_button_up(1):
                self.function()
        else:
            self.__update("path")
        self.__image.draw(window, plus_x, plus_y)
    def __update(self, use):
        if self.path[use] == None:
            self.__image.path = self.path["path"]
        else:
            self.__image.path = self.path[use]
