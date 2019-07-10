from datetime import datetime 
import time

import clock 
import status
import gfx

menu_items = {
    'brightness': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    'clock': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    'time': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    'hour': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    'rotation': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
}

class Mode:

    menu_order = [
        'clock',
        'time',
        'hour',
        'rotation',
        'brightness'
    ]

    def __init__(self, dmd):
        self.dmd = dmd
        self.index = 0
        self.animator = gfx.Animator()

    def start(self):
        slide_in = gfx.Slide(self.dmd, y_step=-1)
        self.animator.add(slide_in.update, 0.1)

    def next(self):
        self.index += 1
        if self.index >= len(self.menu_order):
            self.index = 0
        slide_left = gfx.Slide(self.dmd, x_step=1)
        self.animator.add(slide_left.update, 0.1)

    def previous(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.menu_order) - 1
        slide_right = gfx.Slide(self.dmd, x_step=-1)
        self.animator.add(slide_right.update, 0.1)

    def stop(self):
        pass

    def service(self, event_queue):
        while len(event_queue) > 0:
            event = event_queue.pop()
            if event == 'exit':
                return {'mode': 'clock'}
            if event == 'up':
                self.next()
            if event == 'down':
                self.previous()
            if event == 'enter':
                return {'mode': 'clock-select'}
        selected = self.menu_order[self.index]
        display = menu_items[selected]
        self.dmd.clear()
        gfx.render_bitmap(self.dmd, display, (0x00, 0x00, 0xff))
        self.animator.service(time.time())


class ClockSelectMode:

    def __init__(self, dmd):
        self.clocks = [
            clock.XY(dmd),
            clock.Numeric(dmd),
        ]
        self.index = 0 
        self.clock = self.clocks[self.index]
        self.demo_time = datetime(2019, 1, 1, 20)

    def start(self):
        self.clock.update(self.demo_time)

    def stop(self):
        self.clock.stop()

    def next(self):
        self.clock.stop()
        self.index += 1
        if self.index >= len(self.clocks):
            self.index = 0 
        self.clock = self.clocks[self.index]
        self.clock.update(self.demo_time) 

    def previous(self):
        self.clock.stop()
        self.index -= 1 
        if self.index < 0:
            self.index = len(self.clocks) - 1
        self.clock = self.clocks[self.index]
        self.clock.update(self.demo_time) 

    def service(self, event_queue):
        while len(event_queue) > 0:
            event = event_queue.pop()
            if event == 'up': 
                self.next() 
            if event == 'down':
                self.previous()
            if event == 'exit':
                return {'mode': 'menu'}
            if event == 'enter':
                return status.ok({'mode': 'menu'})
        self.demo_time += self.clock.demo_time_step
        self.clock.next(self.demo_time)


