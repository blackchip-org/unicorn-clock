import sys

def render_bitmap(dmd, gfx, color, at=(0, 0)):
    for y, row in enumerate(gfx):
        for x, pixel in enumerate(row):
            if pixel != 0:
                dmd.set_pixel((x + at[0], y + at[1]), color)

class Animation:

    def __init__(self, callback, duration, delay=0):
        self.callback = callback
        self.duration = duration
        self.delay = delay
        self.start_time = 0
        self.end_time = sys.float_info.max
        self.progress = 0

    def service(self, now):
        if self.start_time == 0:
            self.start_time = now + self.delay
            self.end_time = self.start_time + self.duration
        if now < self.start_time:
            return
        if now > self.end_time:
            return
        self.progress = (now - self.start_time) / (self.end_time - self.start_time)
        self.callback(self.progress)


class Animator:

    def __init__(self):
        self.animations = []

    def add(self, callback, duration, delay=0):
        self.animations += [Animation(callback, duration, delay)]

    def service(self, now):
        for anim in self.animations:
            anim.service(now)
        self.animations = [x for x in self.animations if now < x.end_time]

    def clear(self):
        self.animations = []


class Fade:

    def __init__(self, dmd, x, y, source, target):
        self.dmd = dmd
        self.x = x
        self.y = y
        self.source = source
        self.target = target

    def update(self, progress):
        color = [0, 0, 0]
        for i in range(3):
            h = self.source[i]
            diff = self.target[i] - h
            color[i] = int(h + (diff * progress))
        self.dmd.set_pixel((self.x, self.y), color)


class SlideColumnIn:

    def __init__(self, dmd, duration, column, pixels):
        self.dmd = dmd
        self.column = column
        self.pixels = pixels

    def update(self, progress):
        offset = int(self.dmd.height - (progress * self.dmd.height))
        for i in range(self.dmd.height):
            index = i + offset
            if index >= 0 and index < len(self.pixels):
                pix = self.pixels[index]
                self.dmd.set_pixel((self.column, i), pix)

chars64 = {
    'd': [
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    't': [
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
}

digits3 = {
    0: [
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    1: [
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
    ],
    2: [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
    ],
    3: [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    4: [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
    ],
    5: [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    6: [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    7: [
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
    ],
    8: [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    9: [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
   ]
}
