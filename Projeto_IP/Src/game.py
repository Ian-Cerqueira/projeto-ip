import pygame as pg
import sys
from classe_Button import Button
from primeira_fase import jogo_1
from space_shooter import jogo_2

# Configurações da tela e fonts
largura_tela = 1000
altura_tela = 720
tela = pg.display.set_mode((largura_tela, altura_tela))
pg.display.set_caption("ChronoCIn")
pixel_font = pg.font.Font("assets/Pixeltype.ttf", 40)
title_font = pg.font.Font("assets/Pixeltype.ttf", 100)
FPS = 60
clock = pg.time.Clock()

pg.init()

def primeira_fase():
    passou_fase = jogo_1()
    if passou_fase :
        segunda_fase()
    menu()

def segunda_fase():
    jogo_2()
    
    menu()

def menu():
    
    # Carrega o background de menu e ajusta a tela
    tela = pg.display.set_mode((largura_tela, altura_tela))
    menu_background = pg.image.load("assets/background_menu.jpg")
    menu_background = pg.transform.scale(menu_background, (largura_tela, altura_tela))
    
    # Renderiza o título do menu
    menu_text = title_font.render("ChronoCIn", True, "white")
    menu_text_rect = menu_text.get_rect(center=(500, 80))
    
    # Carrega a imagem do botão e redimensiona
    button_image = pg.image.load("assets/Button.png")
    button_image = pg.transform.scale(button_image, (205, 84))
    
    # Cria os botões Play e Quit
    button_play = Button(button_image, 500, 300, "Play")
    button_quit = Button(button_image, 500, 500, "Quit")
    
    run = True
    while run:
        mouse_pos = pg.mouse.get_pos()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # Se o mouse clicar sobre o botão Play, inicia a primeira fase
                if button_play.rect.collidepoint(mouse_pos):
                    primeira_fase()
                # Se o mouse clicar sobre o botão Quit, encerra o programa
                if button_quit.rect.collidepoint(mouse_pos):
                    run = False

        # Desenha o background e o título do menu
        tela.blit(menu_background, (0, 0))
        tela.blit(menu_text, menu_text_rect)
        
        # Atualiza a cor dos botões conforme a posição do mouse e os desenha
        for button in (button_play, button_quit):
            button.mudar_cor(mouse_pos)
            button.update()
        
        pg.display.update()
    
    pg.quit()
    sys.exit()

run = True
while run :
    clock.tick(FPS)    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    menu()