"""
Objects: Line, Rectangle, Ellipse, Polygon, Image, Text, ButtonImage, DefaultButton


from pygameGui import Window, Line, Rectangle, Ellipse, Plygon, Image, Text, ButtonImage
from pygameGui import DefaultButton as Button

root = Window(width, height, fullscreen)

#...

while True:
    root.fill((R,G,B))

    #...

    root.loop(100)
"""

import pygame

from time import time as now

pygame.init()
pygame.mixer.init()

def pass_(): pass
def use(args, names, default):
    for name in names:
        if name in args:
            return args[name]
    return default
def mouse_on(x, y, width, height):
    mouse = pygame.mouse.get_pos()
    if x < mouse[0] < x + width and y < mouse[1] < y + height: return True
    else: return False
def convert(root, image, x, y, opacity = 255, angle = 0):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = [x, y]).center)
    image, [x, y] = rotated_image, new_rect.topleft
    temp = pygame.Surface((image.get_width(), image.get_height())).convert()
    temp.blit(root, (-x, -y))
    temp.blit(image, (0, 0))
    temp.set_alpha(opacity)        
    return temp, x, y
class Window:
    """Window class open and manage window
*width = width of window, 0 for screen width
*height = height of window, 0 for screen height
*fullscreen = is window fullscreanned or not
\nUsage:
*width = Integer greater than or equal to 0
*height = Integer greater than or equal to 0
*fullscreen = True/Flase"""
    def __init__(self, width: int, height: int, fullscreen: bool = False):
        if fullscreen: self.root = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
        else: self.root = pygame.display.set_mode([width, height])
        self.width, self.height = self.root.get_width(), self.root.get_height()
        self.clock = pygame.time.Clock()
        self.images = {}; self.fonts = {}
        self.actions = ActionListener()
    def is_button_down(self, button_id):
        """This function returns if button, that id was given, is pressed
*button_id = numeric id of button on mouse
\nUsage:
*button_id = Integer greater than 0"""
        return self.actions.is_button_down(button_id)
    def is_button_up(self, button_id):
        """This function returns if button, that id was given, is released
*button_id = numeric id of button on mouse
\nUsage:
*button_id = Integer greater than 0"""
        return self.actions.is_button_up(button_id)
    def is_key_down(self, key_id): 
        """This function return if key, that id was given, is pressed
*key_id = numeric id of key on keyboard
\nUsage:\nkey_id = Integer greater than 0"""
        return self.actions.is_key_down(key_id)
    def is_key_up(self, key_id): 
        """This function return if key, that id was given, is released
*key_id = numeric id of key on keyboard
\nUsage:
*key_id = Integer greater than 0"""
        return self.actions.is_key_up(key_id)
    def load_image(self, path):
        """This function load an image form datastorage
*path = path to image
\nUsage:
*path = \"path_to_image/image.image_type\" like \"resources/images/image.png\""""
        if path in self.images: return self.images[path]
        else: self.images[path] = pygame.image.load(path); return self.load_image(path)
    def load_font(self, font_name, font_size):
        """This function load a font from sysfonts
*font_name = name of sys font
*font_size = size of sys font
\nUsage:
*font_name = String name
*font_size = Integer greater than 0"""
        if font_name in self.fonts:
            if font_size in self.fonts[font_name]: return self.fonts[font_name][font_size]
        else: self.fonts[font_name] = {}
        self.fonts[font_name][font_size] = pygame.font.SysFont(font_name, font_size)
        return self.load_font(font_name, font_size)
    def fill(self, color):
        """This function fill window via color
*color = color that was fill the window
\nUsage:
*color = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255"""
        self.root.fill(color)
    def loop(self, fps):
        """This function loop the window
*fps = how often the pack passes per second
\nUsage:
*fps = Integer greater than 0"""
        self.clock.tick(fps)
        pygame.display.flip()
        self.actions.loop()
class ActionListener:
    """Action Listener class manage events of pygame"""
    def __init__(self):
        self.button_down    = {}; self.button_up      = []
        self.key_down       = {}; self.key_up         = []
        self.escape         = False; self.expose         = False
        self.minimalize     = False
        self.cursor_motion  = {"x" : 0, "y" : 0}
    def loop(self):
        """This function recognize pygame's events"""
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
        """This function returns if button, that id was given, is pressed
*button_id = numeric id of button on mouse
\nUsage:
*button_id = Integer greater than 0"""
        if button_id not in self.button_down: return False
        return self.button_down[button_id]
    def is_button_up(self, button_id): 
        """This function returns if button, that id was given, is released
*button_id = numeric id of button on mouse
\nUsage:
*button_id = Integer greater than 0"""
        return button_id in self.button_up
    def is_key_down(self, key_id):
        """This function return if key, that id was given, is pressed
*key_id = numeric id of key on keyboard
\nUsage:\nkey_id = Integer greater than 0"""
        if key_id not in self.key_down: return False
        return self.key_down[key_id]
    def is_key_up(self, key_id): 
        """This function return if key, that id was given, is released
*key_id = numeric id of key on keyboard
\nUsage:
*key_id = Integer greater than 0"""
        return key_id in self.key_up
