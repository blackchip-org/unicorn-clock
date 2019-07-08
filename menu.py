import gfx

class Mode:

    menu_order = ['d', 't']

    def __init__(self, dmd):
        self.dmd = dmd
        self.index = 0

    def start(self):
        self.dmd.clear()

    def stop(self):
        pass

    def service(self, event_queue):
        while len(event_queue) > 0:
            event = event_queue.pop()
            if event == 'exit':
                return 'clock'
            if event == 'up':
                self.index += 1
                if self.index >= len(self.menu_order):
                    self.index = 0
            if event == 'down':
                self.index -= 1
                if self.index < 0:
                    self.index = len(self.menu_order) - 1
        selected = self.menu_order[self.index]
        char = gfx.chars64[selected]
        gfx.render_bitmap(self.dmd, char, (0x00, 0x00, 0xff))
        return 'menu'
