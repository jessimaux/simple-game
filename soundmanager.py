import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.soundVolume = 0.4
        self.musicVolume = 0  # 0.2
        self.targetMusicVolume = 0  # 0.2
        self.nextMusic = None
        self.currentMusic = None
        self.sounds = {
            'jump': pygame.mixer.Sound('sounds/03_Jump_v2.ogg'),
        }

    def playSound(self, soundName):
        self.sounds[soundName].set_volume(self.soundVolume)
        self.sounds[soundName].play()