class Line:
    """Line class draw line on window
*geometry = list of x-y-cordinations
*color = line color
\nUsage:
*geometry = [[x1, y1], [x2, y2] ... ]
*color = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255"""
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window: Window, plus_x:int = 0, plus_y:int = 0):
        """This function draw the line on window
*window = window that use for draw
*plus_x = shift on the x-axis
*plus_y = shift on the y-axis
\nUsage:
*window = Window instance
*plus_x = Integer
*plus_y = Integer"""
        geo_last = None
        for geo in self.geometry:
            if geo_last: pygame.draw.line(window.root, self.color, [geo[0] + plus_x, geo[1] + plus_y], [geo_last[0] + plus_x, geo_last[1] + plus_y])
            geo_last = geo
class Rectangle:
    """Rectangle class draw rectangle on window
*geometry = list of x-y-cordination, width and height
*color = rectangle color
\nUsage:
*geometry = [topLeftCornerX, topLeftCornerY, width, height] | topLeftCornerX = Integer, topLeftCornerY = Integer, width = Integer greater than 0, height = Integer greater than 0
*color = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255"""
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window:Window, plus_x:int = 0, plus_y:int = 0):
        """This function draw the rectangle on window
*window = window that use for draw
*plus_x = shift on the x-axis
*plus_y = shift on the y-axis
\nUsage:
*window = Window instance
*plus_x = Integer
*plus_y = Integer"""
        geo = self.geometry.copy()
        geo[0] += plus_x; geo[1] += plus_y
        pygame.draw.rect(window.root, self.color, geo)
class Ellipse:
    """Elliple class draw ellipse on window
*geometry = list of x-y-cordination, width and height
*color = color of ellipse
\nUsage:
*geometry = [topLeftCornerX, topLeftCornerY, width, height] | topLeftCornerX = Integer, topLeftCornerY = Integer, width = Integer greater than 0, height = Integer greater than 0
*color = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255"""
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window:Window, plus_x:int = 0, plus_y:int = 0):
        """This function draw the ellipse on window
*window = window that use for draw
*plus_x = shift on the x-axis
*plus_y = shift on the y-axis
\nUsage:
*window = Window instance
*plus_x = Integer
*plus_y = Integer"""
        geo = self.geometry.copy()
        geo[0] += plus_x; geo[1] += plus_y
        pygame.draw.ellipse(window.root, self.color, geo)
class Polygon:
    """Polygon class draw polygon on window
*geometry = list of x-y-cordinations
*color = polygon color
\nUsage:
*geometry = [[x1, y1], [x2, y2], [x3, y3] ... ]
*color = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255"""
    def __init__(self, geometry, color):
        self.geometry = geometry
        self.color = color
    def draw(self, window:Window, plus_x:int = 0, plus_y:int = 0):
        """This function draw the polygon on window
*window = window that use for draw
*plus_x = shift on the x-axis
*plus_y = shift on the y-axis
\nUsage:
*window = Window instance
*plus_x = Integer
*plus_y = Integer"""
        geo = self.geometry.copy()
        for point_i in range(len(geo)):
            point = geo[point_i].copy()
            point[0] += plus_x; point[1] += plus_y
            geo[point_i] = point
        pygame.draw.polygon(window.root, self.color, geo)
class Image:
    """Image class draw image on window
*path = path to image
*geometry = list of x-y-cordination, width and height (width and height now required. If not given, image use original size)
*alpha = opticity of image (0 = invisible, 255 = normal view)
*angle = rotate of image in degrees
\nUsage:
*path = \"path_to_image/image.image_type\" like \"resources/images/image.png\"
*geometry = [topLeftCornerX, topLeftCornerY, width, height] | topLeftCornerX = Integer, topLeftCornerY = Integer, width = Integer greater than 0, height = Integer greater than 0
*alpha = Integer 0-255
*angle = Integer"""
    def __init__(self, path, geometry, alpha = 255, angle = 0):
        self.path = path
        self.geometry = geometry
        self.alpha = alpha
        self.angle = angle
    def draw(self, window:Window, plus_x:int = 0, plus_y:int = 0):
        """This function draw the image on window
*window = window that use for draw
*plus_x = shift on the x-axis
*plus_y = shift on the y-axis
\nUsage:
*window = Window instance
*plus_x = Integer
*plus_y = Integer"""
        img = window.load_image(self.path)
        geo = self.geometry.copy()
        geo[0] += plus_x; geo[1] += plus_y
        try: img = pygame.transform.scale(img, (geo[2], geo[3]))
        except: pass
        img, x, y = convert(window.root, img, geo[0], geo[1], self.alpha, self.angle)
        window.root.blit(img, [x, y])
