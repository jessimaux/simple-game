import engine
import entity


class Level:
    def __init__(self):
        self.map = None
        self.entities = dict()


class Level1(Level):
    def __init__(self):
        super(Level1, self).__init__()
        self.map = engine.TileMap('map/test_level_platforms.csv', engine.SpriteSheet('map/test.png'))
        self.entities = {
            'player': entity.Player(0, 0),
        }