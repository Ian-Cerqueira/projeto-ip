import pygame
from random import randint
from sys import exit

pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

#as cores v]ao ser os tipos de coletaveis
SPRITES = {
    'moeda': "sprite_sheets/pixil-frame-0.png",  #vermelho
    'chave': "sprite_sheets/key(1).png",  #verde
    'estrela': "sprite_sheets/pixil-frame-star.png"  #amarelo
}

class ItemColetavel(pygame.sprite.Sprite):
    def __init__(self, tipo, loc_x, loc_y):
        super().__init__()
        self.tipo = tipo
        self.image = pygame.Surface((40, 50))
        self.image = pygame.image.load(SPRITES[tipo])
        self.rect = self.image.get_rect()
        self.rect.x = loc_x
        self.rect.y = loc_y

