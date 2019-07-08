from datetime import datetime, timedelta
import time
import gfx

class XY:

    color_hour5 = (0xff, 0x00, 0x00)
    color_hour = (0x00, 0x00, 0xff)
    color_dot = (0xff, 0xff, 0x00)
    demo_time_step = timedelta(seconds=0.75)

    def __init__(self, dmd):
        self.dmd = dmd
        self.last_x = 0
        self.last_y = 0
        self.animator = gfx.Animator()

    def cursor(self, now):
        seconds = (now.minute * 60) + now.second
        total_dots = (self.dmd.width - 1) * self.dmd.height
        index = int(total_dots * (seconds / 3600))
        x = index % (self.dmd.width - 1)
        y = index // (self.dmd.width - 1)
        return x, y

    def hour_pixels(self, hour):
        pixels = []
        count = hour
        for _ in range(self.dmd.width):
            if count >= 5:
                pixels += [self.color_hour5]
                count -= 5
            elif count > 0:
                pixels += [self.color_hour]
                count -= 1
            else:
                pixels += [(0, 0, 0)]
        return pixels[::-1]

    def display_hours(self, now):
        pixels = self.hour_pixels(now.hour)
        for y in range(self.dmd.height):
            self.dmd.set_pixel((self.dmd.width - 1, y), pixels[y])

    def display_minutes(self, now):
        cursor_x, cursor_y = self.cursor(now)
        for x in range(cursor_x+1):
            self.dmd.set_pixel((x, cursor_y), self.color_dot)
        for y in range(cursor_y+1):
            self.dmd.set_pixel((0, y), self.color_dot)
        self.last_x = x
        self.last_y = y

    def fade_out(self, x, y):
        to_white = gfx.Fade(self.dmd, x, y, self.color_dot, (255, 255, 255))
        to_black = gfx.Fade(self.dmd, x, y, (255, 255, 255), (0, 0, 0))
        self.animator.add(to_white.update, 1)
        self.animator.add(to_black.update, 1, delay=1)

    def fade_in(self, x, y):
        to_white = gfx.Fade(self.dmd, x, y, (0, 0, 0), (255, 255, 255))
        to_dot = gfx.Fade(self.dmd, x, y, (255, 255, 255), self.color_dot)
        self.animator.add(to_white.update, 1)
        self.animator.add(to_dot.update, 1, delay=1)

    def hour_animation(self, now):
        for y in range(8):
            x = self.dmd.width - 1
            color = self.dmd.get_pixel((x, y))
            if color == (0, 0, 0):
                continue
            to_white = gfx.Fade(self.dmd, x, y, color, (255, 255, 255))
            to_black = gfx.Fade(self.dmd, x, y, (255, 255, 255), (0, 0, 0))
            self.animator.add(to_white.update, 1)
            self.animator.add(to_black.update, 1, delay=1)
        slide = gfx.SlideColumnIn(self.dmd, duration=0.75, column=7,
                                  pixels=self.hour_pixels(now.hour))
        self.animator.add(slide.update, 0.75, delay=2)

    def update(self, now):
        self.dmd.clear()
        self.display_hours(now)
        self.display_minutes(now)

    def next(self, now):
        self.animator.service(time.time())
        x, y = self.cursor(now)
        if self.last_x == x:
            return
        if x == 0:
            for px in range(1, self.dmd.width - 1):
                self.fade_out(px, self.last_y)
        if x == 0 and y == 0:
            self.hour_animation(now)
            for py in range(1, self.dmd.height):
                self.fade_out(0, py)
        else:
            self.fade_in(x, y)
        self.last_x = x
        self.last_y = y

    def stop(self):
        self.animator.clear()


class Numeric:

    color_hour = (0x00, 0x00, 0xff)
    color_digit = (0xff, 0xff, 0x00)
    demo_time_step = timedelta(minutes=1)

    def __init__(self, dmd):
        self.dmd = dmd
        self.animator = gfx.Animator()
        self.path = []
        for x in range(0, 7):
            self.path += [(x, 0)]
        for y in range(0, 7):
            self.path += [(6, y)]
        for x in reversed(range(0, 7)):
            self.path += [(x, 6)]
        for y in reversed(range(0, 7)):
            self.path += [(0, y)]

    def cursor(self, now):
        seconds = (now.minute * 60) + now.second
        index = int(len(self.path) * (seconds / 3600))
        return index

    def update(self, now):
        self.dmd.clear()
        for x in range(7):
            for y in range(7):
                self.dmd.set_pixel((x, y), (0x00, 0x00, 0x60))
        hour = now.hour
        if hour > 12:
            hour -= 12
        if hour == 0:
            hour = 12
        d0 = hour % 10
        d1 = hour // 10
        if d1 > 0:
            gfx.render_bitmap(self.dmd, gfx.digits3[d1], self.color_digit, (-1, 1))
            gfx.render_bitmap(self.dmd, gfx.digits3[d0], self.color_digit, (3, 1))
        else:
            gfx.render_bitmap(self.dmd, gfx.digits3[d0], self.color_digit, (2, 1))
        index = self.cursor(now)
        for i in range(index + 1):
            coords = self.path[i]
            self.dmd.set_pixel(coords, self.color_hour)

    def next(self, now):
        self.update(now)
        #pass

    def stop(self):
        self.animator.clear()

class Mode:

    def __init__(self, dmd):
        self.clock = Numeric(dmd)

    def start(self):
        self.clock.update(datetime.now())

    def stop(self):
        self.clock.stop()

    def service(self, event_queue):
        while len(event_queue) > 0:
            event = event_queue.pop()
            if event == 'enter':
                return 'menu'
        self.clock.next(datetime.now())
        return 'clock'

class DemoMode:

    def __init__(self, dmd):
        self.clock = Numeric(dmd)
        self.demo_time = datetime(2019, 1, 1, 20, 30)

    def start(self):
        self.clock.update(self.demo_time)

    def stop(self):
        self.clock.stop()

    def service(self, event_queue):
        while len(event_queue) > 0:
            event = event_queue.pop()
            if event == 'enter':
                return 'menu'
        self.demo_time += self.clock.demo_time_step
        self.clock.next(self.demo_time)
        return 'clock-demo'
