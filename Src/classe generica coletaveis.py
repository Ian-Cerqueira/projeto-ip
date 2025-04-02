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
COLORS = {
    'moeda': (255, 0, 0),  #vermelho
    'chave': (0, 255, 0),  #verde
    'estrela': (255, 255, 0)  #amarelo
}

class ItemColetavel(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        self.image = pygame.Surface((40, 50))
        self.image.fill(COLORS[tipo])
        self.rect = self.image.get_rect()
        self.rect.x = randint(50, screen_width - 50)
        self.rect.y = randint(50, screen_height - 50)

