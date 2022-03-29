import ui
import utils
import pygame
import engine
import level
import globals


class Scene:
    def __init__(self):
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def update(self, sm, inputStream, soundManager):
        pass

    def draw(self, screen):
        pass


class MainMenuScene(Scene):
    def __init__(self):
        super(MainMenuScene, self).__init__()
        self.buttons = [
            ui.ButtonUI('New game', 75, 75),
            ui.ButtonUI('Level selection', 75, 100),
            ui.ButtonUI('Exit', 75, 125),
        ]
        self.active_item = 0
        self.buttons[self.active_item].active = True

    def update(self, sm, inputStream, soundManager):
        if inputStream.keyboard.isKeyPressed(pygame.K_DOWN):
            prev_item = self.active_item
            self.active_item = (self.active_item + 1) % len(self.buttons)
            self.buttons[prev_item].active = False
            self.buttons[self.active_item].active = True
        if inputStream.keyboard.isKeyPressed(pygame.K_UP):
            prev_item = self.active_item
            self.active_item = (self.active_item - 1) % len(self.buttons)
            self.buttons[prev_item].active = False
            self.buttons[self.active_item].active = True
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            if self.active_item == 0:
                sm.push(GameScene())
            elif self.active_item == 1:
                sm.push(LevelSelectScene())
            elif self.active_item == 2:
                sm.clear()

    def draw(self, screen):
        screen.fill((50, 50, 50))
        utils.drawText(screen, 'Main Menu', 50, 50, (255, 255, 255))
        for b in self.buttons:
            b.draw(screen)


class LevelSelectScene(Scene):
    def update(self, sm, inputStream, soundManager):
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()

    def draw(self, screen):
        screen.fill((50, 50, 50))
        utils.drawText(screen, 'Level Select', 50, 50, (255, 255, 255))


class GameScene(Scene):
    def __init__(self):
        super(GameScene, self).__init__()
        self.level = level.Level1()
        self.camera = engine.Camera(self.level.entities['player'], (self.level.map.w, self.level.map.h))

    def update(self, sm, inputStream, soundManager):
        player = self.level.entities['player']

        # animations update
        for entity in self.level.entities.values():
            entity.animations.animationList[entity.state].update()

        new_player_x = player.position.rect.x
        new_player_y = player.position.rect.y

        if inputStream.keyboard.isKeyDown(pygame.K_a):
            new_player_x -= 2
            player.direction = 'left'
            player.state = 'walking'
        if inputStream.keyboard.isKeyDown(pygame.K_d):
            new_player_x += 2
            player.direction = 'right'
            player.state = 'walking'
        if not inputStream.keyboard.isKeyDown(pygame.K_a) and not inputStream.keyboard.isKeyDown(pygame.K_d):
            player.state = 'idle'
        if (inputStream.keyboard.isKeyDown(pygame.K_w) or inputStream.keyboard.isKeyDown(pygame.K_SPACE)) and \
                player.on_ground:
            player.speed = -5
            player.on_ground = False
            soundManager.playSound('jump')

        new_player_rect = pygame.Rect(new_player_x, player.position.rect.y, 23, 26)
        x_collision = False
        y_collision = False

        for p in self.level.map.tiles:
            if p.rect.colliderect(new_player_rect):
                x_collision = True
                break

        if x_collision == False:
            player.position.rect.x = new_player_x

        player.speed += player.acc
        new_player_y += player.speed

        new_player_rect = pygame.Rect(player.position.rect.x, new_player_y, 23, 26)

        for p in self.level.map.tiles:
            if p.rect.colliderect(new_player_rect):
                y_collision = True
                player.speed = 0
                if p.rect.y > new_player_y:
                    player.position.rect.y = p.rect.y - 26
                    player.on_ground = True
                break

        if y_collision == False:
            player.position.rect.y = new_player_y

        if player.position.rect.y > 1000:
            player.position.rect.y = 0
            player.position.rect.x = 350

    def draw(self, screen):
        screen.fill(globals.DARK_GREY)
        self.camera.update(screen, self.level.entities.values(), self.level.map.tiles)


class SceneManager:
    def __init__(self):
        self.scenes = []

    def isEmpty(self):
        return len(self.scenes) == 0

    def enterScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onEnter()

    def exitScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onExit()

    def update(self, inputStream, soundManager):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self, inputStream, soundManager)

    def draw(self, screen):
        if len(self.scenes) > 0:
            self.scenes[-1].draw(screen)
        pygame.display.flip()

    def push(self, scene):
        self.exitScene()
        self.scenes.append(scene)
        self.enterScene()

    def pop(self):
        self.exitScene()
        self.scenes.pop()
        self.enterScene()

    def set(self, scene):
        self.scenes.clear()
        self.push(scene)

    def clear(self):
        self.scenes.clear()