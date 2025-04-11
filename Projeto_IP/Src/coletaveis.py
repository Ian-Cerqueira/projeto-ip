import pygame
from random import randint
from sys import exit

pygame.init()

SPRITES = {
    'moeda': "assets/coin_cin.png", 
    'chave': "assets/key_nave.png",  
    'vida': "assets/heart pixel art 16x16.png",  
    'nave': "assets/nave_fase_1.png"}

class ItemColetavel(pygame.sprite.Sprite):
    def __init__(self, tipo, loc_x, loc_y):
        super().__init__()
        self.tipo = tipo
        if self.tipo == 'moeda' :
            self.image = pygame.transform.scale2x(pygame.image.load(SPRITES[tipo]))
        elif self.tipo == 'vida' :
            self.image = pygame.transform.scale2x(pygame.image.load(SPRITES[tipo]))
        elif self.tipo == 'nave' :
            self.image = pygame.transform.flip(pygame.transform.scale_by(pygame.image.load(SPRITES[tipo]), 0.4), True, False)
        else:
            self.image = pygame.image.load(SPRITES[tipo])
        self.rect = self.image.get_rect(topleft=(loc_x, loc_y))
        self.mask = pygame.mask.from_surface(self.image)
