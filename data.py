import pygame
pygame.init()

tileset = None
player = pygame.image.load('player.png')
mobs = pygame.image.load('mobs.png')
ways = pygame.image.load('ways.png')
textfont = pygame.font.Font('vgasysr.fon',19)
edittext = pygame.font.Font('BRLNSDB.TTF',30)
cursorfont = pygame.font.Font('vgasysr.fon',15)
screensize = (800,600)
fullscreen = False
title = "RPG Editor"
