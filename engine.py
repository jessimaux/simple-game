import pygame
import json
import utils
import globals
import math

# TODO:
# fix camera attribute
# add worldPos

class Camera:
    def __init__(self, track, w_size):
        self.entityToTrack = track
        self.x = 0
        self.y = 0
        self.world_size = w_size
        self.offset = -350

    def update(self, screen, entities, platforms):
        for p in platforms:
            p.rect.x -= self.offset
            p.draw(screen)

        for entity in entities:
            # debug
            pygame.draw.rect(screen, (255, 0, 0), entity.position.rect, 1)
            utils.drawText(screen, str(entity.position.rect.x) + ';' + str(entity.position.rect.y), entity.position.rect.x - 15, entity.position.rect.y - 15, globals.WHITE)

            self.entityToTrack.position.rect.x -= self.offset

            if entity.direction == 'right':
                entity.animations.animationList[entity.state].draw(screen, entity.position.rect.x,
                                                                   entity.position.rect.y, False, False)
            elif entity.direction == 'left':
                entity.animations.animationList[entity.state].draw(screen, entity.position.rect.x,
                                                                   entity.position.rect.y, True, False)

        #utils.drawText(screen, str(self.scrollX) + ';' + str(self.scrollY), 0, 0, globals.WHITE)
        self.offset = int(self.offset - self.offset + (self.entityToTrack.position.rect.x - 350))
        print(self.offset)



class Position:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)


class Animations:
    def __init__(self):
        self.animationList = {}

    def add(self, state, animation):
        self.animationList[state] = animation


class Animation:
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 8

    def update(self):
        self.animationTimer += 1
        if self.animationTimer >= self.animationSpeed:
            self.animationTimer = 0
            self.imageIndex += 1
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0

    def draw(self, screen, x, y, flipX, flipY):
        screen.blit(pygame.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (x, y))


class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, id):
        x = globals.SPRITE_SIZE * (id % self.data['columns'])
        y = globals.SPRITE_SIZE * (id // self.data['columns'])
        w, h = globals.SPRITE_SIZE, globals.SPRITE_SIZE
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))

        return sprite


class Tile:
    def __init__(self, id, x, y, spritesheet):
        self.image = spritesheet.get_sprite(id)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface, offset=0):
        # debug
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)

        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap:
    def __init__(self, filename, spritesheet):
        self.w = 0
        self.h = 0
        self.tile_size = globals.SPRITE_SIZE
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)

    def load_tiles(self, filename):
        tiles = []
        tile_map = utils.read_csv(filename, ',')
        x, y = 0, 0
        for row in tile_map:
            x = 0
            for tile in row:
                if tile == '32':
                    tiles.append(Tile(32, x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '33':
                    tiles.append(Tile(33, x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '34':
                    tiles.append(Tile(34, x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '41':
                    tiles.append(Tile(41, x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '42':
                    tiles.append(Tile(42, x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '43':
                    tiles.append(Tile(43, x * self.tile_size, y * self.tile_size, self.spritesheet))

                x += 1

            # Move to next row
            y += 1
        self.w = x * self.tile_size
        self.h = y * self.tile_size

        return tiles