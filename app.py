#!/usr/bin/env python3

import time
from datetime import datetime
from gpiozero import Button
import clock
import menu
import status 

try:
    from hardware import Hardware
except Exception:
    from virtual import Hardware

class App:

    def __init__(self):
        self.now = 0
        self.demo_now = 0
        self.event_queue = []
        self.hw = Hardware()
        self.hw.enter_button.when_pressed = self.enter_button_pressed
        self.hw.up_button.when_pressed = self.up_button_pressed
        self.hw.down_button.when_pressed = self.down_button_pressed
        self.hw.exit_button.when_pressed = self.exit_button_pressed
        self.dmd = self.hw.dmd
        self.modes = {
            'clock': clock.Mode(self.dmd),
            'menu': menu.Mode(self.dmd),
            'clock-select': menu.ClockSelectMode(self.dmd),
            'status': status.Mode(self.dmd),
        }
        self.mode = 'clock'
        self.dmd.brightness = 0.5
        self.dmd.rotation = 180
        self.modes[self.mode].start()
        self.dmd.show()

    def enter_button_pressed(self):
        self.event_queue.insert(0, 'enter')

    def up_button_pressed(self):
        self.event_queue.insert(0, 'up')

    def down_button_pressed(self):
        self.event_queue.insert(0, 'down')

    def exit_button_pressed(self):
        self.event_queue.insert(0, 'exit')

    def loop(self):
        next_mode = self.modes[self.mode].service(self.event_queue)
        if next_mode is not None:
            next_mode_name = next_mode['mode']
            self.modes[self.mode].stop()
            kwargs = dict(next_mode) 
            del kwargs['mode']
            self.modes[next_mode_name].start(**kwargs)
            self.mode = next_mode_name
        self.dmd.show()
        self.hw.service()

    def run(self):
        interval = 1/60
        while True:
            self.now = time.time()
            self.loop()
            remaining = interval - (time.time() - self.now)
            if remaining > 0:
                time.sleep(remaining)

app = App()
app.run()
