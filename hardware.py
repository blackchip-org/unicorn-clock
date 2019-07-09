from unicorn import UnicornHAT
from gpiozero import Button

class Hardware:

    def __init__(self):
        bounce_time = 0.02
        self.dmd = UnicornHAT()
        self.enter_button = Button(6, bounce_time=bounce_time)
        self.up_button = Button(13, bounce_time=bounce_time)
        self.down_button = Button(16, bounce_time=bounce_time)
        self.exit_button = Button(26, bounce_time=bounce_time)

    def service(self):
        pass
