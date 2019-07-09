import ctypes
import sys
import sdl2.ext
from sdl2 import *
from gpiozero import Device, Button
from gpiozero.pins.mock import MockFactory

def init():
    SDL_Init(SDL_INIT_VIDEO)

class DMD:

    bg_color = (40, 40, 40)
    border_color = (80, 80, 80)
    border_size = 20

    def __init__(self, width, height, scale=1, padding=1, name='DMD'):
        self.width = width
        self.height = height
        self.scale = scale
        self.padding = padding
        self.win_width = ((width * scale) + (padding * width) + padding +
                          (self.border_size * 2))
        self.win_height = ((height * scale) + (padding * height) + padding +
                           (self.border_size * 2))
        self.name = name
        self.window = SDL_CreateWindow(bytes(self.name, 'utf-8'),
            SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
            self.win_width, self.win_height, SDL_WINDOW_SHOWN)
        self.r = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED)
        SDL_GL_SetSwapInterval(1)
        self.pixel = SDL_CreateTexture(self.r, SDL_PIXELFORMAT_RGBA8888,
            SDL_TEXTUREACCESS_TARGET, self.scale, self.scale)
        SDL_SetRenderTarget(self.r, self.pixel)
        SDL_SetRenderDrawColor(self.r, 0xff, 0xff, 0xff, 0xff)
        SDL_RenderFillRect(self.r, None)
        SDL_SetRenderTarget(self.r, None)
        self.pixels = {}
        self.clear()

    @property
    def rotation(self):
        return 0

    @rotation.setter
    def rotation(self, value):
        pass

    @property
    def brightness(self):
        return 1

    @brightness.setter
    def brightness(self, value):
        pass

    def set_pixel(self, coord, color):
        self.pixels[coord] = color

    def get_pixel(self, coord):
        return self.pixels[coord]

    def show(self):
        SDL_SetRenderTarget(self.r, None)
        c = self.bg_color
        SDL_SetRenderDrawColor(self.r, c[0], c[1], c[2], 0xff)
        SDL_RenderClear(self.r)
        self.draw_border()
        self.draw_pixels()
        SDL_RenderPresent(self.r)

    def draw_border(self):
        c = self.border_color
        SDL_SetRenderDrawColor(self.r, c[0], c[1], c[2], 0xff)
        top_border = SDL_Rect(
            0,
            0,
            self.win_width,
            self.border_size
        )
        SDL_RenderFillRect(self.r, top_border)
        bottom_border = SDL_Rect(
            0,
            self.win_height - self.border_size,
            self.win_width,
            self.border_size
        )
        SDL_RenderFillRect(self.r, bottom_border)
        left_border = SDL_Rect(
            0,
            0,
            self.border_size,
            self.win_height
        )
        SDL_RenderFillRect(self.r, left_border)
        right_border = SDL_Rect(
            self.win_width - self.border_size,
            0,
            self.border_size,
            self.win_height
        )
        SDL_RenderFillRect(self.r, right_border)

    def draw_pixels(self):
        for x in range(self.width):
            for y in range(self.height):
                px = self.border_size + (x * self.padding) + self.padding + (x * self.scale)
                py = self.border_size + (y * self.padding) + self.padding + (y * self.scale)
                c = self.pixels[(x, y)]
                SDL_SetTextureColorMod(self.pixel, c[0], c[1], c[2])
                dest = SDL_Rect(px, py, self.scale, self.scale)
                SDL_RenderCopy(self.r, self.pixel, None, dest)

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.pixels[(x, y)] = (0x00, 0x00, 0x00)


Device.pin_factory = MockFactory()

class Hardware:

    def __init__(self):
        self.dmd = DMD(8, 8, 16, name='Unicorn HAT')
        self.enter_button = Button(6)
        self.up_button = Button(13)
        self.down_button = Button(16)
        self.exit_button = Button(26)

    def service(self):
        event = SDL_Event()
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                sys.exit(0)
            if event.type == SDL_KEYDOWN:
                self.key_event(event.key)

    def key_event(self, e):
        if e.keysym.sym == SDLK_1:
            self.exit_button.when_pressed()
        if e.keysym.sym == SDLK_2:
            self.down_button.when_pressed()
        if e.keysym.sym == SDLK_3:
            self.up_button.when_pressed()
        if e.keysym.sym == SDLK_4:
            self.enter_button.when_pressed()


