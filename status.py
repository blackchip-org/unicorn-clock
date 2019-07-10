import gfx
import time 

images = {
    'happy': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    'sad': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
}

colors = {
    'happy': (0x00, 0xff, 0x00),
    'sad': (0xff, 0x00, 0x00),
}

def ok(next_mode):
    return {'mode': 'status', 'show': 'happy', 'next_mode': next_mode}

def error(next_mode):
    return {'mode': 'status', 'show': 'sad', 'next_mode': next_mode}


class Mode:

    duration = 1.0 

    def __init__(self, dmd):
        self.dmd = dmd 

    def start(self, show, next_mode, args=None):
        self.image = images[show]
        self.color = colors[show]
        self.next_mode = next_mode 
        self.start_time = time.time()
        
    def stop(self):
        pass 

    def service(self, event_queue):
        now = time.time() 
        if now - self.start_time > self.duration:
            return self.next_mode
        self.dmd.clear() 
        gfx.render_bitmap(self.dmd, self.image, self.color)
