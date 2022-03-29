import pygame
import os, csv

pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 14)

def drawText(screen, t, x, y, color):
    text = font.render(t, True, color)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x,y)

    screen.blit(text, text_rectangle)

def read_csv(filename, sep):
    data_list = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=sep)
        for row in data:
            data_list.append(list(row))
    return data_list