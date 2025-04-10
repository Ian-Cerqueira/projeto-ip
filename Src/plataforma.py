import pygame as pg

pg.init()

class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pg.Surface((largura, altura))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(self.image)