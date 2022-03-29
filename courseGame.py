import pygame
import scene
import inputstream

# GAME
import soundmanager

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Course game')

running = True

clock = pygame.time.Clock()

# scenes
sceneManager = scene.SceneManager()
sceneManager.push(scene.MainMenuScene())

# keyboard
inputStream = inputstream.InputStream()

# sound
soundManager = soundmanager.SoundManager()

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    inputStream.processInput()

    if sceneManager.isEmpty():
        running = False
    sceneManager.update(inputStream, soundManager)
    sceneManager.draw(screen)

    clock.tick(60)

pygame.quit()