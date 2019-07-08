#!/usr/bin/python3

import time
from unicorn import UnicornHAT
from datetime import datetime
from gpiozero import Button
import clock
import menu

class Hardware:

    def __init__(self):
        bounce_time = 0.02
        self.dmd = UnicornHAT()
        self.enter_button = Button(6, bounce_time=bounce_time)
        self.up_button = Button(13, bounce_time=bounce_time)
        self.down_button = Button(16, bounce_time=bounce_time)
        self.exit_button = Button(26, bounce_time=bounce_time)


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
            'clock-demo': clock.DemoMode(self.dmd),
            'menu': menu.Mode(self.dmd),
        }
        self.mode = 'clock-demo'
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
        if next_mode != self.mode:
            self.modes[self.mode].stop()
            self.modes[next_mode].start()
            self.mode = next_mode
        self.dmd.show()

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