class Text:
    """Image class draw image on window
*text = text that would be drawed
*geometry = x-y-cordination and text size
*alpha = opticity of text (0 = invisible, 255 = normal view)
*angle = rotate of text in degrees
*color = color of text
*font = font of text
\nUsage:
*text = String
*geometry = [topLeftCornerX, topLeftCornerY, textSize] | topLeftCornerX = Integer, topLeftCornerY = Integer, textSize = Integer greater than 0
*alpha = Integer 0-255
*angle = Integer
*color = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255
*font = name of sys font"""
    def __init__(self, text, geometry, alpha = 255, angle = 0, color = (0, 0, 0), font = "Arial"):
        self.text = text
        self.geometry = geometry
        self.alpha = alpha
        self.angle = angle
        self.color = color
        self.font = font 
    def draw(self, window:Window, plus_x:int = 0, plus_y:int = 0):
        """This function draw the text on window
*window = window that use for draw
*plus_x = shift on the x-axis
*plus_y = shift on the y-axis
\nUsage:
*window = Window instance
*plus_x = Integer
*plus_y = Integer"""
        geo = self.geometry.copy()
        geo[0] += plus_x; geo[1] += plus_y
        font = window.load_font(self.font, geo[2])
        text = font.render(self.text, True, self.color)
        text, x, y = convert(window.root, text, geo[0], geo[1], self.alpha, self.angle)
        window.root.blit(text, (x, y))
    def get_size(self):
        """This function return size of text"""
        geo = self.geometry.copy()
        font = pygame.font.SysFont(self.font, geo[2])
        text = font.render(self.text, True, self.color)

        text, x, y = convert(pygame.Surface([0, 0], pygame.SRCALPHA, 32), text, geo[0], geo[1], self.alpha, self.angle)
        return [text.get_width(), text.get_height()]
class ButtonImage:
    """Button Image class draw button on window
*geometry = list of x-y-cordinaton, width and height
*path = path to image
*function = function that use on button click
**path_hover = path to image, that draw when cursor hover on button (if not set use *path)
**path_activate = path to image, that draw when button is down (if not set use *path)
\nUsage:
*geometry = [topLeftCornerX, topLeftCornerY, width, height] | topLeftCornerX = Integer, topLeftCornerY = Integer, width = Integer greater than 0, height = Integer greater than 0
*path = \"path_to_image/image.image_type\" like \"resources/images/image.png\"
*function = lambda: someFunction(some args) or someFunction
**path_hover = \"path_to_image/image.image_type\" like \"resources/images/image.png\"
**path_activate = \"path_to_image/image.image_type\" like \"resources/images/image.png\""""
    def __init__(self, geometry, path:str, function = pass_, **args):
        self.geometry = geometry
        self.path = {"path":path, "hover":use(args, ["path_hover"], None), "activate":use(args, ["path_activate"], None)}
        self.__image = Image(self.path["path"], self.geometry)
        self.function = function
    def draw(self, window: Window, plus_x:int = 0, plus_y:int = 0):
        """This function draw the button on window
*window = window that use for draw
*plus_x = shift on the x-axis
*plus_y = shift on the y-axis
\nUsage:
*window = Window instance
*plus_x = Integer
*plus_y = Integer"""
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
class DefaultButton:
    """Default Button class draw button on window
*geometry = list of x-y-cordination, width and height
*text = text of button
*fg = color of text and border of button
*bg = color of background of button
*font = font of button's text
*function = function that use on button click
**fg_hover = color of text and border of button, that draw when cursor hover on button (when not set use fg)
**fg_activate = color of text and border of button, that draw when button is down (when not set use fg)
**bg_hover = color of background of button, that draw when cursor hover on button (when not set use bg)
**bg_activate = color of background of button, that draw when button is down (when not set use bg)
\nUsage:
*geometry = [topLeftCornerX, topLeftCornerY, width, height] | topLeftCornerX = Integer, topLeftCornerY = Integer, width = Integer greater than 0, height = Integer greater than 0
*text = String
*fg = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255
*bg = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255
*font = name of sys font
*function = lambda: someFunction(some args) or someFunction
**fg_hover = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255
**fg_activate = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255
**bg_hover = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255
**bg_activate = (R, G, B) | R(red) = 0-252, G(green) = 0-255, B(blue) = 0-255"""
    def __init__(self, geometry, text, fg = (0, 0, 0), bg = (255, 255, 255), font = "Arial", function = pass_, **args):
        self.geometry = geometry
        self.text = text
        self.font = font
        self.function = function
        self.color = {"fg_def":fg, "fg_hover":use(args, ["fg_hover"], None), "fg_activate":use(args, ["fg_activate"], None), 
                      "bg_def":bg, "bg_hover":use(args, ["bg_hover"], None), "bg_activate":use(args, ["bg_activate"], None)}
        self.text_size = [0,0]
    def draw(self, window: Window, plus_x:int = 0, plus_y:int = 0):
        """This function draw the button on window
*window = window that use for draw
*plus_x = shift on the x-axis
*plus_y = shift on the y-axis
\nUsage:
*window = Window instance
*plus_x = Integer
*plus_y = Integer"""
        geo = self.geometry
        if mouse_on(geo[0] + plus_x, geo[1] + plus_y, geo[2], geo[3]):
            use = "hover"
            if window.is_button_down(1):
                use = "activate"
            elif window.is_button_up(1):
                self.function()
        else:
            use = "def"
        bg = pygame.Surface((self.geometry[2], self.geometry[3]), pygame.SRCALPHA, 32)
        if self.color[f"fg_{use}"] == None:
            bg.fill(self.color["fg_def"])
        else:
            bg.fill(self.color[f"fg_{use}"])
        if self.color[f"bg_{use}"] == None:
            pygame.draw.rect(bg, self.color["bg_def"], (1, 1, geo[2]-2, geo[3]-2))
        else:
            pygame.draw.rect(bg, self.color[f"bg_{use}"], (1, 1, geo[2]-2, geo[3]-2))
        if self.color[f"fg_{use}"] == None:
            minus = 0
            while True:
                text = window.load_font(self.font, geo[3] - 4 - minus).render(self.text, True, self.color["fg_def"])
                if geo[2] - 4 > text.get_width() and geo[3] - 4 > text.get_height():
                    break
                else:
                    minus += 1
        else:
            minus = 0
            while True:
                text = window.load_font(self.font, geo[3] - 4 - minus).render(self.text, True, self.color[f"fg_{use}"])
                if geo[2] - 4 > text.get_width() and geo[3] - 4 > text.get_height():
                    break
                else:
                    minus += 1
        height = int((geo[3] - text.get_height())/2); width  = int((geo[2] - text.get_width())/2)
        bg.blit(text, [width, height])
        window.root.blit(bg, [geo[0] + plus_x, geo[1] + plus_y])
        self.text_size = [text.get_width(), text.get_height()]
