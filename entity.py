import engine
import pygame


class Entity:
    def __init__(self):
        self.state = 'idle'
        self.position = None
        self.animations = engine.Animations()
        self.direction = 'right'


class Player(Entity):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.position = engine.Position(x, y, 23, 26)
        self.animations.add('idle', engine.Animation([
            pygame.image.load('images/player/idle/sprite_00.png'),
            pygame.image.load('images/player/idle/sprite_01.png'),
            pygame.image.load('images/player/idle/sprite_02.png'),
            pygame.image.load('images/player/idle/sprite_03.png'),
        ]))
        self.animations.add('walking', engine.Animation([
            pygame.image.load('images/player/walking/sprite_04.png'),
            pygame.image.load('images/player/walking/sprite_05.png'),
            pygame.image.load('images/player/walking/sprite_06.png'),
            pygame.image.load('images/player/walking/sprite_07.png'),
            pygame.image.load('images/player/walking/sprite_08.png'),
            pygame.image.load('images/player/walking/sprite_09.png'),
        ]))
        self.speed = 0
        self.acc = 0.2
        self.on_ground = False