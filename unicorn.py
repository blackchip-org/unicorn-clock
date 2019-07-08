import unicornhat

class UnicornHAT:

    dimensions = 2
    width = 8
    height = 8

    @property
    def rotation(self):
        return unicornhat.get_rotation()

    @rotation.setter
    def rotation(self, value):
        unicornhat.rotation(value)

    @property
    def brightness(self):
        return unicornhat.get_brightness()

    @brightness.setter
    def brightness(self, value):
        unicornhat.brightness(value)

    def set_pixel(self, coord, color):
        unicornhat.set_pixel(coord[0], coord[1], color[0], color[1], color[2])

    def get_pixel(self, coord):
        r, g, b = unicornhat.get_pixel(coord[0], coord[1])
        return (r, g, b)

    def show(self):
        unicornhat.show()

    def clear(self):
        unicornhat.clear()
