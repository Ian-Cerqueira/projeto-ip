import pygame as pg
import sys

pg.init()
screen = pg.display.set_mode((1000, 720))
pixel_font = pg.font.Font("assets/Pixeltype.ttf", 40)

class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text_input
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.font = pixel_font.render(self.text_input, True, "white")
        self.font_rect = self.font.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.font, self.font_rect)

    def verificar_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom):
            print("Botão Pressionado")

    def mudar_cor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom):
            self.font = pixel_font.render(self.text_input, True, "green")
        else:
            self.font = pixel_font.render(self.text_input, True, "white")

button_surface = pg.image.load("assets/Button.png")
button_surface = pg.transform.scale(button_surface, (205, 84))
