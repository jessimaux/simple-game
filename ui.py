import globals
import utils


class ButtonUI:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.active = False

    def update(self, inputStream):
        pass

    def draw(self, screen):
        if self.active:
            color = globals.GREEN
        else:
            color = globals.WHITE
        utils.drawText(screen, self.text, self.x, self.y, color)