class OnOffSwitch:
    def __init__(self, geometry, border = (0, 0, 0), bg = (255, 255, 255), **args):
        self.geometry = geometry
        self.colors = { "border_def": border, "border_hover": use(args, ["border_hover"], None), "border_activate": use(args, ["border_hover"], None),
                        "bg_def": bg, "bg_hover": use(args, ["bg_hover"], None), "bg_activate": use(args, ["bg_activate"], (0, 0, 255)),
                        "I": use(args, ["i_color"], (0, 255, 0)), "O": use(args, ["o_color"], (255, 0, 0))}
        self.state = False
        self.__surface = pygame.Surface((51, 31), pygame.SRCALPHA, 32)
    def draw(self, window: Window, plus_x:int = 0, plus_y:int = 0):
        font = window.load_font("PalatinoLinoType", 25)
        I = font.render("I", True, self.colors["I"]); O = font.render("O", True, self.colors["O"])
        geo = self.geometry.copy()
        self.__surface.convert_alpha()
        self.__surface.fill(self.colors["border_def"])
        if not self.state:
            pygame.draw.rect(self.__surface, self.colors["bg_def"], [1, 1, 24, 29])
            if self.colors["bg_activate"] != None: pygame.draw.rect(self.__surface, self.colors["bg_activate"], [26, 1, 24, 29])
        else:
            if self.colors["bg_activate"] != None: pygame.draw.rect(self.__surface, self.colors["bg_activate"], [1, 1, 24, 29])
            pygame.draw.rect(self.__surface, self.colors["bg_def"], [26, 1, 24, 29])
        if mouse_on(geo[0] + 1, geo[1] + 1, 24, 29):
            if self.colors["bg_hover"]: pygame.draw.rect(self.__surface, self.colors["bg_hover"], [1, 1, 24, 29])
            if window.is_button_down(1): self.state = True
        elif mouse_on(geo[0] + 26, geo[1] + 1, 24, 29):
            if self.colors["bg_hover"]: pygame.draw.rect(self.__surface, self.colors["bg_hover"], [26, 1, 24, 29])
            if window.is_button_down(1): self.state = False
        self.__surface.blit(I, [8, 5]); self.__surface.blit(O, [28, 5])
        self.__surface = convert(window.root, self.__surface, geo[0] + plus_x, geo[1] + plus_y)[0]
        window.root.blit(self.__surface, self.geometry)        
        

        

